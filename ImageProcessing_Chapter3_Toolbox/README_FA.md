# جعبه‌ابزار آموزشی فصل ۳ پردازش تصویر

## Intensity Transformations and Spatial Filtering

این بسته برای تدریس و آزمایش فصل ۳ کتاب Gonzalez & Woods ساخته شده است. مبنای ترتیب مباحث، فایل تک‌فصل `reference/chapter_03_intensity_transformations_spatial_filtering_fa.tex` و فصل سوم کتاب است.

### اجرای سریع در ویندوز

1. Python 3.10 یا جدیدتر نصب باشد (در هنگام نصب گزینه Add Python to PATH مفید است).
2. روی `INSTALL_AND_RUN.bat` دوبار کلیک کنید. این فایل ابتدا `SETUP_ENV.bat` را اجرا می‌کند، محیط `.venv` می‌سازد، وابستگی‌ها و Tkinter را کنترل می‌کند و سپس GUI را باز می‌کند.
3. دفعات بعد `RUN_TOOLBOX.bat` یا `RUN_TOOLBOX.cmd` را اجرا کنید. برای نصب بدون باز شدن GUI نیز می‌توانید فقط `SETUP_ENV.bat` را اجرا کنید.

### GUI چه دارد؟

- انتخاب تصویر استاندارد از `skimage.data`: camera، moon، coins، page، text، clock، checkerboard.
- پوشه `samples/` نیز چند تصویر نمونه CC0/public-domain و چند الگوی مصنوعی آموزشی را به‌صورت فایل PNG دارد.
- تصاویر مصنوعی آموزشی: zone plate بر پایه ایده رابطه 3-66، ramp، نسخه کم‌کنتراست و نسخه نمک‌وفلفل.
- Browse برای هر تصویر دلخواه.
- Browse جداگانه برای تصویر مرجع در Histogram Matching.
- منوی گروه و الگوریتم، پارامترهای قابل تغییر، نمایش ورودی/خروجی، ذخیره خروجی و رسم هیستوگرام.

### ساختار کد

هر الگوریتم در فایل مستقل خود در پوشه `algorithms/` است و تابع `apply(...)` دارد. هر فایل نیز مستقیماً از خط فرمان قابل اجراست. برای جلوگیری از تکرار کد، فقط بارگذاری/ذخیره تصویر و CLI عمومی در `_common.py` مشترک است؛ منطق الگوریتم در همان فایل مستقل قرار دارد.

مثال:

```bat
.venv\Scripts\python.exe algorithms\gamma_transform.py --params gamma=0.4 --output outputs\gamma.png
.venv\Scripts\python.exe algorithms\median_filter.py --params size=5 --output outputs\median.png
```

برای اجرای آزمون همه الگوریتم‌ها:

```bat
RUN_SMOKE_TEST.bat
```

برای تولید یک contact sheet نمایشی:

```bat
.venv\Scripts\python.exe demo_all.py
```

## نکته آموزشی مهم

در فصل ۳ اکثر عملیات بر تصویر شدت خاکستری تعریف شده‌اند. GUI اگر تصویر رنگی Browse شود، آن را به شدت خاکستری تبدیل می‌کند. این رفتار عمدی است تا رابطه مستقیم میان فرمول‌های فصل و خروجی برنامه حفظ شود.

## وابستگی‌ها

NumPy، SciPy، scikit-image، Pillow و Matplotlib. Tkinter همراه Python استاندارد ویندوز است و برای GUI استفاده شده است.

برای توضیح تمام گزینه‌ها و مقادیر پیشنهادی، `OPTIONS_GUIDE_FA.md` را بخوانید. برای تطبیق هر فایل با بخش کتاب، `CHAPTER3_MAPPING_FA.md` را ببینید.
