# ساخت نسخه وب و PDF

| دستور | خروجی |
| --- | --- |
| `python3 build.py` | صفحه‌های وب در `dist/` (نسخه artifact) |
| `python3 print.py` | فایل PDF در `pdf/` |
| `python3 site.py` | وب‌سایت کامل در `site/` (برای شاخه `gh-pages`) |

اول یک بار `npm install` را اجرا کنید. پیش‌نیازها: Python 3 (beautifulsoup4، numpy، scipy، pypdf)، pandoc، Node 18+، Playwright و فونت وزیرمتن.

- **محتوا:** از `../jozve/chapters/` خوانده می‌شود.
- **فرمول‌ها:** با MathJax به SVG تبدیل می‌شوند (`mathrender.js`).
- **شکل‌ها:** با `figs.py` و `figlib.py` رسم می‌شوند.
- **قالب صفحه:** در `template.py` است.
