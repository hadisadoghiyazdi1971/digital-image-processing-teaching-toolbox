# پیشنهاد ساختار GitHub برای مجموعه آموزشی پردازش تصویر

## پیشنهاد اصلی

برای کل کتاب، به‌جای آن‌که یک Repository داخل Repository دیگر قرار دهید، یک **Monorepo** اصلی بسازید و هر فصل را در یک پوشه مستقل نگه دارید.

نام پیشنهادی مخزن اصلی:

```text
digital-image-processing-teaching-toolbox
```

Description پیشنهادی:

```text
Chapter-by-chapter Python toolboxes, GUIs, demos, and Persian teaching materials for digital image processing.
```

ساختار پیشنهادی:

```text
digital-image-processing-teaching-toolbox/
├── README.md
├── LICENSE
├── chapters/
│   ├── ch01-introduction/
│   ├── ch02-digital-image-fundamentals/
│   ├── ch03-intensity-spatial-filtering/
│   ├── ch04-frequency-domain-filtering/
│   ├── ch05-restoration-reconstruction/
│   ├── ch06-color-image-processing/
│   ├── ch07-wavelets-transforms/
│   ├── ch08-compression-watermarking/
│   ├── ch09-morphology/
│   ├── ch10-segmentation/
│   ├── ch11-feature-extraction/
│   └── ch12-pattern-classification/
├── shared/
│   ├── images/
│   ├── utilities/
│   └── docs/
└── .github/
```

هر فصل می‌تواند `README.md`، `requirements.txt`، کد، GUI، نمونه‌ها و اسناد مخصوص خودش را داشته باشد.

## چرا Monorepo برای این پروژه بهتر است؟

1. دانشجو فقط یک Repository را Clone می‌کند.
2. همه فصل‌ها در یک محل و با نام‌گذاری یکنواخت هستند.
3. لینک دادن بین فصل‌ها ساده است.
4. می‌توان ابزارها و تصاویر مشترک را در `shared/` قرار داد.
5. GitHub Issues، Releases و نسخه‌بندی برای کل درس یکپارچه می‌ماند.
6. نگهداری `git submodule` برای دانشجویان و کاربران تازه‌کار حذف می‌شود.
7. در آینده می‌توان یک GUI اصلی ساخت که از همین پوشه‌ها ابزار هر فصل را اجرا کند.

## چرا «Repository شامل چند Repository» را فعلاً توصیه نمی‌کنم؟

Git به‌طور معمول Repository را به‌عنوان پوشه عادی داخل Repository دیگر مدیریت نمی‌کند. برای این کار باید از **Git submodule** استفاده شود. Submodule برای پروژه‌هایی که واقعاً چرخه انتشار و تیم توسعه مستقل دارند مناسب است، اما برای یک مجموعه آموزشی معمولاً پیچیدگی اضافه ایجاد می‌کند؛ برای مثال کاربر باید clone را با `--recursive` انجام دهد و به‌روزرسانی submoduleها نیز جداگانه مدیریت شود.

بنابراین، تا زمانی که هر فصل واقعاً یک پروژه مستقل با کاربران، release و نگهداری مستقل نشده است، Monorepo انتخاب ساده‌تر و مناسب‌تری است.

## با Repository فصل سوم فعلی چه کنید؟

دو راه دارید.

### راه پیشنهادی: فصل سوم را از ابتدا داخل مخزن اصلی قرار دهید

1. در GitHub روی `New repository` بزنید.
2. نام را بگذارید:

```text
digital-image-processing-teaching-toolbox
```

3. Description را وارد کنید:

```text
Chapter-by-chapter Python toolboxes, GUIs, demos, and Persian teaching materials for digital image processing.
```

4. Public یا Private را انتخاب کنید.
5. بهتر است هنگام ساخت، اگر فایل‌های محلی آماده دارید گزینه ایجاد README خودکار را خاموش بگذارید تا conflict ایجاد نشود.
6. روی کامپیوتر ساختار `chapters/ch03-intensity-spatial-filtering/` را بسازید.
7. محتوای بسته فصل سوم را داخل همین پوشه کپی کنید.
8. فایل `reference/chapter_03_intensity_transformations_spatial_filtering_fa.tex` را فقط در صورتی public کنید که حق بازنشر آن را دارید. PDF کتاب و تصاویر اسکن‌شده کتاب را در GitHub عمومی قرار ندهید.
9. یک `README.md` اصلی در ریشه مخزن بسازید که فهرست فصل‌ها را نشان دهد.
10. Commit و Push کنید.

نمونه دستورات:

```bash
git init
git add .
git commit -m "Initial digital image processing teaching toolbox"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/digital-image-processing-teaching-toolbox.git
git push -u origin main
```

## اگر اصرار دارید هر فصل Repository مستقل باشد

آن‌گاه پیشنهاد من این ساختار است:

```text
dip-ch03-intensity-spatial-filtering
dip-ch04-frequency-domain-filtering
dip-ch05-restoration-reconstruction
dip-ch06-color-image-processing
...
```

و یک مخزن فهرست اصلی ایجاد کنید:

```text
digital-image-processing-teaching-suite
```

این مخزن اصلی فقط README، فهرست فصل‌ها، لینک‌ها، روش نصب و شاید launcher مشترک را نگه دارد. در این حالت **لازم نیست** Repositoryها را واقعاً داخل هم قرار دهید؛ لینک دادن به آنها از README اصلی ساده‌تر است.

اگر بعدها لازم شد همه فصل‌ها با یک clone دریافت شوند، آن زمان می‌توان از Git submodules استفاده کرد.

## نام پیشنهادی Repository مستقل فصل ۳

```text
digital-image-processing-ch3-toolbox
```

Description:

```text
Educational Python GUI and standalone demos for intensity transformations, histogram processing, spatial filtering, smoothing, and sharpening.
```

Topics پیشنهادی GitHub:

```text
image-processing
computer-vision
python
scipy
scikit-image
digital-image-processing
spatial-filtering
histogram-equalization
image-enhancement
education
teaching
tkinter
```

## انتخاب نهایی پیشنهادی من

اگر هدف شما ادامه همین کار برای فصل‌های متعدد کتاب است، **یک Monorepo اصلی** با نام `digital-image-processing-teaching-toolbox` بسازید و فصل سوم را اولین پوشه آن قرار دهید. این ساختار برای درس، دانشجو و نگهداری بلندمدت از چند Repository مستقل و submodule ساده‌تر است.
