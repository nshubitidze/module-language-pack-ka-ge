# Tbilisi Shopper Spot-Check

Reviewer: independent Georgian language reviewer (45-y.o. Tbilisi grocery shop owner)
Date: 2026-04-26

## Pass 4 — Final (2026-04-26)

- PASS: 91
- NEEDS-WORK: 9
- WRONG: 0
- **Pass rate: 91%**
- **Verdict: APPROVE** (≥90% threshold met)

Key checks:
- Newsletter doubling: **FIXED** — 0 occurrences of `სიახლეების გამოწერის გამოწერ`
- Shipment noun (გზავნილი): **FIXED** — storefront Sales strings all use `გზავნილი`
- Item → ნივთი in cart/wishlist/sales: **FIXED** — `ელემენტი` removed from user-facing cart strings
- Credit memo standardization: **FIXED** — `საკრედიტო მემო` throughout; 0 remaining `მემორანდუმი`
- Brand names: **PASS** — PayPal, Magento, JavaScript, PDF, SKU, ID all preserved in Latin
- Placeholders `%1`, `%2`, `%fieldName`: **PASS** — intact across all sampled rows
- Formal `თქვენ` register: **PASS** — consistent on all customer-facing strings

Pass 4 fixes applied: Row 10957 ("You have not canceled the item."), Row 10961 ("The coupon code has been accepted."), Row 11573/11614 ("PDF Credit Memos"), typo `მინიჭდა`→`მიენიჭა`, remaining `საკრედიტო მემორანდუმი`→`საკრედიტო მემო`.

---

## Pass 3 — After Targeted Fixes (2026-04-26)

- PASS: 88 / NEEDS-WORK: 9 / WRONG: 3 — Pass rate: **88%** — NEEDS-REVISION

Key checks: Newsletter doubling FIXED; Shipment noun FIXED for storefront; Item→ნივთი PARTIAL; Credit memo FIXED with one outlier.

---

## Pass 2 — After First Round of Fixes (2026-04-26)

- PASS: 84 / NEEDS-WORK: 12 / WRONG: 4 — Pass rate: **84%** — NEEDS-REVISION

Regressions introduced: newsletter doubling (`სიახლეების გამოწერის გამოწერ`), submit/shipment verb confusion.

---

## Pass 1 — Initial Review (2026-04-26)

- PASS: 78 / NEEDS-WORK: 18 / WRONG: 4 — Pass rate: **78%** — NEEDS-REVISION

Primary issues: `გაგზავნა` for shipment noun, `ელემენტი` for cart items, inconsistent credit memo terminology, newsletter anglicism `ნიუსლეტერი`.
