# Shubo — Magento 2 Georgian Language Pack (`ka_GE`)

[![Packagist Version](https://img.shields.io/badge/packagist-0.1.0--alpha-orange.svg)](https://packagist.org/packages/shubo/language-pack-ka-ge)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Magento](https://img.shields.io/badge/Magento-2.4.8%2B-8a2be2.svg)](https://magento.com)

Georgian (Georgia) — `ka_GE` — language pack for Magento 2.4.8+. Covers storefront, checkout, customer-account, and the Shubo marketplace stack (vendor onboarding, commission, payout, split payments, shipping, cookie consent).

**Status:** `0.1.0-alpha` — ~1,680 translated rows across 120+ module CSVs. Storefront + checkout are human-reviewed; admin UI is deferred to 0.2.0.

---

## Installation

```bash
composer require shubo/language-pack-ka-ge
bin/magento setup:upgrade
bin/magento setup:di:compile
bin/magento setup:static-content:deploy ka_GE
bin/magento config:set general/locale/code ka_GE --scope=default
bin/magento cache:flush
```

Alternative UI path: **Admin → Stores → Configuration → General → Locale Options → Locale = `Georgian (Georgia)`**.

Per-store switch (multi-store setups):

```bash
bin/magento config:set general/locale/code ka_GE --scope=stores --scope-code=<store-code>
```

---

## Coverage

| Tier | Modules | Translated rows | Review status |
|---|---:|---:|---|
| **P1** — storefront + checkout + Shubo marketplace | 30 | ~920 | dictionary-reviewed by Georgian speaker |
| **Auto-backfill** — admin / B2B / dev tooling | 93 | ~760 | shared-dictionary matches only; needs human pass (0.2.0) |

Per-module detail in [`_coverage.txt`](./_coverage.txt). Rows without a confident Georgian translation are **omitted**: Magento falls back to the English source — safer than shipping wrong Georgian.

Top P1 modules by coverage:

| Module | Rows | % of source |
|---|---:|---:|
| Shubo_CookieConsent | 12 | 41% |
| Shubo_Commission | 16 | 33% |
| Magento_Checkout | 63 | 28% |
| Shubo_Merchant | 45 | 23% |
| Magento_Review | 29 | 21% |
| Shubo_ShippingCore | 23 | 19% |
| Magento_Shipping | 32 | 17% |
| Magento_Payment | 12 | 17% |
| Magento_Sales | 134 | 16% |
| Magento_Ui | 35 | 15% |

---

## How it was built

1. `bin/magento i18n:collect-phrases --magento > _phrases-raw.csv` — 13,520 unique source phrases from 295 Magento + Shubo modules.
2. `_translate.py` embeds a curated Georgian UI dictionary (~500 canonical ecommerce terms) and maps source phrases to Georgian via exact-match (case-insensitive key, casing-preserved output). Common leading/trailing punctuation is stripped + restored.
3. Per-component CSVs are emitted at repo root using the canonical Magento language-pack layout (`Magento_<Module>.csv`, `Shubo_<Module>.csv`).
4. Coverage + per-module stats reported in `_coverage.txt`.

The dictionary and script are shipped in the repo (`_translate.py`) so contributors can add terms and regenerate; they are excluded from the Magento auto-loader via composer's `autoload` whitelist (`files: [registration.php]`).

---

## Contributing

Pull requests welcome. Preferred workflow:

1. **Fix translations** — edit any `Magento_*.csv` or `Shubo_*.csv` directly and open a PR. Each row is `"source","georgian"`.
2. **Extend dictionary** — add entries to the `DICT` map in `_translate.py`, then run `python3 _translate.py` to regenerate CSVs and commit both.
3. **Placeholder safety** — preserve `%1`, `%2`, `%s`, `%d` in translations. The validator flags missing placeholders.

### Local validation

```bash
# Regenerate translations
python3 _translate.py

# Validate the language pack against a dev Magento 2.4.8 install
composer require shubo/language-pack-ka-ge:dev-main --no-update \
  --with-all-dependencies
bin/magento setup:upgrade
bin/magento setup:static-content:deploy ka_GE
```

### Style guide

- Use standard Georgian ecommerce vocabulary (mymarket.ge / extra.ge conventions where established).
- Keep UI labels short — Georgian ~1.4× English character count; reserve screen real estate.
- Preserve sentence casing (Magento ships mostly Sentence case).
- Formal register (`თქვენ`, not `შენ`) for all customer-facing strings.

---

## Changelog

See [CHANGELOG.md](./CHANGELOG.md).

## License

[MIT](./LICENSE) — free to fork, embed, and redistribute. No CLA required.

## Credits

Built by [Shubo](https://duka.ge) for the Georgian SME marketplace [duka.ge](https://duka.ge). Contributions from the Georgian Magento community are welcome.
