"""Build single consolidated ka_GE.csv from Mageplaza German reference.

Steps:
  1. Read /tmp/mageplaza-ref/de/de_DE.csv (15,328 rows, 4 cols).
  2. For each row, replace col[1] (German) with empty string. Preserve
     col[0] (English source), col[2] ("module"), col[3] (module name).
  3. Append rows from existing Shubo_*.csv files at the language pack root
     as ("English","Georgian","module","Shubo_X").
  4. Seed col[1] from existing trusted Magento_*.csv files where module
     basename matches col[3] AND col[0] matches an entry's source.
  5. Apply CANONICAL dictionary substitution to still-empty rows.
  6. Apply PATTERNS regex substitution to still-empty rows.
  7. Write /home/nika/module-language-pack-ka-ge/ka_GE.csv with csv.writer
     using QUOTE_ALL so output mirrors Mageplaza style.

Print progress + final coverage to stdout.
"""

from __future__ import annotations

import csv
import glob
import os
import sys
from pathlib import Path

# Make canonical importable when run as script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from canonical import (  # noqa: E402
    CANONICAL,
    PATTERNS,
    apply_canonical,
    apply_pattern,
)

REPO_ROOT = Path("/home/nika/module-language-pack-ka-ge")
MAGEPLAZA_REF = Path("/tmp/mageplaza-ref/de/de_DE.csv")
OUT_CSV = REPO_ROOT / "ka_GE.csv"


def load_mageplaza_skeleton() -> list[list[str]]:
    """Load Mageplaza CSV; reset column 2 to empty string. Dedupe (source,module).

    Mageplaza's upstream CSV has 5 duplicate (source,module) pairs that we drop
    so downstream lint stays clean. First occurrence wins.
    """
    rows: list[list[str]] = []
    seen: set[tuple[str, str]] = set()
    with MAGEPLAZA_REF.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        for row in reader:
            if len(row) < 4:
                # Pad short rows
                while len(row) < 4:
                    row.append("")
            elif len(row) > 4:
                row = row[:4]
            key = (row[0], row[3])
            if key in seen:
                continue
            seen.add(key)
            rows.append([row[0], "", row[2], row[3]])
    return rows


def load_shubo_rows() -> list[list[str]]:
    """Load Shubo_*.csv (already-translated 2-col files); emit 4-col rows."""
    rows: list[list[str]] = []
    for fpath in sorted(REPO_ROOT.glob("Shubo_*.csv")):
        module = fpath.stem  # "Shubo_Merchant" etc.
        with fpath.open(encoding="utf-8", newline="") as fh:
            reader = csv.reader(fh)
            for row in reader:
                if len(row) < 2:
                    continue
                src, tgt = row[0], row[1]
                rows.append([src, tgt, "module", module])
    return rows


def load_seed_index() -> dict[tuple[str, str], str]:
    """Build (module, source) -> trusted_translation index from Magento_*.csv.

    Module basename is the file stem (e.g. 'Magento_Sales').
    Also include PayPal_Braintree.csv and any non-Shubo extras.
    """
    index: dict[tuple[str, str], str] = {}
    for fpath in sorted(REPO_ROOT.glob("*.csv")):
        if fpath.name.startswith("Shubo_"):
            continue
        if fpath.name == "ka_GE.csv":
            continue
        if fpath.name.startswith("_"):
            continue
        module = fpath.stem
        with fpath.open(encoding="utf-8", newline="") as fh:
            reader = csv.reader(fh)
            for row in reader:
                if len(row) < 2:
                    continue
                src, tgt = row[0], row[1]
                if not tgt or tgt == src:
                    continue
                # Skip empty-translation rows
                if not tgt.strip():
                    continue
                index[(module, src)] = tgt
    return index


def main() -> int:
    print("[1/6] Loading Mageplaza skeleton...", flush=True)
    skeleton = load_mageplaza_skeleton()
    print(f"      {len(skeleton)} rows from Mageplaza ref", flush=True)

    print("[2/6] Loading Shubo_*.csv rows...", flush=True)
    shubo_rows = load_shubo_rows()
    print(f"      {len(shubo_rows)} pre-translated Shubo rows", flush=True)

    rows = skeleton + shubo_rows

    print("[3/6] Building seed index from existing trusted Magento_*.csv...", flush=True)
    seed_index = load_seed_index()
    print(f"      {len(seed_index)} (module,source) -> translation entries", flush=True)

    seeded = 0
    for r in rows:
        if r[1]:
            continue  # already translated (Shubo rows)
        key = (r[3], r[0])
        if key in seed_index:
            r[1] = seed_index[key]
            seeded += 1
    print(f"[4/6] Seeded {seeded} translations from trusted Magento sources", flush=True)

    canonical_hits = 0
    pattern_hits = 0
    for r in rows:
        if r[1]:
            continue
        # canonical exact-match
        canon_translation = apply_canonical(r[0])
        if canon_translation is not None:
            r[1] = canon_translation
            canonical_hits += 1
            continue
        # pattern fallback
        patt_translation = apply_pattern(r[0])
        if patt_translation is not None:
            r[1] = patt_translation
            pattern_hits += 1

    print(f"[5/6] Canonical hits: {canonical_hits}; Pattern hits: {pattern_hits}", flush=True)

    print(f"[6/6] Writing {OUT_CSV} ({len(rows)} rows)", flush=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, quoting=csv.QUOTE_ALL)
        for r in rows:
            writer.writerow(r)

    translated = sum(1 for r in rows if r[1] and r[1] != r[0])
    pct = 100.0 * translated / max(len(rows), 1)
    print(
        f"      Total rows: {len(rows)}; translated: {translated} "
        f"({pct:.2f}% incl. brand-passthrough)",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
