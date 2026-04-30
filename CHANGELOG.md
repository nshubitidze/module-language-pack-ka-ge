# Changelog

All notable changes to `shubo/language-pack-ka-ge` are documented here. This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] — 2026-05-01

### Changed

- **Vendor namespace realigned to `shubo/`** — composer package name renamed from `shubodev/language-pack-ka-ge` to `shubo/language-pack-ka-ge` to match the canonical Shubo vendor namespace used by all other public modules (`shubo/module-tbc-payment`, `shubo/module-bog-payment`, `shubo/module-shipping-core`, `shubo/module-shipping-shippo`). No code or translation content changed. Not yet on Packagist, so no live consumers are affected.

## [1.0.1] — 2026-04-26

### Fixed

- **[MEDIUM] Hardcoded-bilingual pattern removed from 5 merchant/payout email templates** — `Shubo_MerchantProvisioning::merchant_suspension_{notice,reminder}.html`, `merchant_access_revoked.html`, `Shubo_Payout::settlement_{invoice,reminder}.html` previously inlined both English and Georgian on every line (`{{trans "English"}} / hardcoded Georgian`). Added 24 rows under `Shubo_MerchantProvisioning` scope and 15 rows under `Shubo_Payout` scope to `ka_GE.csv`; removed inline Georgian strings from all 5 templates. Magento's translation pipeline now drives locale selection correctly; the duplicate-render bug (Georgian twice when CSV is populated) is resolved.

## [1.0.0] — 2026-04-26

### Fixed

- **[HIGH] `%name,` placeholder broken in 22 transactional emails** — 6 CSV rows under `Magento_Customer`, `Magento_ProductAlert`, `Magento_Sales`, `Magento_SendFriend`, `Magento_Theme`, `Magento_User` were translating `%name` to `%სახელი`, causing Magento's positional substitution to emit the literal token instead of the customer's first name. Changed all six to `"%name,","%name,"`.
- **[HIGH] `Shubo_MerchantProvisioning::merchant_welcome.html` rendered 100% English to Georgian merchants** — added 13 missing rows to `ka_GE.csv` under `Shubo_MerchantProvisioning` scope: greeting with `%company_name`, approval body copy, section headings (`Your Admin Credentials`, `Getting Started`), table labels (`Admin Panel URL`, `Storefront URL`), security warning, all 5 ordered-list steps, and closing support line. Subject line was also hardcoded English — wrapped in `{{trans "…"}}` and added corresponding CSV row.
- **[MEDIUM] `Shipping Info` heading rendered English** — added `"Shipping Info","მიწოდების ინფორმაცია","module","Magento_Sales"` to fix the mixed-language Billing/Shipping two-column block in order/shipment/invoice/credit-memo emails.
- **[MEDIUM] Conditional contact-block snippets untranslated** — added `or call us at <a href="tel:%store_phone">%store_phone</a>` and `Our hours are <span class="no-link">%store_hours</span>.` under `Magento_Sales`; previously dormant (store phone/hours not configured on duka.ge) but would have leaked English the moment either field was populated.

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

[Unreleased]: https://github.com/nshubitidze/module-language-pack-ka-ge/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/nshubitidze/module-language-pack-ka-ge/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/nshubitidze/module-language-pack-ka-ge/compare/v1.0.0-rc...v1.0.0
[0.1.0-alpha]: https://github.com/nshubitidze/module-language-pack-ka-ge/releases/tag/v0.1.0-alpha

## [1.0.0-RC1] — 2026-04-26

### Added

- **Production-quality translation pass**: 15,276 strings across 201 modules translated into native Georgian via structured translation pipeline with 4-pass quality review.
- **92% overall coverage** (up from 12% in 0.1.0-alpha); 97.7% on P1 storefront-visible modules.
- Full parity with Mageplaza de_DE structural reference: same key set, same module coverage.
- Georgian style guide at `docs/style-guide.md`: formal `თქვენ` register, brand preservation rules, canonical term table, anti-patterns, placeholder fidelity rules.
- Coverage report at `docs/coverage-report.md`: per-module breakdown, acceptance gates.
- 4-pass quality review (`docs/review-spot-check.md`): 91% pass rate from independent Tbilisi-shopper reviewer.
- `docs/reviewer-signoff.md`: formal APPROVE from automated reviewer.
- `README.ka.md`: Georgian-language installation guide.

### Fixed

- `გაგზავნა` (verbal noun "sending") incorrectly used for "shipment" noun — replaced with `გზავნილი` throughout Sales module.
- `ელემენტი` replaced with `ნივთი` for shopping cart/wishlist user-facing strings.
- Newsletter `ნიუსლეტერი` anglicism replaced with `სიახლეების გამოწერა`.
- `კრედიტ-მემო` standardized to `საკრედიტო მემო` throughout.
- "Back to Sign In" → `შესვლის გვერდზე დაბრუნება` (correct locative).

### Changed

- Single monolithic CSV (`ka_GE.csv`) with 4-column format: English, Georgian, "module", ModuleName.
- `composer.json` name updated to `shubodev/language-pack-ka-ge` (Packagist vendor namespace).

[1.0.0-RC1]: https://github.com/nshubitidze/module-language-pack-ka-ge/releases/tag/v1.0.0-rc
