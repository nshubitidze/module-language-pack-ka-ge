# Shubo Language Pack — ka_GE (Georgian)

Magento 2 language package providing Georgian (`ka_GE`) translations for storefront, checkout, and Shubo marketplace modules.

## 1. Repo Layout

```
module-language-pack-ka-ge/
├── composer.json              # type=magento2-language, name=shubo/language-pack-ka-ge, MIT
├── registration.php           # ComponentRegistrar::LANGUAGE, 'shubo_ka_ge'
├── language.xml               # <code>ka_GE</code><vendor>Shubo</vendor><package>ka_GE</package>
├── Magento_Catalog.csv        # per-Component CSV (canonical Magento pack layout)
├── Magento_Checkout.csv
├── Magento_Customer.csv
├── …                          # one CSV per Magento/Shubo module with translations
├── Shubo_TbcPayment.csv
├── Shubo_BogPayment.csv
├── LICENSE                    # MIT
├── CHANGELOG.md               # Keep-a-Changelog, SemVer
├── README.md                  # Install + contribution instructions
├── _translate.py              # Dictionary-driven generator (dev tool — not shipped)
├── _phrases-raw.csv           # Output of `bin/magento i18n:collect-phrases --magento` (dev input)
├── _coverage.txt              # Per-module coverage report (dev output)
├── docs/
│   └── design.md              # This file
└── .github/workflows/ci.yml   # composer validate + schema lint
```

**Per-module CSVs at repo root** is the canonical Magento language-pack layout (see `vendor/magento/language-de_de/` plus community packs at swissup, mageplaza, splendor). The phrase renderer (`Magento\Framework\Phrase\Renderer\Translate`) looks up `i18n_<locale>_<Component>_<Module>.csv` during pack loading.

## 2. Translation Strategy

- **Dictionary-driven.** `_translate.py` embeds a curated ~300-term Georgian UI vocabulary mapping English → Georgian (e.g. `"Add to Cart" → "კალათაში დამატება"`).
- **Exact-match look-up** (case-insensitive on key, exact on value). Optional leading/trailing-punctuation strip for phrases like `Save.` or `(Cancel)`.
- **Omit-unknown.** Rows without a dictionary hit are omitted from output CSV. Magento falls back to the source English string — safer than shipping incorrect Georgian.
- **Two tiers:**
  - **P1** (storefront + checkout + Shubo): Magento_Catalog, _Checkout, _Customer, _Cms, _Theme, _Sales, _OfflinePayments, _Payment, _Shipping, _Tax, _Ui, _Wishlist, _Review, _SalesRule, _Quote, _GiftMessage, _Newsletter, _Contact, _ProductAlert, _Search, _CatalogSearch, _Directory, plus every Shubo_* module. 0.1.0 ships these.
  - **Auto-backfill** (admin/B2B/dev-tooling): Magento_Backend, _Reports, _Integration, _User, _ImportExport, _Config, _Eav, etc. Shared-dictionary auto-matches only; deferred to 0.2.0 with explicit `# AUTO: needs human pass` marker rows at top.

## 3. Quality Bar

- Every row CSV-escaped (RFC 4180): `csv.QUOTE_ALL` — quotes doubled, commas/newlines safe inside quoted fields.
- No empty translations — the generator drops empty-RHS rows.
- Placeholder preserved — `%1 %2 %s %d` pass-through unchanged in dictionary values (generator does not rewrite them).
- No rows where source already contains Georgian (defence against double-translation on re-runs).
- UTF-8, LF, no BOM.

## 4. Versioning + Compatibility

- SemVer. Initial release **0.1.0-alpha**.
- Magento target: **2.4.8+** (composer `magento/framework: >=103.0`).
- PHP 8.4+ (matches platform).
- Breaking changes to CSV keys are patch-level (Magento fallback = English source, no runtime break).

## 5. Install Contract

```bash
composer require shubo/language-pack-ka-ge
bin/magento setup:upgrade
bin/magento config:set general/locale/code ka_GE --scope=default
bin/magento cache:flush
```

Optional UI path: Admin → Stores → Configuration → General → Locale Options → Locale = `Georgian (Georgia)`.

## 6. License

**MIT.** Matches Magento language-pack ecosystem norm (de_de, fr_fr, es_es all permissive). Enables fork/contribution from community without CLA friction.

## 7. Publication Roadmap

- **0.1.0-alpha** — storefront + checkout + Shubo modules. Initial seed (~1,300 rows across ~120 module CSVs).
- **0.2.0** — admin backfill with AUTO markers. Additional ~6,000 rows.
- **0.5.0** — AUTO rows pass first human review round.
- **1.0.0** — stable. Gate: 95%+ of P1 rows human-reviewed, zero validator warnings, two consecutive 0.x releases with no translation-correctness bug reports.
