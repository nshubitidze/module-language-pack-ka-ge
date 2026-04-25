"""Lint ka_GE.csv. Exit 0 on clean, 1 on violations.

Checks:
  1. Every row has exactly 4 columns.
  2. No duplicate (source, module) composite keys.
  3. Per non-empty translation:
     a. Placeholder count matches: %1..%9, %s, %d (multiset compare).
     b. {{ and }} brace pair count matches.
     c. < and > angle bracket count matches.
     d. No bare Latin letter mid-word in Mkhedruli (whitelist exempt).
     e. Trailing punctuation matches: . : ? ! ; (… and ... interchangeable).
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path("/home/nika/module-language-pack-ka-ge")
CSV_PATH = REPO_ROOT / "ka_GE.csv"

# Brand whitelist — verbatim Latin tokens allowed inside translations
BRAND_WHITELIST: frozenset[str] = frozenset({
    "Magento", "PayPal", "Adobe", "Stripe", "Klarna", "Braintree",
    "FedEx", "UPS", "DHL", "USPS", "ElasticSearch", "OpenSearch",
    "MySQL", "MariaDB", "Redis", "RabbitMQ", "Varnish",
    "GraphQL", "REST", "SOAP", "AJAX", "JSON", "XML", "YAML",
    "CSV", "PDF", "HTML", "CSS", "JS", "HTTP", "HTTPS",
    "URL", "URI", "API", "SKU", "UPC", "EAN", "ISBN",
    "IBAN", "BIC", "SWIFT", "IP", "GPS",
    "OAuth", "OAuth2", "JWT", "GDPR", "CAPTCHA", "reCAPTCHA",
    "TBC", "BOG", "Flitt", "Shippo", "Wolt",
    "Authorize.Net",
    "Amazon", "Apple", "Google", "eBay",
    "ID", "VAT", "VAT-",
    "OK", "USD", "EUR", "GBP", "GEL",
    "US", "GE", "DE", "GB",
})

GE_RANGE = ("ა", "ჿ")


def is_georgian(ch: str) -> bool:
    return GE_RANGE[0] <= ch <= GE_RANGE[1]


def lint_row(row: list[str], lineno: int) -> list[str]:
    violations: list[str] = []

    if len(row) != 4:
        violations.append(f"L{lineno}: wrong column count {len(row)} (expected 4)")
        return violations  # other checks unsafe

    src, tgt, kind, module = row

    # Skip if untranslated or pass-through
    if not tgt or tgt == src:
        return violations
    if not tgt.strip():
        return violations

    # Placeholders
    src_pn = Counter(re.findall(r"%[1-9]", src))
    tgt_pn = Counter(re.findall(r"%[1-9]", tgt))
    if src_pn != tgt_pn:
        violations.append(
            f"L{lineno} [{module}]: %N placeholder mismatch "
            f"src={dict(src_pn)} tgt={dict(tgt_pn)} "
            f"src={src!r}"
        )
    src_ps = src.count("%s")
    tgt_ps = tgt.count("%s")
    if src_ps != tgt_ps:
        violations.append(
            f"L{lineno} [{module}]: %s count mismatch src={src_ps} tgt={tgt_ps}"
        )
    src_pd = src.count("%d")
    tgt_pd = tgt.count("%d")
    if src_pd != tgt_pd:
        violations.append(
            f"L{lineno} [{module}]: %d count mismatch src={src_pd} tgt={tgt_pd}"
        )

    # Braces
    src_open = src.count("{{")
    src_close = src.count("}}")
    tgt_open = tgt.count("{{")
    tgt_close = tgt.count("}}")
    if src_open != tgt_open or src_close != tgt_close:
        violations.append(
            f"L{lineno} [{module}]: {{{{}}}} brace mismatch "
            f"src=({src_open},{src_close}) tgt=({tgt_open},{tgt_close})"
        )

    # Angle brackets
    src_lt = src.count("<")
    src_gt = src.count(">")
    tgt_lt = tgt.count("<")
    tgt_gt = tgt.count(">")
    if src_lt != tgt_lt or src_gt != tgt_gt:
        violations.append(
            f"L{lineno} [{module}]: < / > angle bracket mismatch "
            f"src=({src_lt},{src_gt}) tgt=({tgt_lt},{tgt_gt})"
        )

    # Mid-word mixed-script: a Latin letter immediately adjacent to a
    # Georgian letter without a separator. Tokenize tgt by whitespace +
    # punctuation; flag any token that contains BOTH Latin and Georgian
    # letters AND is not a brand whitelist member.
    # Allowed: hyphen-separated like "PayPal-ით" (split on hyphen first).
    for raw_token in re.split(r"[\s,.;:!?()\[\]\"“”‘’/]+", tgt):
        if not raw_token:
            continue
        # Hyphen handling: split into parts; brand-Latin + ge-suffix is OK
        parts = raw_token.split("-")
        if len(parts) > 1:
            # Each part must individually be either pure-Latin (whitelist) or pure-Georgian
            ok = True
            for p in parts:
                if not p:
                    continue
                if any(is_georgian(c) for c in p) and any(c.isascii() and c.isalpha() for c in p):
                    ok = False
                    break
            if not ok:
                violations.append(
                    f"L{lineno} [{module}]: mixed-script token {raw_token!r}"
                )
            continue
        has_lat = any(c.isascii() and c.isalpha() for c in raw_token)
        has_ge = any(is_georgian(c) for c in raw_token)
        if has_lat and has_ge:
            # Not allowed — even brand whitelist needs hyphen
            violations.append(
                f"L{lineno} [{module}]: mixed-script token {raw_token!r}"
            )

    # Trailing punctuation
    def trail(s: str) -> str:
        s = s.rstrip()
        # treat ... and … as same class
        if s.endswith("..."):
            return "…"
        return s[-1] if s and s[-1] in ".:?!;…" else ""

    if trail(src) != trail(tgt):
        violations.append(
            f"L{lineno} [{module}]: trailing punctuation mismatch "
            f"src={trail(src)!r} tgt={trail(tgt)!r} "
            f"src={src!r}"
        )

    return violations


def main() -> int:
    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} not found", file=sys.stderr)
        return 2

    rows: list[list[str]] = []
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        for row in reader:
            rows.append(row)

    violations: list[str] = []
    seen: dict[tuple[str, str], int] = {}

    for i, row in enumerate(rows, start=1):
        violations.extend(lint_row(row, i))
        if len(row) >= 4:
            key = (row[0], row[3])
            if key in seen:
                violations.append(
                    f"L{i} [{row[3]}]: duplicate (source,module) — first at L{seen[key]}: {row[0]!r}"
                )
            else:
                seen[key] = i

    total = len(rows)
    translated = sum(1 for r in rows if len(r) >= 2 and r[1] and r[1] != r[0])

    if violations:
        print("LINT VIOLATIONS:")
        for v in violations[:200]:
            print("  " + v)
        if len(violations) > 200:
            print(f"  ... ({len(violations) - 200} more suppressed)")
        print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  Total rows:        {total}")
    print(f"  Translated rows:   {translated}")
    print(f"  Untranslated rows: {total - translated}")
    print(f"  Violations:        {len(violations)}")
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
