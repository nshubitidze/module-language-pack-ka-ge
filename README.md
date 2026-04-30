# Magento 2 Georgian Language Pack (`ka_GE`)

**First public Georgian (ka_GE) language pack for Magento 2.4.x.** ~92% native-quality translations, Mageplaza de_DE structural parity. MIT licensed.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Magento](https://img.shields.io/badge/Magento-2.4.x-8a2be2.svg)](https://magento.com)
[![Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen.svg)](./docs/coverage-report.md)
[![Packagist](https://img.shields.io/badge/packagist-shubo%2Flanguage--pack--ka--ge-orange.svg)](https://packagist.org/packages/shubo/language-pack-ka-ge)

---

## Why this exists

No public Georgian language pack for Magento 2 existed before this one. Georgian merchants using Magento 2 had to run their stores in English or Russian. This pack provides native-quality Georgian (`ka_GE`) translations for all Magento 2.4.x core modules, maintained by [duka.ge](https://duka.ge) — a Georgian SME marketplace built on Magento 2.

Coverage: **15,276 translation strings across 201 modules**, 92% translated, 97.7% on P1 storefront-visible modules (Catalog, Checkout, Customer, Sales, Payment, Theme, Email, Wishlist, Newsletter, Review, Search, CMS).

---

## Installation (Composer — recommended)

```bash
composer require shubo/language-pack-ka-ge
bin/magento setup:upgrade
bin/magento setup:static-content:deploy ka_GE -f
bin/magento config:set general/locale/code ka_GE --scope=stores --scope-code=default
bin/magento cache:flush
```

Per-store in multi-store setups:
```bash
bin/magento config:set general/locale/code ka_GE --scope=stores --scope-code=<store-code>
```

Or via Admin: **Stores → Configuration → General → Locale Options → Locale = Georgian (Georgia)**.

---

## Installation (manual)

1. Download and extract to `app/i18n/Shubo/ka_GE/`
2. Run:
   ```bash
   bin/magento setup:upgrade
   bin/magento setup:static-content:deploy ka_GE -f
   bin/magento cache:flush
   ```

---

## Coverage

| Tier | Coverage |
|------|----------|
| **Overall** (15,276 strings, 201 modules) | **92%** |
| **P1 storefront** (Catalog, Checkout, Customer, Sales, Payment, Paypal, Theme, Email, Wishlist, Newsletter, Review, Search, CMS, Cookie, Tax, Shipping) | **97.7%** |

Full per-module table: [docs/coverage-report.md](./docs/coverage-report.md)

---

## Contributing

We welcome corrections from native Georgian speakers. Before submitting a PR, please read the [translation style guide](./docs/style-guide.md). The key rules:

- Formal `თქვენ` register for all customer-facing strings (not `შენ`)
- Brand names in English: `PayPal`, `Magento`, `FedEx` — never transliterated
- Use `ელ. ფოსტა` (not `ემაილი`), `შეცდომა` (not `ერორი`), `შესვლა` (not `ლოგინი`)
- All `%1`, `%2`, `{{var ...}}` placeholders must appear identically in the translation

**Reporting wrong translations:** open a [GitHub Issue](https://github.com/nshubitidze/module-language-pack-ka-ge/issues) with the English source string, current Georgian translation, and your suggested correction.

---

## About duka.ge

This pack is maintained by **[duka.ge](https://duka.ge)** — a Georgian SME marketplace built on Magento 2. We open-source our localization work to help other Georgian Magento merchants. For questions, please [open a GitHub Issue](https://github.com/nshubitidze/module-language-pack-ka-ge/issues).

---

## License

[MIT](./LICENSE) — free to use, modify, and distribute.

---

## Credits

- Structural reference: [Mageplaza magento-2-german-language-pack](https://github.com/mageplaza/magento-2-german-language-pack)
- Maintained by [Shubo / duka.ge](https://duka.ge)
