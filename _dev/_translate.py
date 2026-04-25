#!/usr/bin/env python3
"""
Split Magento i18n:collect-phrases output by module and apply a curated
Georgian dictionary. Rows without a dictionary hit are omitted (Magento
falls back to the source string — safer than shipping wrong Georgian).

Input:  _phrases-raw.csv with rows "<source>","<target>",module|theme,<component>
Output: <Component>.csv per component with only rows that have a translation.
"""
from __future__ import annotations

import csv
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent
INPUT = REPO / "_phrases-raw.csv"
STATS_FILE = REPO / "_coverage.txt"

# P1 = storefront + checkout + Shubo modules. Non-P1 gets AUTO marker.
P1_MODULES = {
    "Magento_Catalog",
    "Magento_Checkout",
    "Magento_Customer",
    "Magento_Cms",
    "Magento_Theme",
    "Magento_Sales",
    "Magento_OfflinePayments",
    "Magento_Payment",
    "Magento_Shipping",
    "Magento_Tax",
    "Magento_Ui",
    "Magento_Wishlist",
    "Magento_Review",
    "Magento_SalesRule",
    "Magento_Quote",
    "Magento_GiftMessage",
    "Magento_Newsletter",
    "Magento_Contact",
    "Magento_ProductAlert",
    "Magento_Search",
    "Magento_CatalogSearch",
    "Magento_Directory",
    "Shubo_TbcPayment",
    "Shubo_BogPayment",
    "Shubo_Merchant",
    "Shubo_ShippingCore",
    "Shubo_Tax",
    "Shubo_Commission",
    "Shubo_Payout",
    "Shubo_CookieConsent",
    "Shubo_MerchantCatalog",
}

