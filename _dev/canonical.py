"""Canonical translation dictionary and pattern templates for ka_GE pack.

Source of truth: docs/style-guide.md sections 3, 7, 8.
Additional safe-everywhere entries appended below.
Mkhedruli only. Trailing punctuation handling is done by the caller.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# CANONICAL: exact-match (case-sensitive) English source -> Georgian.
# Trailing whitespace/punctuation is stripped before lookup; punctuation is
# re-attached on output by the caller.
# ---------------------------------------------------------------------------

CANONICAL: dict[str, str] = {
    # --- Style guide section 3 (canon, mandatory) ---
    "Add to Cart": "კალათაში დამატება",
    "Remove": "წაშლა",
    "Remove item": "ელემენტის წაშლა",
    "Update Cart": "კალათის განახლება",
    "Empty Cart": "კალათის დაცარიელება",
    "Shopping Cart": "საყიდლების კალათა",
    "My Cart": "ჩემი კალათა",
    "Cart": "კალათა",
    "Checkout": "შეკვეთის გაფორმება",
    "Proceed to Checkout": "შეკვეთის გაფორმებაზე გადასვლა",
    "Continue Shopping": "შოპინგის გაგრძელება",
    "Sign In": "შესვლა",
    "Login": "შესვლა",
    "Log In": "შესვლა",
    "Log in": "შესვლა",
    "Sign Out": "გასვლა",
    "Log Out": "გასვლა",
    "Logout": "გასვლა",
    "Sign Up": "რეგისტრაცია",
    "Register": "რეგისტრაცია",
    "Create an Account": "ანგარიშის შექმნა",
    "Create Account": "ანგარიშის შექმნა",
    "My Account": "ჩემი ანგარიში",
    "Account": "ანგარიში",
    "Account Information": "ანგარიშის ინფორმაცია",
    "Forgot Your Password?": "პაროლი დაგავიწყდა?",
    "Forgot Password?": "პაროლი დაგავიწყდა?",
    "Forgot Password": "პაროლი დაგავიწყდა",
    "Reset Password": "პაროლის აღდგენა",
    "Change Password": "პაროლის შეცვლა",
    "Address Book": "მისამართების წიგნი",
    "Newsletter": "სიახლეების გამოწერა",
    "Newsletter Subscription": "სიახლეების გამოწერა",
    "Order": "შეკვეთა",
    "Orders": "შეკვეთები",
    "My Orders": "ჩემი შეკვეთები",
    "Order Status": "შეკვეთის სტატუსი",
    "Order Details": "შეკვეთის დეტალები",
    "Order Information": "შეკვეთის ინფორმაცია",
    "Order History": "შეკვეთების ისტორია",
    "Order Date": "შეკვეთის თარიღი",
    "Order Total": "შეკვეთის ჯამი",
    "Order Number": "შეკვეთის ნომერი",
    "Place Order": "შეკვეთის განთავსება",
    "Reorder": "შეკვეთის განმეორება",
    "Track Order": "შეკვეთის თვალყურის დევნება",
    "Subtotal": "ქვეჯამი",
    "Tax": "გადასახადი",
    "VAT": "დღგ",
    "Shipping": "მიწოდება",
    "Shipping & Handling": "მიწოდება და დამუშავება",
    "Shipping Address": "მიწოდების მისამართი",
    "Shipping Method": "მიწოდების მეთოდი",
    "Billing Address": "ანგარიშსწორების მისამართი",
    "Payment Method": "გადახდის მეთოდი",
    "Grand Total": "საერთო ჯამი",
    "Total": "სულ",
    "Discount": "ფასდაკლება",
    "Coupon Code": "კუპონის კოდი",
    "Apply": "გამოყენება",
    "Apply Discount Code": "ფასდაკლების კოდის გამოყენება",
    "Cancel": "გაუქმება",
    "Product": "პროდუქტი",
    "Products": "პროდუქტები",
    "In Stock": "მარაგშია",
    "Out of Stock": "მარაგში არ არის",
    "Add to Wish List": "სასურველთა სიაში დამატება",
    "Add to Wishlist": "სასურველთა სიაში დამატება",
    "Add to Compare": "შესადარებლად დამატება",
    "Quantity": "რაოდენობა",
    "Qty": "რაოდენობა",
    "Price": "ფასი",
    "Special Price": "სპეციალური ფასი",
    "Review": "მიმოხილვა",
    "Reviews": "მიმოხილვები",
    "Rating": "შეფასება",
    "Description": "აღწერა",
    "Specifications": "მახასიათებლები",
    "Related Products": "მსგავსი პროდუქტები",
    "Save": "შენახვა",
    "Delete": "წაშლა",
    "Edit": "რედაქტირება",
    "View": "ნახვა",
    "Search": "ძებნა",
    "Submit": "გაგზავნა",
    "Continue": "გაგრძელება",
    "Back": "უკან",
    "Next": "შემდეგი",
    "Previous": "წინა",
    "Close": "დახურვა",
    "Open": "გახსნა",
    "Yes": "დიახ",
    "No": "არა",
    "OK": "კარგი",
    "Loading...": "იტვირთება...",
    "Loading…": "იტვირთება…",
    "Loading": "იტვირთება",
    "Please wait": "გთხოვთ, დაელოდოთ",
    "Please wait...": "გთხოვთ, დაელოდოთ...",
    "Thank you": "გმადლობთ",
    "Thanks": "გმადლობთ",
    "Welcome": "მოგესალმებით",
    "Required": "სავალდებულო",
    "Invalid": "არასწორი",
    "This is a required field.": "ეს ველი სავალდებულოა.",
    "Please try again": "გთხოვთ, სცადოთ ხელახლა",
    "Please try again.": "გთხოვთ, სცადოთ ხელახლა.",
    "Something went wrong.": "რაღაც შეცდომა მოხდა.",
    "Something went wrong": "რაღაც შეცდომა მოხდა",
    "N/A": "არ არის",
    "None": "არცერთი",
    "All": "ყველა",
    "Other": "სხვა",
    "No items found": "ელემენტები ვერ მოიძებნა",
    "No results": "შედეგები ვერ მოიძებნა",
    "An error occurred": "მოხდა შეცდომა",
    "An error occurred.": "მოხდა შეცდომა.",
    "Hello": "გამარჯობათ",
    "Goodbye": "ნახვამდის",
    # --- Generic UI verbs / buttons (safe everywhere) ---
    "Add": "დამატება",
    "Update": "განახლება",
    "Submit Form": "ფორმის გაგზავნა",
    "Reset": "გადატვირთვა",
    "Refresh": "განახლება",
    "Reload": "განახლება",
    "Print": "ბეჭდვა",
    "Export": "ექსპორტი",
    "Import": "იმპორტი",
    "Copy": "კოპირება",
    "Paste": "ჩასმა",
    "Move": "გადატანა",
    "Send": "გაგზავნა",
    "Receive": "მიღება",
    "Download": "ჩამოტვირთვა",
    "Upload": "ატვირთვა",
    "Browse": "დათვალიერება",
    "Select": "არჩევა",
    "Choose": "არჩევა",
    "Confirm": "დადასტურება",
    "Approve": "დადასტურება",
    "Reject": "უარყოფა",
    "Enable": "ჩართვა",
    "Disable": "გამორთვა",
    "Activate": "გააქტიურება",
    "Deactivate": "დეაქტივაცია",
    "Show": "ჩვენება",
    "Hide": "დამალვა",
    "Toggle": "გადართვა",
    "Expand": "გაშლა",
    "Collapse": "ჩაკეცვა",
    "Sort": "დახარისხება",
    "Filter": "ფილტრი",
    "Group": "ჯგუფი",
    "Help": "დახმარება",
    "Settings": "პარამეტრები",
    "Options": "ვარიანტები",
    "Preferences": "პარამეტრები",
    "Profile": "პროფილი",
    # --- Status words ---
    "Active": "აქტიური",
    "Inactive": "არააქტიური",
    "Enabled": "ჩართულია",
    "Disabled": "გამორთულია",
    "Pending": "მოლოდინში",
    "Approved": "დადასტურებული",
    "Rejected": "უარყოფილი",
    "Cancelled": "გაუქმებული",
    "Canceled": "გაუქმებული",
    "Completed": "დასრულებული",
    "Complete": "დასრულებული",
    "Processing": "მიმდინარეობს",
    "Shipped": "გაგზავნილი",
    "Delivered": "მიწოდებული",
    "Returned": "დაბრუნებული",
    "Refunded": "თანხა დაბრუნდა",
    "Paid": "გადახდილი",
    "Unpaid": "გადაუხდელი",
    "Closed": "დახურული",
    "Draft": "მონახაზი",
    "Published": "გამოქვეყნებული",
    "Available": "ხელმისაწვდომი",
    "Unavailable": "მიუწვდომელი",
    # --- Form labels ---
    "Name": "სახელი",
    "Title": "სათაური",
    "Comments": "კომენტარები",
    "Comment": "კომენტარი",
    "Notes": "შენიშვნები",
    "Note": "შენიშვნა",
    "Date": "თარიღი",
    "Time": "დრო",
    "Created At": "შექმნის თარიღი",
    "Updated At": "განახლების თარიღი",
    "Modified At": "შეცვლის თარიღი",
    "Last Modified": "ბოლო ცვლილება",
    "Created By": "შემქმნელი",
    "Updated By": "განმაახლებელი",
    "Status": "სტატუსი",
    "Type": "ტიპი",
    "Category": "კატეგორია",
    "Tag": "ტეგი",
    "Tags": "ტეგები",
    "Position": "პოზიცია",
    "Weight": "წონა",
    "Dimensions": "ზომები",
    "SKU": "SKU",
    "Stock": "მარაგი",
    # --- Account form fields ---
    "Email": "ელ. ფოსტა",
    "Email Address": "ელ. ფოსტის მისამართი",
    "Password": "პაროლი",
    "First Name": "სახელი",
    "Last Name": "გვარი",
    "Date of Birth": "დაბადების თარიღი",
    "Gender": "სქესი",
    "Telephone": "ტელეფონი",
    "Phone": "ტელეფონი",
    "Phone Number": "ტელეფონის ნომერი",
    "Fax": "ფაქსი",
    "Address": "მისამართი",
    "Country": "ქვეყანა",
    "State": "შტატი",
    "Region": "რეგიონი",
    "City": "ქალაქი",
    "Zip": "საფოსტო ინდექსი",
    "ZIP": "საფოსტო ინდექსი",
    "Postal Code": "საფოსტო ინდექსი",
    "Zip/Postal Code": "საფოსტო ინდექსი",
    "Street": "ქუჩა",
    "Street Address": "ქუჩის მისამართი",
    "Company": "კომპანია",
    "Tax/VAT Number": "გადასახადის/დღგ ნომერი",
    "VAT Number": "დღგ ნომერი",
    # --- Time / period ---
    "Today": "დღეს",
    "Yesterday": "გუშინ",
    "Tomorrow": "ხვალ",
    "This Week": "ამ კვირაში",
    "Last Week": "გასულ კვირაში",
    "Next Week": "შემდეგ კვირაში",
    "This Month": "ამ თვეში",
    "Last Month": "გასულ თვეში",
    "Year": "წელი",
    "Month": "თვე",
    "Day": "დღე",
    "Week": "კვირა",
    "Hour": "საათი",
    "Minute": "წუთი",
    "Second": "წამი",
    # --- Plurals & quantifiers ---
    "Item": "ელემენტი",
    "Items": "ელემენტები",
    "Customer": "მომხმარებელი",
    "Customers": "მომხმარებლები",
    "Page": "გვერდი",
    "Pages": "გვერდები",
    "Result": "შედეგი",
    "Results": "შედეგები",
    "User": "მომხმარებელი",
    "Users": "მომხმარებლები",
    "More": "მეტი",
    "Less": "ნაკლები",
    # --- Common Magento phrases ---
    "Are you sure?": "დარწმუნებული ხართ?",
    "Are you sure you want to do this?": "დარწმუნებული ხართ, რომ ამის გაკეთება გსურთ?",
    "This action cannot be undone": "ეს მოქმედება შეუქცევადია",
    "This action cannot be undone.": "ეს მოქმედება შეუქცევადია.",
    "Please select": "გთხოვთ აირჩიოთ",
    "-- Please Select --": "-- გთხოვთ აირჩიოთ --",
    "Please enter": "გთხოვთ შეიყვანოთ",
    "Choose file": "აირჩიეთ ფაილი",
    "Choose File": "აირჩიეთ ფაილი",
    "No file chosen": "ფაილი არ არის არჩეული",
    "Choose Files": "აირჩიეთ ფაილები",
    "No File": "ფაილი არ არის",
    "Required Fields": "სავალდებულო ველები",
    "Required Field": "სავალდებულო ველი",
    "Optional": "არასავალდებულო",
    "From": "დან",
    "To": "მდე",
    "Action": "მოქმედება",
    "Actions": "მოქმედებები",
    "ID": "ID",
    "Code": "კოდი",
    "Value": "მნიშვნელობა",
    "Default": "ნაგულისხმევი",
    "Custom": "ინდივიდუალური",
    "Save and Continue Edit": "შენახვა და რედაქტირების გაგრძელება",
    "Save and Close": "შენახვა და დახურვა",
    "Save Config": "კონფიგურაციის შენახვა",
    "General": "ზოგადი",
    "Advanced": "გაფართოებული",
    "Information": "ინფორმაცია",
    "Details": "დეტალები",
    "Summary": "მოკლედ",
    "Overview": "მიმოხილვა",
    "Dashboard": "მთავარი პანელი",
    "Reports": "ანგარიშები",
    "Report": "ანგარიში",
    # --- Honorifics (style guide section 8) ---
    "Sincerely": "პატივისცემით",
    "Best regards": "პატივისცემით",
    "Best Regards": "პატივისცემით",
    "Kind regards": "პატივისცემით",
    # --- Errors / messaging ---
    "Error": "შეცდომა",
    "Warning": "გაფრთხილება",
    "Notice": "შეტყობინება",
    "Success": "წარმატება",
    "Failed": "ვერ მოხერხდა",
    "Failure": "შეცდომა",
    "Saved": "შენახულია",
    "Saved.": "შენახულია.",
    "Deleted": "წაშლილია",
    "Updated": "განახლდა",
    "Created": "შეიქმნა",
    # --- Misc storefront ---
    "Compare": "შედარება",
    "Compare Products": "პროდუქტების შედარება",
    "Wishlist": "სასურველთა სია",
    "Wish List": "სასურველთა სია",
    "My Wish List": "ჩემი სასურველთა სია",
    "Special Offers": "სპეციალური შეთავაზებები",
    "New Products": "ახალი პროდუქტები",
    "Featured Products": "გამორჩეული პროდუქტები",
    "Best Sellers": "ბესტსელერები",
    "Categories": "კატეგორიები",
    "Brands": "ბრენდები",
    "Brand": "ბრენდი",
    "Sale": "ფასდაკლება",
    "On Sale": "ფასდაკლებაზე",
    # --- Pagination & lists ---
    "Show More": "მეტის ჩვენება",
    "Show Less": "ნაკლების ჩვენება",
    "Read More": "მეტის წაკითხვა",
    "Read Less": "ნაკლების წაკითხვა",
    "View All": "ყველას ნახვა",
    "View More": "მეტის ნახვა",
    "View Details": "დეტალების ნახვა",
    "Per Page": "გვერდზე",
    "First": "პირველი",
    "Last": "ბოლო",
    "Page Not Found": "გვერდი ვერ მოიძებნა",
    "Not Found": "ვერ მოიძებნა",
    # --- Confirmation phrases ---
    "Are you sure you want to delete this?": "დარწმუნებული ხართ, რომ გსურთ ამის წაშლა?",
    "Saved successfully": "წარმატებით შენახულია",
    "Saved successfully.": "წარმატებით შენახულია.",
    "Deleted successfully": "წარმატებით წაშლილია",
    "Deleted successfully.": "წარმატებით წაშლილია.",
    # --- Currency / lari ---
    "Georgian Lari": "ქართული ლარი",
}


# ---------------------------------------------------------------------------
# PATTERNS: regex templates for compositional phrases.
# Each entry is (pattern, replacement-template-with-\1-placeholder, transform).
# When the captured \1 is itself an English word in CANONICAL, it is replaced
# with the canonical Georgian during application. If \1 is unknown and not a
# whitelisted brand token, the pattern is skipped.
# ---------------------------------------------------------------------------

# Brand/identifier whitelist tokens that pass through unchanged
_BRAND_WHITELIST: frozenset[str] = frozenset({
    "Magento", "PayPal", "Adobe", "Stripe", "Klarna", "Braintree",
    "FedEx", "UPS", "DHL", "USPS", "ElasticSearch", "OpenSearch",
    "MySQL", "MariaDB", "Redis", "RabbitMQ", "Varnish",
    "GraphQL", "REST", "SOAP", "AJAX", "JSON", "XML", "YAML",
    "CSV", "PDF", "HTML", "CSS", "JS", "HTTP", "HTTPS",
    "URL", "URI", "API", "SKU", "UPC", "EAN", "ISBN",
    "IBAN", "BIC", "SWIFT", "IP", "GPS",
    "OAuth", "OAuth2", "JWT", "GDPR", "CAPTCHA", "reCAPTCHA",
    "TBC", "BOG", "Flitt", "Shippo", "Wolt",
    "Apple Pay", "Google Pay", "Amazon Pay", "Authorize.Net",
    "Amazon", "eBay",
})


def _is_brand_token(s: str) -> bool:
    """Return True if s is a whitelisted brand or a Magento_*/Shubo_* token."""
    s = s.strip()
    if s in _BRAND_WHITELIST:
        return True
    if s.startswith("Magento_") or s.startswith("Shubo_"):
        return True
    # single uppercase token like "USPS" caught by whitelist; otherwise reject
    return False


def resolve_token(token: str) -> str | None:
    """Look up English token to Georgian. Return None if unresolvable.

    Tries CANONICAL exact match, then plural-stripped form, then brand whitelist.
    """
    token = token.strip()
    if not token:
        return None
    if token in CANONICAL:
        return CANONICAL[token]
    if _is_brand_token(token):
        return token
    return None


# Patterns are tuples of (compiled regex, builder function).
# The builder receives the regex match and returns the Georgian translation,
# or None if the captured group(s) cannot be resolved.

PatternBuilder = "tuple[re.Pattern[str], object]"


def _to_genitive(noun: str) -> str:
    """Form Georgian genitive (-ის) of a noun.

    Rules (sufficient for our canon vocabulary):
      - Latin brand token (no Mkhedruli letters): append "-ის" with hyphen.
      - Mkhedruli noun ending in "ა" or "ე": drop the final vowel, add "ის".
      - Mkhedruli noun ending in "ი": drop "ი", add "ის".
      - Mkhedruli noun ending in "ო" or "უ": keep, add "ის".
      - Mkhedruli noun ending in any other char (consonant): add "ის".
      - Multi-word phrases: only the LAST word is inflected.
    """
    noun = noun.strip()
    if not noun:
        return noun
    # If it's a Latin brand token (no Georgian letters at all): hyphen-enclitic.
    if not _is_georgian(noun):
        return f"{noun}-ის"
    # Multi-word: inflect last token only.
    if " " in noun:
        head, _, tail = noun.rpartition(" ")
        return f"{head} {_to_genitive(tail)}"
    last = noun[-1]
    if last in ("ა", "ე", "ი"):
        return noun[:-1] + "ის"
    # Consonant or other vowel: append directly.
    return noun + "ის"


# Determiners / pronouns that should NOT be inflected as genitive nouns.
# If a pattern's captured group resolves to one of these, skip the pattern.
_NON_INFLECTABLE: frozenset[str] = frozenset({
    "ყველა",
    "არცერთი",
    "სხვა",
    "ახალი",
    "ჩემი",
    "მეტი",
    "ნაკლები",
    "სავალდებულო",
    "არასწორი",
    "კარგი",
    "დიახ",
    "არა",
    "ნახვამდის",
})


def _build_genitive_action(verb_noun: str):
    """Make a builder that emits '<genitive(\\1)> <verb_noun>' or fallback."""

    def builder(m: re.Match[str]) -> str | None:
        captured = m.group(1).strip()
        resolved = resolve_token(captured)
        if resolved is None:
            return None
        if resolved in _NON_INFLECTABLE:
            return None
        return f"{_to_genitive(resolved)} {verb_noun}"

    return builder


def _build_prefix(prefix: str):
    """Make a builder that emits '<prefix> <resolved \\1>'."""

    def builder(m: re.Match[str]) -> str | None:
        captured = m.group(1).strip()
        resolved = resolve_token(captured)
        if resolved is None:
            return None
        return f"{prefix} {resolved}"

    return builder


def _build_suffix(suffix: str):
    """Make a builder that emits '<resolved \\1> <suffix>'."""

    def builder(m: re.Match[str]) -> str | None:
        captured = m.group(1).strip()
        resolved = resolve_token(captured)
        if resolved is None:
            return None
        return f"{resolved} {suffix}"

    return builder


def _is_georgian(s: str) -> bool:
    """True if string contains any Mkhedruli character."""
    return any("ა" <= ch <= "ჿ" for ch in s)


def _placeholder_passthrough(template: str):
    """Builder that emits template with %1/%2 left intact."""

    def builder(m: re.Match[str]) -> str | None:
        return template

    return builder


PATTERNS: list[tuple[re.Pattern[str], object]] = [
    # Verb-noun forms — captured noun becomes genitive subject
    (re.compile(r"^Save (.+)$"), _build_genitive_action("შენახვა")),
    (re.compile(r"^Edit (.+)$"), _build_genitive_action("რედაქტირება")),
    (re.compile(r"^Delete (.+)$"), _build_genitive_action("წაშლა")),
    (re.compile(r"^Remove (.+)$"), _build_genitive_action("წაშლა")),
    (re.compile(r"^Add (.+)$"), _build_genitive_action("დამატება")),
    (re.compile(r"^Manage (.+)$"), _build_genitive_action("მართვა")),
    (re.compile(r"^View (.+)$"), _build_genitive_action("ნახვა")),
    (re.compile(r"^Create (.+)$"), _build_genitive_action("შექმნა")),
    (re.compile(r"^Update (.+)$"), _build_genitive_action("განახლება")),
    (re.compile(r"^Show (.+)$"), _build_genitive_action("ჩვენება")),
    (re.compile(r"^Hide (.+)$"), _build_genitive_action("დამალვა")),
    (re.compile(r"^Search (.+)$"), _build_genitive_action("ძებნა")),
    (re.compile(r"^Cancel (.+)$"), _build_genitive_action("გაუქმება")),
    (re.compile(r"^Approve (.+)$"), _build_genitive_action("დადასტურება")),
    (re.compile(r"^Reject (.+)$"), _build_genitive_action("უარყოფა")),
    (re.compile(r"^Enable (.+)$"), _build_genitive_action("ჩართვა")),
    (re.compile(r"^Disable (.+)$"), _build_genitive_action("გამორთვა")),
    (re.compile(r"^Print (.+)$"), _build_genitive_action("ბეჭდვა")),
    (re.compile(r"^Export (.+)$"), _build_genitive_action("ექსპორტი")),
    (re.compile(r"^Import (.+)$"), _build_genitive_action("იმპორტი")),
    (re.compile(r"^Download (.+)$"), _build_genitive_action("ჩამოტვირთვა")),
    (re.compile(r"^Upload (.+)$"), _build_genitive_action("ატვირთვა")),
    (re.compile(r"^Submit (.+)$"), _build_genitive_action("გაგზავნა")),
    (re.compile(r"^Send (.+)$"), _build_genitive_action("გაგზავნა")),
    (re.compile(r"^Track (.+)$"), _build_genitive_action("თვალყურის დევნება")),
    # Add new <X> -> ახალი <X>-ის დამატება
    (
        re.compile(r"^Add new (.+)$", re.IGNORECASE),
        (
            lambda m: (
                f"ახალი {_to_genitive(resolve_token(m.group(1).strip()))} დამატება"
                if resolve_token(m.group(1).strip()) is not None
                else None
            )
        ),
    ),
    # Add a <X> -> <X>-ის დამატება
    (
        re.compile(r"^Add a (.+)$"),
        _build_genitive_action("დამატება"),
    ),
    # Prefix forms — adjective in front
    (re.compile(r"^New (.+)$"), _build_prefix("ახალი")),
    (re.compile(r"^All (.+)$"), _build_prefix("ყველა")),
    (re.compile(r"^My (.+)$"), _build_prefix("ჩემი")),
    # No <X> found
    (
        re.compile(r"^No (.+) found\.?$"),
        (
            lambda m: (
                f"{resolve_token(m.group(1).strip())} ვერ მოიძებნა"
                + ("." if m.group(0).endswith(".") else "")
                if resolve_token(m.group(1).strip()) is not None
                else None
            )
        ),
    ),
    # The <X> was saved/deleted/created/updated.
    (
        re.compile(r"^The (.+) was saved\.?$"),
        (
            lambda m: (
                f"{resolve_token(m.group(1).strip())} შენახულია"
                + ("." if m.group(0).endswith(".") else "")
                if resolve_token(m.group(1).strip()) is not None
                else None
            )
        ),
    ),
    (
        re.compile(r"^The (.+) was deleted\.?$"),
        (
            lambda m: (
                f"{resolve_token(m.group(1).strip())} წაშლილია"
                + ("." if m.group(0).endswith(".") else "")
                if resolve_token(m.group(1).strip()) is not None
                else None
            )
        ),
    ),
    (
        re.compile(r"^The (.+) has been saved\.?$"),
        (
            lambda m: (
                f"{resolve_token(m.group(1).strip())} შენახულია"
                + ("." if m.group(0).endswith(".") else "")
                if resolve_token(m.group(1).strip()) is not None
                else None
            )
        ),
    ),
    (
        re.compile(r"^The (.+) has been deleted\.?$"),
        (
            lambda m: (
                f"{resolve_token(m.group(1).strip())} წაშლილია"
                + ("." if m.group(0).endswith(".") else "")
                if resolve_token(m.group(1).strip()) is not None
                else None
            )
        ),
    ),
    # %1-bearing patterns — placeholder must round-trip
    (
        re.compile(r"^%1 is required\.?$"),
        (
            lambda m: "%1 სავალდებულოა" + ("." if m.group(0).endswith(".") else "")
        ),
    ),
    (
        re.compile(r"^Please enter (.+)\.?$"),
        (
            lambda m: (
                f"გთხოვთ შეიყვანოთ {resolve_token(m.group(1).strip().rstrip('.'))}"
                + ("." if m.group(0).rstrip().endswith(".") else "")
                if resolve_token(m.group(1).strip().rstrip(".")) is not None
                else None
            )
        ),
    ),
    (
        re.compile(r"^Please select (.+)\.?$"),
        (
            lambda m: (
                f"გთხოვთ აირჩიოთ {resolve_token(m.group(1).strip().rstrip('.'))}"
                + ("." if m.group(0).rstrip().endswith(".") else "")
                if resolve_token(m.group(1).strip().rstrip(".")) is not None
                else None
            )
        ),
    ),
    (
        re.compile(r"^Are you sure you want to delete (.+)\?$"),
        (
            lambda m: (
                f"დარწმუნებული ხართ, რომ გსურთ {_to_genitive(resolve_token(m.group(1).strip()))} წაშლა?"
                if resolve_token(m.group(1).strip()) is not None
                else None
            )
        ),
    ),
    # Welcome, %1 -> მოგესალმებით, %1
    (
        re.compile(r"^Welcome, %1\.?$"),
        (
            lambda m: "მოგესალმებით, %1" + ("." if m.group(0).endswith(".") else "")
        ),
    ),
    (
        re.compile(r"^Hello %1\.?$"),
        (
            lambda m: "გამარჯობათ, %1" + ("." if m.group(0).endswith(".") else "")
        ),
    ),
    (
        re.compile(r"^Hello, %1\.?$"),
        (
            lambda m: "გამარჯობათ, %1" + ("." if m.group(0).endswith(".") else "")
        ),
    ),
    (
        re.compile(r"^Dear %1\.?$"),
        (
            lambda m: "ძვირფასო %1" + ("." if m.group(0).endswith(".") else "")
        ),
    ),
    (
        re.compile(r"^Dear %1,$"),
        (lambda m: "ძვირფასო %1,"),
    ),
]


def apply_canonical(source: str) -> str | None:
    """Return Georgian translation of source via CANONICAL exact match, or None.

    Trailing punctuation in source is preserved on output. Whitespace around
    the source is preserved verbatim — only the trimmed core is matched.
    """
    if not source:
        return None
    # Capture leading/trailing whitespace
    stripped = source.strip()
    if not stripped:
        return None
    lead_len = len(source) - len(source.lstrip())
    trail_len = len(source) - len(source.rstrip())
    leading = source[:lead_len]
    trailing = source[len(source) - trail_len:] if trail_len else ""

    # Try exact match first (with trailing punctuation)
    if stripped in CANONICAL:
        return leading + CANONICAL[stripped] + trailing

    # Try stripping trailing punctuation
    trail_punct = ""
    core = stripped
    while core and core[-1] in ".:?!…":
        trail_punct = core[-1] + trail_punct
        core = core[:-1]
    # Handle "..." (ASCII three dots) as a unit
    if core.endswith("..") and stripped.endswith("..."):
        # Already stripped one dot above; strip remaining
        core = core[:-2]
        trail_punct = "..." + trail_punct[1:] if trail_punct.startswith(".") else "..." + trail_punct

    if core in CANONICAL:
        return leading + CANONICAL[core] + trail_punct + trailing

    return None


def apply_pattern(source: str) -> str | None:
    """Return Georgian translation of source via PATTERNS, or None."""
    if not source:
        return None
    stripped = source.strip()
    if not stripped:
        return None
    lead_len = len(source) - len(source.lstrip())
    trail_len = len(source) - len(source.rstrip())
    leading = source[:lead_len]
    trailing = source[len(source) - trail_len:] if trail_len else ""

    for regex, builder in PATTERNS:
        m = regex.match(stripped)
        if m:
            try:
                result = builder(m)  # type: ignore[operator]
            except Exception:
                result = None
            if result is not None:
                # Verify placeholder count matches
                if _placeholders(stripped) != _placeholders(result):
                    continue
                return leading + result + trailing
    return None


def _placeholders(s: str) -> tuple[int, int, int, int]:
    """Return (count_%1..%9, count_%s, count_%d, count_{{}}) for placeholder fidelity."""
    pct_n = len(re.findall(r"%[1-9]", s))
    pct_s = s.count("%s")
    pct_d = s.count("%d")
    braces = s.count("{{")
    return pct_n, pct_s, pct_d, braces
