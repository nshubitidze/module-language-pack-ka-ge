# ka_GE Style Guide — Magento 2 Language Pack

Authoritative ruleset for the `ka_GE.csv` translation pass. Every row MUST conform.
Reviewer enforces; linter checks placeholders.

## 1. Register & tone

- Customer-facing UI: formal `თქვენ` / `გთხოვთ` / `გმადლობთ`. Never `შენ` on storefront,
  checkout, account, or transactional emails. (Mirrors uk_UA pack's `Ви` register.)
- Admin UI: formal but direct. Imperative (`შეინახეთ`) and noun (`შენახვა`) forms both
  accepted; pick ONE per CSV file and stay consistent.
- Errors: factual + empathetic. No Latinized loanwords — `ერორი` is forbidden; use
  `შეცდომა`. `An error occurred` -> `მოხდა შეცდომა`.
- Primary CTA buttons: noun form per canon (`კალათაში დამატება`, `შენახვა`, `გაუქმება`).
  Imperative form reserved for transactional emails.
- Empty states: short, helpful, never scolding. `No items found` -> `ელემენტები ვერ
  მოიძებნა`. Avoid bare `არ არის` except where canon mandates (`N/A`).
- Do not add exclamation marks or emoji absent from the source.

## 2. Brand & proper-noun preservation

ALWAYS keep verbatim English (case-sensitive): Magento, Adobe, PayPal, Braintree,
Stripe, Klarna, Authorize.Net, Apple Pay, Google Pay, Amazon Pay, Amazon, eBay,
FedEx, UPS, DHL, USPS, ElasticSearch, OpenSearch, MySQL, MariaDB, Redis, RabbitMQ,
Varnish, GraphQL, REST, SOAP, AJAX, JSON, XML, YAML, CSV, PDF, HTML, CSS, JS, HTTP,
HTTPS, URL, URI, API, SKU, UPC, EAN, ISBN, IBAN, BIC, SWIFT, IP, GPS, OAuth, OAuth2,
JWT, GDPR, CAPTCHA, reCAPTCHA, TBC, BOG, Flitt, Shippo, Wolt. ALSO verbatim: any
`Magento_*` / `Shubo_*` token, ACL nodes (`*::*`), methods (`name()`), file paths
(`*.php`), anything inside backticks, any mixed-case no-space identifier.

TRANSLATE the prose around the brand: `PayPal payment failed` ->
`PayPal-ით გადახდა ვერ მოხერხდა`. Georgian case enclitics attach to Latin tokens with
a hyphen (`PayPal-ით`, `Magento-ს`).

Currency: keep source `$`, `USD`, `EUR`, `GBP`, `GEL` verbatim; `₾` only if source uses
it; `Georgian Lari` -> `ქართული ლარი`. Numbers: comma decimal `1,50`, space thousands
`1 250`. Dates: `dd.mm.yyyy`. Times: `HH:mm`. Never reformat numbers inside `{{var}}`.

## 3. Canonical translations (mandatory)

Match case-insensitively, trim trailing whitespace before match, preserve trailing
punctuation in output.

| English | Georgian | Notes |
|---|---|---|
| Add to Cart | კალათაში დამატება | noun-form canon |
| Remove | წაშლა | |
| Remove item | ელემენტის წაშლა | |
| Update Cart | კალათის განახლება | |
| Empty Cart | კალათის დაცარიელება | |
| Shopping Cart | საყიდლების კალათა | |
| My Cart | ჩემი კალათა | |
| Checkout | შეკვეთის გაფორმება | |
| Proceed to Checkout | შეკვეთის გაფორმებაზე გადასვლა | |
| Continue Shopping | შოპინგის გაგრძელება | |
| Sign In / Login | შესვლა | |
| Sign Out | გასვლა | |
| Sign Up / Register | რეგისტრაცია | |
| Create an Account | ანგარიშის შექმნა | |
| My Account | ჩემი ანგარიში | |
| Account Information | ანგარიშის ინფორმაცია | |
| Forgot Your Password? | პაროლი დაგავიწყდა? | |
| Reset Password | პაროლის აღდგენა | |
| Change Password | პაროლის შეცვლა | |
| Address Book | მისამართების წიგნი | |
| Newsletter / Newsletter Subscription | სიახლეების გამოწერა | |
| Order / Orders | შეკვეთა / შეკვეთები | |
| My Orders | ჩემი შეკვეთები | |
| Order Status | შეკვეთის სტატუსი | |
| Order Details | შეკვეთის დეტალები | |
| Order Information | შეკვეთის ინფორმაცია | |
| Order History | შეკვეთების ისტორია | |
| Order Date / Order Total / Order Number | შეკვეთის თარიღი / ჯამი / ნომერი | |
| Place Order | შეკვეთის განთავსება | |
| Reorder | შეკვეთის განმეორება | |
| Track Order | შეკვეთის თვალყურის დევნება | |
| Subtotal | ქვეჯამი | |
| Tax | გადასახადი | |
| VAT | დღგ | |
| Shipping | მიწოდება | |
| Shipping & Handling | მიწოდება და დამუშავება | |
| Shipping Address | მიწოდების მისამართი | |
| Shipping Method | მიწოდების მეთოდი | |
| Billing Address | ანგარიშსწორების მისამართი | |
| Payment Method | გადახდის მეთოდი | |
| Grand Total | საერთო ჯამი | |
| Total | სულ | column/label |
| Discount | ფასდაკლება | |
| Coupon Code | კუპონის კოდი | |
| Apply | გამოყენება | |
| Apply Discount Code | ფასდაკლების კოდის გამოყენება | |
| Cancel | გაუქმება | |
| Product / Products | პროდუქტი / პროდუქტები | |
| In Stock | მარაგშია | |
| Out of Stock | მარაგში არ არის | |
| Add to Wish List / Wishlist | სასურველთა სიაში დამატება | |
| Add to Compare | შესადარებლად დამატება | |
| Quantity / Qty | რაოდენობა | |
| Price | ფასი | |
| Special Price | სპეციალური ფასი | |
| Review / Reviews | მიმოხილვა / მიმოხილვები | |
| Rating | შეფასება | |
| Description / Specifications | აღწერა / მახასიათებლები | |
| Related Products | მსგავსი პროდუქტები | |
| Save | შენახვა | |
| Delete | წაშლა | |
| Edit | რედაქტირება | |
| View | ნახვა | |
| Search | ძებნა | |
| Submit / Continue | გაგზავნა / გაგრძელება | |
| Back / Next / Previous | უკან / შემდეგი / წინა | |
| Close / Open | დახურვა / გახსნა | |
| Yes / No | დიახ / არა | |
| OK | კარგი | |
| Loading... | იტვირთება... | preserve ellipsis |
| Please wait | გთხოვთ, დაელოდოთ | |
| Thank you | გმადლობთ | |
| Welcome | მოგესალმებით | |
| Required / Invalid | სავალდებულო / არასწორი | |
| This is a required field. | ეს ველი სავალდებულოა. | |
| Please try again | გთხოვთ, სცადოთ ხელახლა | |
| Something went wrong. | რაღაც შეცდომა მოხდა. | preserve period |
| N/A | არ არის | legacy canon |
| None / All / Other | არცერთი / ყველა / სხვა | |
| No items found | ელემენტები ვერ მოიძებნა | |
| No results | შედეგები ვერ მოიძებნა | |

## 4. What stays English (no translation)

- HTML tags, attribute names, attribute values that look like CSS classes/IDs/data-attrs.
- Email markup: `{{var ...}}`, `{{trans "..."}}`, `{{depend ...}}`, `{{block ...}}`,
  `{{layout ...}}`, `{{config path="..."}}`, `{{store url="..."}}` — verbatim incl. whitespace.
- Module/class/method/event names embedded in strings.
- Developer-only strings (`var/log/exception.log` errors, debug strings).
- Sample/fixture text (`Lorem ipsum`, `TEST_TEXT`, `foo`, `bar`).
- Currency codes as codes (`USD`, `EUR`, `GEL`); ISO country codes (`US`, `DE`, `GE`).
  Country full names DO translate: `United States` -> `ამერიკის შეერთებული შტატები`,
  `Georgia` -> `საქართველო`.
- Strings that are 100% punctuation, numbers, or a single ASCII token; single chars.

## 5. Anti-patterns (reject)

| Wrong | Right | Why |
|---|---|---|
| ერორი მოხდა | მოხდა შეცდომა | Latinized loanword; use native `შეცდომა` |
| ემაილი | ელ. ფოსტა | Latinized; use native form |
| ფეიფალი / მაჟენტო | PayPal / Magento | brand transliteration forbidden |
| ლოგინი | შესვლა | use native verb noun |
| ძიება შედეგები | ძიების შედეგები | broken case; needs genitive `-ის` |
| შენახვა-ის შეკვეთა | შეკვეთის შენახვა | word-by-word machine output |
| გადატვირთვა (for `Reload`) | განახლება | Russian calque from `перезагрузка` |
| Save Sheqveta (Latin) | შეკვეთის შენახვა | Latin transliteration of Georgian |
| შენახ-Magento | Magento-ს შენახვა | mixed-script word; brand stays separate |

## 6. Placeholder fidelity (linter-enforced)

- Every `%1..%N`, `%s`, `%d` appears in translation with identical count and labels.
- Every `{{var x}}`, `{{trans "x"}}`, `{{depend x}}`, `{{block ...}}`, `{{layout ...}}`
  round-trips with identical brace count and inner content.
- HTML tags (`<a>`, `</a>`, `<strong>`, `<br>`, `<br/>`, `<span class="...">`, `<em>`,
  `<b>`, `<i>`, `<u>`, `<p>`) round-trip with identical attributes.
- Leading/trailing whitespace preserved byte-for-byte (trailing-space sentinel in
  `"Order # "`). Trailing punctuation preserved: `:` `.` `?` `!` `…` `...`.
- Source `"..."` stays `"..."`, source `'...'` stays `'...'`. If source starts
  uppercase, do not prepend a lowercase particle in the translation.

## 7. Pluralization

- Georgian uses one plural form `-ები` (e.g. `პროდუქტი` -> `პროდუქტები`).
- After numeric quantifiers Georgian keeps the SINGULAR: `1 პროდუქტი`, `5 პროდუქტი`,
  `100 პროდუქტი`. This is correct, not a duplicate-row bug — linter must not flag
  identical singular/plural translations when both source rows contain `%1`/`%d`.
- Canon: `1 item` / `%1 items` -> `1 ელემენტი` / `%1 ელემენტი`. Without a numeric
  quantifier, use the explicit plural: `Items` -> `ელემენტები`.

## 8. Honorifics & politeness

- `Welcome` / `Welcome, %1` -> `მოგესალმებით` / `მოგესალმებით, %1`.
- `Hello %1` (email) -> `გამარჯობათ, %1` (formal-plural; bare `გამარჯობა` is informal).
- `Please` sentence-initial -> `გთხოვთ,` always followed by a comma.
- `Thank you` / `Thanks` -> `გმადლობთ`. `Dear %1` -> `ძვირფასო %1`.
- `Sincerely` / `Best regards` -> `პატივისცემით`.

## 9. Module-specific guidance

| Module | Tone & vocabulary |
|---|---|
| Magento_Catalog | Shopping vocab; noun-form CTAs on product listings. |
| Magento_Sales | Order/invoice/credit-memo terms; preserve `Order #` spacing. |
| Magento_Customer | Account/auth terms; formal welcome (`მოგესალმებით`). |
| Magento_Checkout | Short, action-oriented; noun-form CTAs per canon. |
| Magento_Paypal | Keep `PayPal` English; translate surrounding prose. |
| Magento_Shipping | Address vocab; carriers (`FedEx`, `UPS`, `DHL`) stay English. |
| Magento_Email | Friendly + formal; preserve every `{{var}}` / `{{trans}}` / `{{depend}}`. |
| Magento_Theme / Cms | Short labels (Theme); page-content prose stays formal (Cms). |
| Magento_Newsletter | Marketing tone but formal `თქვენ`; CTA = `გამოიწერეთ`. |
| Magento_Wishlist | Short labels; `Wish List` = `სასურველთა სია`. |
| Magento_Review | Legacy informal `დაწერე პირველი მიმოხილვა` is a canon exception. |