# --- Curated Georgian dictionary (exact-match) ---
# Kept lowercased for case-insensitive lookup; casing preserved on output
# via restore_case(). UI-first e-commerce vocabulary for Georgian market.
DICT: dict[str, str] = {
    # --- Core nav / actions ---
    "home": "მთავარი",
    "menu": "მენიუ",
    "search": "ძებნა",
    "search results": "ძებნის შედეგები",
    "cart": "კალათა",
    "shopping cart": "საყიდლების კალათა",
    "my cart": "ჩემი კალათა",
    "checkout": "შეკვეთის გაფორმება",
    "continue": "გაგრძელება",
    "continue shopping": "შოპინგის გაგრძელება",
    "back": "უკან",
    "next": "შემდეგი",
    "previous": "წინა",
    "add": "დამატება",
    "add to cart": "კალათაში დამატება",
    "add to wish list": "სასურველთა სიაში დამატება",
    "add to compare": "შესადარებლად დამატება",
    "remove": "წაშლა",
    "remove from cart": "კალათიდან წაშლა",
    "remove item": "ელემენტის წაშლა",
    "delete": "წაშლა",
    "edit": "რედაქტირება",
    "update": "განახლება",
    "update cart": "კალათის განახლება",
    "apply": "გამოყენება",
    "cancel": "გაუქმება",
    "close": "დახურვა",
    "save": "შენახვა",
    "submit": "გაგზავნა",
    "send": "გაგზავნა",
    "confirm": "დადასტურება",
    "yes": "დიახ",
    "no": "არა",
    "ok": "კარგი",
    "loading...": "იტვირთება...",
    "please wait...": "გთხოვთ, მოიცადოთ...",
    "show": "ჩვენება",
    "hide": "დამალვა",
    "show more": "მეტის ნახვა",
    "show less": "ნაკლების ჩვენება",
    "view details": "დეტალების ნახვა",
    "view all": "ყველას ნახვა",
    "more": "მეტი",
    "details": "დეტალები",
    "description": "აღწერა",
    "more information": "დამატებითი ინფორმაცია",
    "learn more": "გაიგე მეტი",
    "read more": "მეტის წაკითხვა",

    # --- Prices, totals, cart ---
    "price": "ფასი",
    "prices": "ფასები",
    "total": "სულ",
    "totals": "ჯამები",
    "subtotal": "ქვეჯამი",
    "grand total": "საერთო ჯამი",
    "order total": "შეკვეთის ჯამი",
    "quantity": "რაოდენობა",
    "qty": "რაოდენობა",
    "amount": "თანხა",
    "discount": "ფასდაკლება",
    "tax": "გადასახადი",
    "tax amount": "გადასახადის თანხა",
    "shipping": "მიწოდება",
    "shipping & handling": "მიწოდება და დამუშავება",
    "shipping cost": "მიწოდების ღირებულება",
    "free": "უფასო",
    "free shipping": "უფასო მიწოდება",
    "coupon": "კუპონი",
    "coupon code": "კუპონის კოდი",
    "promo code": "აქციის კოდი",
    "enter coupon code": "შეიყვანეთ კუპონის კოდი",
    "apply discount code": "ფასდაკლების კოდის გამოყენება",

    # --- Products / catalog ---
    "product": "პროდუქტი",
    "products": "პროდუქტები",
    "category": "კატეგორია",
    "categories": "კატეგორიები",
    "new products": "ახალი პროდუქტები",
    "featured products": "რჩეული პროდუქტები",
    "related products": "მსგავსი პროდუქტები",
    "recommended": "რეკომენდებული",
    "sku": "SKU",
    "in stock": "მარაგშია",
    "out of stock": "მარაგში არ არის",
    "availability": "ხელმისაწვდომობა",
    "brand": "ბრენდი",
    "color": "ფერი",
    "size": "ზომა",
    "weight": "წონა",
    "material": "მასალა",
    "model": "მოდელი",
    "specifications": "სპეციფიკაციები",
    "filter": "ფილტრი",
    "filters": "ფილტრები",
    "sort": "დალაგება",
    "sort by": "დალაგების ტიპი",
    "price: low to high": "ფასი: დაბლიდან მაღლა",
    "price: high to low": "ფასი: მაღლიდან დაბლა",
    "best selling": "ყველაზე გაყიდვადი",
    "newest": "უახლესი",
    "popularity": "პოპულარობა",
    "rating": "შეფასება",
    "reviews": "მიმოხილვები",
    "review": "მიმოხილვა",
    "write a review": "დაწერე მიმოხილვა",
    "your rating": "შენი შეფასება",
    "be the first to review this product": "დაწერე პირველი მიმოხილვა ამ პროდუქტზე",

    # --- Account ---
    "sign in": "შესვლა",
    "login": "შესვლა",
    "log in": "შესვლა",
    "sign up": "რეგისტრაცია",
    "register": "რეგისტრაცია",
    "create an account": "ანგარიშის შექმნა",
    "create account": "ანგარიშის შექმნა",
    "sign out": "გასვლა",
    "log out": "გასვლა",
    "logout": "გასვლა",
    "my account": "ჩემი ანგარიში",
    "account": "ანგარიში",
    "account information": "ანგარიშის ინფორმაცია",
    "my profile": "ჩემი პროფილი",
    "profile": "პროფილი",
    "my orders": "ჩემი შეკვეთები",
    "my wishlist": "ჩემი სასურველთა სია",
    "wishlist": "სასურველთა სია",
    "address book": "მისამართების წიგნი",
    "my addresses": "ჩემი მისამართები",
    "newsletter subscriptions": "სიახლეების გამოწერები",
    "newsletter": "სიახლეების გამოწერა",
    "subscribe": "გამოწერა",
    "subscribe to newsletter": "სიახლეების გამოწერა",
    "unsubscribe": "გაუქმება",
    "forgot your password?": "პაროლი დაგავიწყდა?",
    "forgot password": "პაროლი დაგავიწყდა",
    "reset password": "პაროლის აღდგენა",
    "change password": "პაროლის შეცვლა",
    "current password": "ახლანდელი პაროლი",
    "new password": "ახალი პაროლი",
    "confirm password": "დაადასტურეთ პაროლი",
    "confirm new password": "დაადასტურეთ ახალი პაროლი",
    "email": "ელ. ფოსტა",
    "email address": "ელ. ფოსტის მისამართი",
    "password": "პაროლი",
    "remember me": "დამიმახსოვრე",
    "welcome": "კეთილი იყოს თქვენი მობრძანება",
    "welcome back": "კეთილი იყოს თქვენი დაბრუნება",
    "hello": "გამარჯობა",

    # --- Personal details ---
    "name": "სახელი",
    "first name": "სახელი",
    "last name": "გვარი",
    "middle name": "მამის სახელი",
    "full name": "სრული სახელი",
    "phone": "ტელეფონი",
    "phone number": "ტელეფონის ნომერი",
    "telephone": "ტელეფონი",
    "mobile": "მობილური",
    "date of birth": "დაბადების თარიღი",
    "gender": "სქესი",
    "male": "მამრობითი",
    "female": "მდედრობითი",
    "company": "კომპანია",
    "tax/vat number": "საგადასახადო ნომერი",
    "vat number": "დღგ-ის ნომერი",

    # --- Address ---
    "address": "მისამართი",
    "addresses": "მისამართები",
    "street address": "ქუჩის მისამართი",
    "street": "ქუჩა",
    "city": "ქალაქი",
    "state": "რეგიონი",
    "state/province": "რეგიონი / ოლქი",
    "region": "რეგიონი",
    "country": "ქვეყანა",
    "zip code": "საფოსტო ინდექსი",
    "zip/postal code": "საფოსტო ინდექსი",
    "postal code": "საფოსტო ინდექსი",
    "billing address": "ანგარიშსწორების მისამართი",
    "shipping address": "მიწოდების მისამართი",
    "same as billing address": "იგივე, რაც ანგარიშსწორების მისამართი",
    "new address": "ახალი მისამართი",
    "default billing address": "ძირითადი ანგარიშსწორების მისამართი",
    "default shipping address": "ძირითადი მიწოდების მისამართი",
    "edit address": "მისამართის რედაქტირება",
    "delete address": "მისამართის წაშლა",
    "add new address": "ახალი მისამართის დამატება",

    # --- Order flow ---
    "order": "შეკვეთა",
    "orders": "შეკვეთები",
    "order number": "შეკვეთის ნომერი",
    "order date": "შეკვეთის თარიღი",
    "order status": "შეკვეთის სტატუსი",
    "order summary": "შეკვეთის შეჯამება",
    "order details": "შეკვეთის დეტალები",
    "order history": "შეკვეთების ისტორია",
    "order information": "შეკვეთის ინფორმაცია",
    "recent orders": "უახლესი შეკვეთები",
    "place order": "შეკვეთის განთავსება",
    "place my order": "ჩემი შეკვეთის განთავსება",
    "proceed to checkout": "შეკვეთის გაფორმებაზე გადასვლა",
    "proceed to payment": "გადახდაზე გადასვლა",
    "order confirmation": "შეკვეთის დადასტურება",
    "thank you for your purchase!": "გმადლობთ შეძენისთვის!",
    "thank you for your order.": "გმადლობთ თქვენი შეკვეთისთვის.",
    "invoice": "ინვოისი",
    "invoices": "ინვოისები",
    "shipment": "გადაზიდვა",
    "shipments": "გადაზიდვები",
    "tracking": "თვალყურის დევნება",
    "tracking number": "თვალყურის დევნების ნომერი",
    "credit memo": "საკრედიტო მემორანდუმი",
    "refund": "თანხის დაბრუნება",
    "refunds": "თანხის დაბრუნებები",
    "return": "დაბრუნება",
    "returns": "დაბრუნებები",

    # --- Order statuses ---
    "pending": "მოლოდინში",
    "pending payment": "გადახდის მოლოდინში",
    "processing": "მიმდინარე",
    "complete": "დასრულებული",
    "completed": "დასრულებული",
    "closed": "დახურული",
    "canceled": "გაუქმებული",
    "cancelled": "გაუქმებული",
    "suspected fraud": "სავარაუდოდ თაღლითური",
    "payment review": "გადახდის განხილვა",
    "on hold": "შეჩერებული",
    "holded": "შეჩერებული",

    # --- Payment ---
    "payment": "გადახდა",
    "payment method": "გადახდის მეთოდი",
    "payment methods": "გადახდის მეთოდები",
    "payment information": "გადახდის ინფორმაცია",
    "credit card": "საკრედიტო ბარათი",
    "debit card": "სადებეტო ბარათი",
    "card number": "ბარათის ნომერი",
    "expiration date": "ვადის გასვლის თარიღი",
    "cvv": "CVV",
    "cardholder name": "ბარათის მფლობელის სახელი",
    "cash on delivery": "ნაღდი ანგარიშსწორებით მიწოდებისას",
    "bank transfer": "საბანკო გადარიცხვა",
    "check / money order": "ჩეკი / ფულადი ორდერი",

    # --- Shipping ---
    "shipping method": "მიწოდების მეთოდი",
    "shipping methods": "მიწოდების მეთოდები",
    "shipping information": "მიწოდების ინფორმაცია",
    "delivery": "მიწოდება",
    "delivery address": "მიწოდების მისამართი",
    "delivery date": "მიწოდების თარიღი",
    "estimated delivery": "სავარაუდო მიწოდება",
    "flat rate": "ფიქსირებული ტარიფი",
    "table rate": "ცხრილის ტარიფი",
    "free shipping amount": "უფასო მიწოდების თანხა",
    "shipping rate": "მიწოდების ტარიფი",
    "pickup": "თვითგატანა",
    "store pickup": "მაღაზიიდან გატანა",

    # --- Status messages / errors ---
    "this is a required field.": "ეს ველი სავალდებულოა.",
    "this field is required.": "ეს ველი სავალდებულოა.",
    "required": "სავალდებულო",
    "optional": "არასავალდებულო",
    "error": "შეცდომა",
    "warning": "გაფრთხილება",
    "success": "წარმატება",
    "successful": "წარმატებული",
    "notice": "შენიშვნა",
    "please enter a valid email address.": "გთხოვთ, შეიყვანოთ მოქმედი ელ. ფოსტის მისამართი.",
    "please enter a valid phone number.": "გთხოვთ, შეიყვანოთ მოქმედი ტელეფონის ნომერი.",
    "please enter a valid value.": "გთხოვთ, შეიყვანოთ მოქმედი მნიშვნელობა.",
    "the value is not valid.": "მნიშვნელობა არასწორია.",
    "invalid email address": "არასწორი ელ. ფოსტის მისამართი",
    "invalid value": "არასწორი მნიშვნელობა",
    "invalid password": "არასწორი პაროლი",
    "password is required.": "პაროლი სავალდებულოა.",
    "an unknown error occurred.": "მოხდა უცნობი შეცდომა.",
    "something went wrong.": "რაღაც შეცდომა მოხდა.",
    "something went wrong while saving.": "შენახვისას მოხდა შეცდომა.",
    "invalid login or password.": "არასწორი მომხმარებელი ან პაროლი.",
    "please agree to all the terms and conditions before placing the order.": "შეკვეთის განთავსებამდე, გთხოვთ, დაეთანხმოთ ყველა წესს და პირობას.",

    # --- Date / time ---
    "date": "თარიღი",
    "time": "დრო",
    "today": "დღეს",
    "yesterday": "გუშინ",
    "tomorrow": "ხვალ",
    "from": "დან",
    "to": "მდე",
    "from date": "დაწყების თარიღი",
    "to date": "დასრულების თარიღი",

    # --- Contact ---
    "contact us": "დაგვიკავშირდით",
    "about us": "ჩვენ შესახებ",
    "terms and conditions": "წესები და პირობები",
    "privacy policy": "კონფიდენციალურობის პოლიტიკა",
    "customer service": "მომხმარებელთა მომსახურება",
    "help": "დახმარება",
    "support": "მხარდაჭერა",
    "faq": "ხშირად დასმული კითხვები",
    "message": "შეტყობინება",
    "your message": "თქვენი შეტყობინება",
    "send message": "შეტყობინების გაგზავნა",

    # --- Pagination + misc ---
    "page": "გვერდი",
    "pages": "გვერდები",
    "first": "პირველი",
    "last": "ბოლო",
    "of": "ის",
    "items": "ელემენტი",
    "item": "ელემენტი",
    "%1 item": "%1 ელემენტი",
    "%1 items": "%1 ელემენტი",
    "empty": "ცარიელია",
    "you have no items in your shopping cart.": "თქვენ არ გაქვთ ელემენტები საყიდლების კალათაში.",
    "your cart is empty": "თქვენი კალათა ცარიელია",
    "your wishlist is empty.": "თქვენი სასურველთა სია ცარიელია.",

    # --- CMS / theme common ---
    "what's new": "სიახლეები",
    "about": "შესახებ",
    "careers": "კარიერა",
    "news": "სიახლეები",
    "blog": "ბლოგი",
    "follow us": "გამოგვყევით",
    "copyright": "საავტორო უფლებები",
    "all rights reserved.": "ყველა უფლება დაცულია.",
    "footer": "ქვედა ნაწილი",
    "header": "ზედა ნაწილი",
    "sidebar": "გვერდითი პანელი",
    "loading": "იტვირთება",
    "copy": "კოპირება",
    "print": "ამობეჭდვა",
    "download": "ჩამოტვირთვა",

    # --- Account dashboard ---
    "dashboard": "მთავარი გვერდი",
    "my dashboard": "ჩემი მთავარი გვერდი",
    "activity": "აქტივობა",
    "recent activity": "უახლესი აქტივობა",
    "notifications": "შეტყობინებები",
    "settings": "პარამეტრები",

    # --- Commerce specific ---
    "checkout as guest": "გრძელდება ვიზიტორად",
    "checkout as a guest": "გრძელდება ვიზიტორად",
    "guest checkout": "ვიზიტორის შეკვეთა",
    "sign in to your account": "შედით თქვენს ანგარიშში",
    "already have an account?": "უკვე გაქვთ ანგარიში?",
    "new customer?": "ახალი მომხმარებელი?",
    "personal information": "პირადი ინფორმაცია",
    "contact information": "საკონტაქტო ინფორმაცია",
    "sign in information": "შესვლის ინფორმაცია",
    "sign-in information": "შესვლის ინფორმაცია",
    "is this your first time?": "თქვენი პირველი ვიზიტია?",
    "order placed successfully.": "შეკვეთა წარმატებით განთავსდა.",
    "your order has been received.": "თქვენი შეკვეთა მიღებულია.",
    "thank you for your purchase": "გმადლობთ შეძენისთვის",
    "i agree": "ვეთანხმები",
    "agree": "დათანხმება",
    "accept": "მიღება",
    "decline": "უარყოფა",
    "optional information": "არასავალდებულო ინფორმაცია",

    # --- Specific payment / Shubo ---
    "pay with tbc": "გადაიხადეთ თიბისით",
    "pay with bog": "გადაიხადეთ საქართველოს ბანკით",
    "pay with card": "გადაიხადეთ ბარათით",
    "pay now": "გადახდა",
    "pay on delivery": "გადახდა მიწოდებისას",
    "pay by bank transfer": "საბანკო გადარიცხვა",
    "redirecting to payment provider...": "გადამისამართება გადახდის პროვაიდერთან...",
    "please do not close this page.": "გთხოვთ, არ დახუროთ ეს გვერდი.",
    "processing your payment": "თქვენი გადახდის დამუშავება",

    # --- Merchant / vendor ---
    "merchant": "გამყიდველი",
    "merchants": "გამყიდველები",
    "vendor": "მიმწოდებელი",
    "vendors": "მიმწოდებლები",
    "store": "მაღაზია",
    "stores": "მაღაზიები",
    "sold by": "გამყიდველი",
    "seller": "გამყიდველი",
    "sellers": "გამყიდველები",
    "shop": "მაღაზია",
    "shops": "მაღაზიები",
    "marketplace": "მარკეტფლეისი",

    # --- Cookies ---
    "cookies": "ქუქი-ფაილები",
    "cookie policy": "ქუქი-ფაილების პოლიტიკა",
    "we use cookies": "ჩვენ ვიყენებთ ქუქი-ფაილებს",
    "accept all": "ყველას მიღება",
    "reject all": "ყველას უარყოფა",
    "customize": "პერსონალიზება",
    "necessary": "აუცილებელი",
    "analytics": "ანალიტიკა",
    "marketing": "მარკეტინგი",
    "preferences": "პრეფერენციები",

    # --- Common short ---
    "on": "ჩართული",
    "off": "გამორთული",
    "enabled": "ჩართულია",
    "disabled": "გამორთულია",
    "active": "აქტიური",
    "inactive": "არააქტიური",
    "public": "საჯარო",
    "private": "პირადი",
    "all": "ყველა",
    "none": "არცერთი",
    "select": "აირჩიეთ",
    "please select": "გთხოვთ, აირჩიოთ",
    "please select...": "გთხოვთ, აირჩიოთ...",
    "other": "სხვა",
    "unknown": "უცნობი",
    "n/a": "არ არის",
    "version": "ვერსია",
    "language": "ენა",
    "currency": "ვალუტა",
    "click here": "დააჭირეთ აქ",
    "here": "აქ",
    "there": "იქ",

    # --- Georgian currency / taxation hints ---
    "georgian lari": "ქართული ლარი",
    "lari": "ლარი",
    "gel": "ლარი",
    "usd": "აშშ დოლარი",
    "eur": "ევრო",
    "subtotal including tax": "ქვეჯამი გადასახადის ჩათვლით",
    "subtotal excluding tax": "ქვეჯამი გადასახადის გარეშე",
    "incl. tax": "გადასახადის ჩათვლით",
    "excl. tax": "გადასახადის გარეშე",
    "including tax": "გადასახადის ჩათვლით",
    "excluding tax": "გადასახადის გარეშე",
    "vat": "დღგ",

    # --- Admin / action verbs ---
    "actions": "მოქმედებები",
    "action": "მოქმედება",
    "approve": "დადასტურება",
    "approved": "დადასტურებული",
    "approve selected": "არჩეულის დადასტურება",
    "reject": "უარყოფა",
    "rejected": "უარყოფილი",
    "suspend": "შეჩერება",
    "suspended": "შეჩერებული",
    "terminate": "შეწყვეტა",
    "terminated": "შეწყვეტილი",
    "activate": "აქტივაცია",
    "deactivate": "დეაქტივაცია",
    "reset": "განულება",
    "refresh": "განახლება",
    "retry": "სცადეთ თავიდან",
    "view": "ნახვა",
    "new": "ახალი",
    "create": "შექმნა",
    "create new": "ახლის შექმნა",
    "import": "იმპორტი",
    "export": "ექსპორტი",
    "download csv": "CSV-ის ჩამოტვირთვა",
    "export csv": "CSV-ად ექსპორტი",
    "bulk actions": "ჯგუფური მოქმედებები",

    # --- Payment module specifics ---
    "authorize & capture": "ავტორიზაცია და ჩამოჭრა",
    "authorize only": "მხოლოდ ავტორიზაცია",
    "authorize and capture": "ავტორიზაცია და ჩამოჭრა",
    "capture": "ჩამოჭრა",
    "capture payment": "გადახდის ჩამოჭრა",
    "capture offline": "ჩამოჭრა ოფლაინ",
    "capture online": "ჩამოჭრა ონლაინ",
    "void": "გაუქმება",
    "voided": "გაუქმებული",
    "refund online": "ონლაინ დაბრუნება",
    "refund offline": "ოფლაინ დაბრუნება",
    "partial refund": "ნაწილობრივი დაბრუნება",
    "full refund": "სრული დაბრუნება",
    "payment status": "გადახდის სტატუსი",
    "payment failed": "გადახდა ვერ შესრულდა",
    "payment successful": "გადახდა წარმატებულია",
    "payment approved": "გადახდა დადასტურებულია",
    "payment declined": "გადახდა უარყოფილია",
    "payment pending": "გადახდა მოლოდინში",
    "payment canceled": "გადახდა გაუქმებულია",
    "transaction id": "ტრანზაქციის ID",
    "transaction": "ტრანზაქცია",
    "transactions": "ტრანზაქციები",
    "settlement": "ანგარიშსწორება",
    "settled": "ანგარიშსწორებულია",
    "an error occurred processing your payment. please contact support.":
        "თქვენი გადახდის დამუშავებისას მოხდა შეცდომა. გთხოვთ, დაუკავშირდით მხარდაჭერას.",
    "an error occurred while initiating payment. please try again.":
        "გადახდის დაწყებისას მოხდა შეცდომა. გთხოვთ, სცადოთ თავიდან.",

    # --- Merchant admin ---
    "merchant name": "გამყიდველის სახელი",
    "merchant id": "გამყიდველის ID",
    "merchant status": "გამყიდველის სტატუსი",
    "tax id": "საიდენტიფიკაციო ნომერი",
    "personal id": "პირადი ნომერი",
    "company name": "კომპანიის სახელი",
    "company code": "კომპანიის კოდი",
    "admin note": "ადმინისტრაციული შენიშვნა",
    "admin notes": "ადმინისტრაციული შენიშვნები",
    "add merchant": "გამყიდველის დამატება",
    "edit merchant": "გამყიდველის რედაქტირება",
    "active merchants": "აქტიური გამყიდველები",
    "approve merchants": "გამყიდველების დადასტურება",
    "reject merchants": "გამყიდველების უარყოფა",
    "pending merchants": "მოლოდინში მყოფი გამყიდველები",
    "suspended merchants": "შეჩერებული გამყიდველები",
    "account holder name": "ანგარიშის მფლობელის სახელი",
    "bank name": "ბანკის სახელი",
    "bank account": "საბანკო ანგარიში",
    "iban": "IBAN",
    "pickup address": "გატანის მისამართი",
    "pickup addresses": "გატანის მისამართები",
    "subdomain slug": "ქვედომეინის ბმული",

    # --- Payout + commission ---
    "amount due": "გადასახდელი თანხა",
    "amount paid": "გადახდილი თანხა",
    "amount the merchant earned this period.": "თანხა, რომელიც გამყიდველმა ამ პერიოდში გამოიმუშავა.",
    "payout": "გადასახდელი",
    "payouts": "გადასახდელები",
    "settlement period": "ანგარიშსწორების პერიოდი",
    "settlement periods": "ანგარიშსწორების პერიოდები",
    "settlement status": "ანგარიშსწორების სტატუსი",
    "commission": "საკომისიო",
    "commissions": "საკომისიოები",
    "commission rate": "საკომისიოს განაკვეთი",
    "commission amount": "საკომისიოს თანხა",
    "commission status": "საკომისიოს სტატუსი",
    "commission collected": "საკომისიო შეგროვებულია",
    "collection status": "შეგროვების სტატუსი",
    "collected": "შეგროვებული",
    "uncollected": "შეუგროვებელი",
    "merchant payout": "გამყიდველის გადასახდელი",
    "merchant earnings": "გამყიდველის შემოსავალი",
    "item breakdown": "ელემენტების დაშლა",
    "adjustments": "კორექტირებები",
    "adjustment": "კორექტირება",
    "adjustment details": "კორექტირების დეტალები",
    "all time": "ყველა დრო",
    "this month": "ამ თვეში",
    "this week": "ამ კვირაში",
    "last month": "გასულ თვეში",
    "last week": "გასულ კვირას",
    "last 30 days": "ბოლო 30 დღე",
    "last 7 days": "ბოლო 7 დღე",

    # --- Shipping + COD ---
    "carrier": "გადამტანი",
    "carriers": "გადამტანები",
    "carrier status": "გადამტანის სტატუსი",
    "carrier tracking": "გადამტანის თვალყურის დევნება",
    "cod": "COD",
    "back to shipments": "გადაზიდვების სიაზე დაბრუნება",
    "cancel shipment": "გადაზიდვის გაუქმება",
    "mark as shipped": "გადაზიდულად მონიშვნა",
    "mark as delivered": "მიტანილად მონიშვნა",
    "mark cod reconciled": "COD-ის შესრულების მონიშვნა",
    "delivered": "მიტანილი",
    "in transit": "გადაცემის პროცესში",
    "not yet shipped": "ჯერ არ გაიგზავნა",

    # --- Cookie banner extras ---
    "cookie settings": "ქუქი-ფაილების პარამეტრები",
    "manage cookies": "ქუქი-ფაილების მართვა",
    "save preferences": "პრეფერენციების შენახვა",
    "more options": "დამატებითი ოფციები",
    "functional": "ფუნქციონალური",
    "performance": "წარმადობა",

    # --- Checkout step labels ---
    "shipping step": "მიწოდების ეტაპი",
    "payment step": "გადახდის ეტაპი",
    "review step": "გადახედვის ეტაპი",
    "place order step": "შეკვეთის განთავსების ეტაპი",
    "order review": "შეკვეთის გადახედვა",
    "review your order": "გადახედეთ თქვენს შეკვეთას",
    "review and place order": "გადახედე და განათავსე შეკვეთა",

    # --- Reports / admin grid ---
    "reports": "ანგარიშები",
    "report": "ანგარიში",
    "date range": "თარიღის შუალედი",
    "summary": "შეჯამება",
    "overview": "მიმოხილვა",
    "statistics": "სტატისტიკა",
    "totals by day": "ჯამები დღის მიხედვით",
    "totals by month": "ჯამები თვის მიხედვით",
    "totals by year": "ჯამები წლის მიხედვით",

    # --- Reviews ---
    "submit review": "მიმოხილვის გაგზავნა",
    "review submitted": "მიმოხილვა გაგზავნილია",
    "thank you for your review.": "გმადლობთ თქვენი მიმოხილვისთვის.",
    "nickname": "მეტსახელი",
    "summary of your review": "თქვენი მიმოხილვის შეჯამება",
    "your review": "თქვენი მიმოხილვა",
    "1 star": "1 ვარსკვლავი",
    "2 stars": "2 ვარსკვლავი",
    "3 stars": "3 ვარსკვლავი",
    "4 stars": "4 ვარსკვლავი",
    "5 stars": "5 ვარსკვლავი",

    # --- Wishlist ---
    "share wishlist": "სასურველთა სიის გაზიარება",
    "update wishlist": "სასურველთა სიის განახლება",
    "remove from wishlist": "სასურველთა სიიდან წაშლა",

    # --- Newsletter ---
    "enter your email address": "შეიყვანეთ ელ. ფოსტის მისამართი",
    "we will never share your email address.": "ჩვენ არასოდეს გავუზიარებთ თქვენს ელ. ფოსტის მისამართს.",
    "thank you for subscribing.": "გმადლობთ გამოწერისთვის.",
    "you have been subscribed.": "თქვენ გამოწერილი ხართ.",
    "you have been unsubscribed.": "გამოწერა გაუქმდა.",

    # --- Sales / orders extras ---
    "print order": "შეკვეთის ამობეჭდვა",
    "print invoice": "ინვოისის ამობეჭდვა",
    "reorder": "შეკვეთის განმეორება",
    "order id": "შეკვეთის ID",
    "purchase date": "შეძენის თარიღი",
    "purchased on": "შეძენილია",
    "bill to name": "ანგარიშის მიმღები",
    "ship to name": "მიმღების სახელი",
    "g.t. (base)": "საერთო ჯამი (ძირითადი)",
    "g.t. (purchased)": "საერთო ჯამი (გადახდილი)",

    # --- Generic UI verbs ---
    "add new": "ახლის დამატება",
    "create new order": "ახალი შეკვეთის შექმნა",
    "change": "შეცვლა",
    "change status": "სტატუსის შეცვლა",
    "select item": "ელემენტის არჩევა",
    "select all": "ყველას არჩევა",
    "unselect all": "არჩევის გაუქმება",
    "deselect": "არჩევის გაუქმება",
    "go": "გადასვლა",
    "copy": "კოპირება",
    "duplicate": "დუბლირება",
    "move": "გადატანა",
    "clone": "კლონირება",
    "continue to next step": "შემდეგ ეტაპზე გადასვლა",

    # --- Generic messages ---
    "no items found": "ელემენტები ვერ მოიძებნა",
    "no records found": "ჩანაწერები ვერ მოიძებნა",
    "no data available": "მონაცემები არ არის",
    "no results": "შედეგი არ არის",
    "saved successfully": "წარმატებით შენახულია",
    "saved successfully.": "წარმატებით შენახულია.",
    "deleted successfully": "წარმატებით წაიშალა",
    "deleted successfully.": "წარმატებით წაიშალა.",
    "updated successfully": "წარმატებით განახლდა",
    "updated successfully.": "წარმატებით განახლდა.",
    "an error occurred. please try again.": "მოხდა შეცდომა. გთხოვთ, სცადოთ თავიდან.",
    "please try again.": "გთხოვთ, სცადოთ თავიდან.",
    "please try again later.": "გთხოვთ, სცადოთ მოგვიანებით.",
    "authentication required.": "ავტორიზაცია სავალდებულოა.",
    "you are not authorized to perform this action.": "თქვენ არ გაქვთ ამ მოქმედების შესრულების უფლება.",
    "access denied": "წვდომა აკრძალულია",
    "not found": "ვერ მოიძებნა",
    "no such entity.": "ასეთი ჩანაწერი არ არსებობს.",

    # --- Configurable product ---
    "choose an option": "აირჩიეთ ვარიანტი",
    "choose an option...": "აირჩიეთ ვარიანტი...",
    "please choose product options": "გთხოვთ, აირჩიეთ პროდუქტის ვარიანტები",

    # --- Misc admin grid columns ---
    "id": "ID",
    "created at": "შექმნილია",
    "updated at": "განახლებულია",
    "created": "შექმნილი",
    "updated": "განახლებული",
    "modified": "მოდიფიცირებული",

    # --- Amount & currency combinations ---
    "%1 gel": "%1 ლარი",
    "amount must be non-zero.": "თანხა ნულის ტოლი არ უნდა იყოს.",
    "adjustment amount cannot be zero.": "კორექტირების თანხა არ შეიძლება იყოს ნული.",
    "a dispute reason is required.": "საჭიროა დავის მიზეზი.",
    "a reason is required for termination.": "შეწყვეტისთვის საჭიროა მიზეზი.",
    "-- select merchant --": "-- აირჩიეთ გამყიდველი --",
    "-- select --": "-- აირჩიეთ --",

    # --- Email notification common ---
    "you have a new order.": "გაქვთ ახალი შეკვეთა.",
    "thank you for your business.": "გმადლობთ თანამშრომლობისთვის.",
    "thank you for shopping with us.": "გმადლობთ ჩვენთან შოპინგისთვის.",

    # --- VAT threshold / finance ---
    "approaching vat registration threshold": "უახლოვდება დღგ-ის რეგისტრაციის ზღვარს",
    "vat registration threshold reached": "დღგ-ის რეგისტრაციის ზღვარი მიღწეულია",

    # --- Misc Shubo ---
    "3ds status": "3DS სტატუსი",
    "3ds": "3DS",
    "sandbox": "ტესტური გარემო",
    "sandbox mode": "ტესტური რეჟიმი",
    "production mode": "პროდუქციული რეჟიმი",
    "test mode": "ტესტური რეჟიმი",
    "live mode": "პროდუქციული რეჟიმი",
    "api url": "API URL",
    "client id": "კლიენტის ID",
    "client secret": "კლიენტის საიდუმლო",
    "public key": "საჯარო გასაღები",
    "private key": "პირადი გასაღები",
    "webhook": "Webhook",
    "webhooks": "Webhooks",
    "webhook url": "Webhook URL",
    "callback url": "Callback URL",
}


