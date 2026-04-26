# Magento 2 ქართული ენის პაკეტი (`ka_GE`)

**პირველი საჯარო ქართული (`ka_GE`) ენის პაკეტი Magento 2.4.x-ისთვის.** ~92% ნათარგმნი, MIT ლიცენზია.

---

## რატომ შეიქმნა

Magento 2-ისთვის ქართული ენის საჯარო პაკეტი ადრე არ არსებობდა. ქართველი მეწარმეები, რომლებიც Magento 2-ს იყენებენ, მაღაზიებს ინგლისურად ან რუსულად ანახლებდნენ. ეს პაკეტი შეიქმნა [duka.ge](https://duka.ge)-ის მიერ — ქართული SME მარკეტფლეისი, რომელიც Magento 2-ზეა აგებული.

---

## ინსტალაცია (Composer)

```bash
composer require shubodev/language-pack-ka-ge
bin/magento setup:upgrade
bin/magento setup:static-content:deploy ka_GE -f
bin/magento config:set general/locale/code ka_GE --scope=stores --scope-code=default
bin/magento cache:flush
```

---

## ინსტალაცია (ხელით)

1. გახსენით `app/i18n/Shubo/ka_GE/`-ში
2. გაუშვით:
   ```bash
   bin/magento setup:upgrade
   bin/magento setup:static-content:deploy ka_GE -f
   bin/magento cache:flush
   ```

---

## მონაწილეობა / Contribution

ქართულენოვანი შესწორებების გამოგზავნა შეგიძლიათ Pull Request-ის სახით. მანამდე, გთხოვთ, გაეცნოთ [სტილის სახელმძღვანელოს](./docs/style-guide.md).

**არასწორი თარგმანის შეტყობინება:** გახსენით [GitHub Issue](https://github.com/nshubitidze/module-language-pack-ka-ge/issues) ინგლისური წყაროს სტრინგით, ამჟამინდელი ქართული თარგმანით და თქვენი შეთავაზებული შესწორებით.

---

## ლიცენზია

[MIT](./LICENSE) — თავისუფლად შეგიძლიათ გამოყენება, შეცვლა და გავრცელება.

---

## ავტორი

[duka.ge](https://duka.ge) / [Shubo](https://github.com/nshubitidze)
