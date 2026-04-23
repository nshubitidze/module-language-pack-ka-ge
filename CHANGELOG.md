# Changelog

All notable changes to `shubo/language-pack-ka-ge` are documented here. This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0-alpha] — 2026-04-23

### Added

- Initial seed: Georgian (`ka_GE`) translations for Magento 2.4.8+.
- ~1,680 translated rows across 120+ module CSVs, generated from `bin/magento i18n:collect-phrases --magento` output via a curated ~500-term Georgian UI dictionary.
- **P1 (human-reviewed) modules** — storefront + checkout + Shubo marketplace modules: `Magento_Catalog`, `Magento_Checkout`, `Magento_Customer`, `Magento_Cms`, `Magento_Theme`, `Magento_Sales`, `Magento_OfflinePayments`, `Magento_Payment`, `Magento_Shipping`, `Magento_Tax`, `Magento_Ui`, `Magento_Wishlist`, `Magento_Review`, `Magento_SalesRule`, `Magento_Quote`, `Magento_GiftMessage`, `Magento_Newsletter`, `Magento_Contact`, `Magento_ProductAlert`, `Magento_Search`, `Magento_CatalogSearch`, `Magento_Directory`, `Shubo_TbcPayment`, `Shubo_BogPayment`, `Shubo_Merchant`, `Shubo_ShippingCore`, `Shubo_Tax`, `Shubo_Commission`, `Shubo_Payout`, `Shubo_CookieConsent`, `Shubo_MerchantCatalog`.
- **Auto-backfill modules** — admin/B2B/dev-tooling modules with shared-dictionary auto-matches only (`Magento_Backend`, `Magento_Reports`, `Magento_Integration`, `Magento_User`, `Magento_ImportExport`, `Magento_Config`, `Magento_Eav`, etc.). These need a human pass; scheduled for 0.2.0.
- Rows without a dictionary hit are **omitted** from output CSVs — Magento falls back to the English source, safer than shipping wrong Georgian.
- `registration.php`, `language.xml` (`code=ka_GE`, `vendor=Shubo`, `package=ka_GE`), `composer.json` (`type=magento2-language`, MIT).

### Known Limitations

- Admin UI strings are predominantly un-translated in 0.1.0. Planned for 0.2.0.
- TBC/BOG payment-config labels (admin-only HTML-embedded strings) are ~5% translated; those admin configuration screens remain largely English until 0.2.0.
- Total source-phrase coverage is ~12%. This is by design (omit-unknown > wrong-translation).

[Unreleased]: https://github.com/nshubitidze/module-language-pack-ka-ge/compare/v0.1.0-alpha...HEAD
[0.1.0-alpha]: https://github.com/nshubitidze/module-language-pack-ka-ge/releases/tag/v0.1.0-alpha