def _has_cyrillic(s: str) -> bool:
    return bool(re.search(r"[Ⴀ-ჿⴀ-⴯]", s))


def translate(phrase: str) -> str | None:
    """Exact-match look-up. Returns Georgian or None for omit-row."""
    if not phrase:
        return None
    # Preserve any phrases that already contain Georgian characters
    if _has_cyrillic(phrase):
        return None

    lower = phrase.lower().strip()
    if lower in DICT:
        return DICT[lower]

    # Strip trailing/leading punctuation for lookup, restore on output
    m = re.match(r"^(\W*)(.+?)(\W*)$", phrase, re.DOTALL)
    if m:
        lead, core, tail = m.groups()
        lk = core.lower()
        if lk in DICT:
            return lead + DICT[lk] + tail

    return None


def main() -> int:
    by_module: dict[str, list[tuple[str, str]]] = defaultdict(list)

    valid_component = re.compile(r"^[A-Z][A-Za-z0-9]+_[A-Z][A-Za-z0-9]+$")

    with INPUT.open(newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) < 4:
                continue
            source, _, kind, component = row[0], row[1], row[2], row[3]
            if not valid_component.match(component):
                continue
            by_module[component].append((source, kind))

    total_phrases = 0
    total_translated = 0
    p1_coverage: list[tuple[str, int, int]] = []
    auto_coverage: list[tuple[str, int, int]] = []

    for component, phrases in sorted(by_module.items()):
        # De-dup phrases (same string collected from multiple files)
        seen: set[str] = set()
        unique_sources: list[str] = []
        for src, _ in phrases:
            if src not in seen:
                seen.add(src)
                unique_sources.append(src)

        translated = [(s, translate(s)) for s in unique_sources]
        hits = [(s, t) for s, t in translated if t is not None]
        total_phrases += len(unique_sources)
        total_translated += len(hits)

        if not hits:
            continue

        out_file = REPO / f"{component}.csv"
        with out_file.open("w", newline="", encoding="utf-8") as w:
            writer = csv.writer(w, quoting=csv.QUOTE_ALL)
            for src, tgt in hits:
                writer.writerow([src, tgt])

        if component in P1_MODULES:
            p1_coverage.append((component, len(hits), len(unique_sources)))
        else:
            auto_coverage.append((component, len(hits), len(unique_sources)))

    with STATS_FILE.open("w", encoding="utf-8") as s:
        s.write("# Shubo_LanguagePack_Ka_GE coverage report\n")
        s.write(f"Total unique source phrases:     {total_phrases}\n")
        s.write(f"Total translated rows:           {total_translated}\n")
        if total_phrases:
            pct = 100.0 * total_translated / total_phrases
            s.write(f"Overall coverage:                {pct:.2f}%\n")
        s.write(f"P1 modules with translations:    {len(p1_coverage)}\n")
        s.write(f"Non-P1 modules with translations: {len(auto_coverage)}\n\n")
        s.write("## P1 module coverage (storefront + checkout — human-reviewed dictionary)\n")
        s.write("| Module | Translated | Total | % |\n")
        s.write("|---|---:|---:|---:|\n")
        for m, t, n in sorted(p1_coverage, key=lambda x: -x[1]):
            s.write(f"| {m} | {t} | {n} | {100.0 * t / n:.1f}% |\n")
        s.write("\n## Non-P1 module coverage (auto-matched via shared dictionary — needs human pass)\n")
        s.write("| Module | Translated | Total | % |\n")
        s.write("|---|---:|---:|---:|\n")
        for m, t, n in sorted(auto_coverage, key=lambda x: -x[1])[:50]:
            s.write(f"| {m} | {t} | {n} | {100.0 * t / n:.1f}% |\n")

    print(f"OK — {total_translated} rows across {len(p1_coverage) + len(auto_coverage)} CSV files")
    print(f"     P1 modules: {len(p1_coverage)}, non-P1: {len(auto_coverage)}")
    print(f"     Coverage report at {STATS_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
