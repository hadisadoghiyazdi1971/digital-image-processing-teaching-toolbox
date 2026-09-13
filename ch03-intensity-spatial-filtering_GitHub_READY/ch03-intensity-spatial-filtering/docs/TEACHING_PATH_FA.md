# مسیر پیشنهادی تدریس/ویدیو/آزمایشگاه فصل ۳

این مسیر برای استفاده قبل از کلاس و سپس اجرای کوتاه در کلاس طراحی شده است.

## جلسه 1 — از `T` تا `s=T(r)`

تصویر `ramp` را انتخاب کنید. Negative، Log و Gamma را پشت‌سرهم اجرا کنید. دانشجو قبل از دیدن خروجی شکل منحنی تبدیل را حدس بزند. سپس روی `camera` همان پارامترها را اعمال کنید تا تفاوت «منحنی» و «اثر تصویری» روشن شود.

## جلسه 2 — تبدیل‌های چندپاره و صفحات بیت

از `low_contrast_camera` برای contrast stretch و از `page` یا `text` برای threshold استفاده کنید. Intensity slicing را روی تصویری با چند سطح روشنایی اجرا کنید. سپس bit-planeها را از 7 تا 0 مقایسه کنید.

## جلسه 3 — هیستوگرام

`low_contrast_camera` را با Global Equalization پردازش کنید و histogram ورودی/خروجی را نمایش دهید. برای Histogram Matching تصویر مرجع `moon` یا یک تصویر Browse شده را انتخاب کنید. تفاوت Equalization و Matching را از نظر «هدف توزیع خروجی» توضیح دهید.

## جلسه 4 — local processing

Global Equalization، Local Equalization، Local Statistics و CLAHE را روی یک تصویر واحد مقایسه کنید. درباره تقویت نویز و اندازه پنجره بحث کنید.

## جلسه 5 — correlation و convolution

یک هسته نامتقارن انتخاب کنید تا تفاوت دو عمل دیده شود. سپس یک هسته متقارن بدهید و نشان دهید چرا خروجی‌ها یکسان می‌شوند. boundary mode را تغییر دهید و فقط لبه تصویر را بررسی کنید.

## جلسه 6 — smoothing

روی `salt_pepper_camera` Box، Gaussian و Median را اجرا کنید. هدف فقط «کدام بهتر است» نیست؛ دانشجو باید علت را بر اساس averaging در برابر ranking توضیح دهد. سپس Bilateral را به‌عنوان توسعه مقایسه کنید.

## جلسه 7 — sharpening

روی `moon` یا `camera`: Laplacian response، Laplacian sharpened، Unsharp و High-Boost را مقایسه کنید. سپس Sobel را اجرا کنید و فرق «تصویر تیزشده» با «نقشه اندازه گرادیان» را روشن کنید.

## جلسه 8 — خانواده فیلترها و Zone Plate

`zone_plate` را انتخاب کنید. Lowpass-derived Highpass و Bandpass/Bandreject را اجرا کنید. از نواحی حلقه‌ای خروجی برای توضیح عبور/توقف بازه‌های فرکانسی استفاده کنید.

## جلسه 9 — pipeline نهایی

`combined_enhancement.py` را مرحله‌به‌مرحله توضیح دهید: Laplacian → Sobel → smoothing → mask → enhancement → gamma. از دانشجو بخواهید حذف هر مرحله را پیش‌بینی کند.

## پیشنهاد تکلیف

برای هر گروه، یک تصویر دلخواه Browse شود و سه روش انتخاب شوند. گزارش باید فقط شامل تصویر نباشد؛ دانشجو برای هر روش پارامترها، دلیل انتخاب، اثر مفید و artifact احتمالی را توضیح دهد.
