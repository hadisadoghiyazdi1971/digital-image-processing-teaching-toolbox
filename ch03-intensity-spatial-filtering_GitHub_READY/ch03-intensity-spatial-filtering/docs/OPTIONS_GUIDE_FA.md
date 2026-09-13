# راهنمای کامل گزینه‌ها — Chapter 3 Toolbox

این فایل مرجع پارامترهای GUI است. برای مسیر مفهومی کامل فصل ابتدا `CHAPTER3_CONCEPTS_FA.md` را ببینید.

## تصاویر ورودی

`camera` برای مشاهده عمومی کنتراست و لبه، `moon` برای جزئیات آرام و تیزسازی، `coins` برای مرزهای شیء، `page` و `text` برای آستانه‌گذاری/کنتراست، `checkerboard` برای پاسخ لبه، `zone_plate` برای رفتار پایین‌گذر/بالاگذر/میان‌گذر، `low_contrast_camera` برای پردازش هیستوگرام، و `salt_pepper_camera` برای مقایسه میانگین/گاوسی/میانه مناسب‌اند.

## تبدیلات شدت

- **Negative**: بدون پارامتر؛ `s=1-r`.
- **Log**: `c` بهره خروجی. مقدار 1 معمولاً کافی است.
- **Inverse-log / Exponential**: `alpha` شدت منحنی نمایی را تعیین می‌کند؛ مکمل آموزشی خانواده لگاریتمی است.
- **Gamma**: `gamma<1` نواحی تیره را باز می‌کند، `gamma>1` تصویر را تیره‌تر می‌کند؛ `c` بهره است.
- **Contrast Stretch**: `p_low`,`p_high` صدک‌های ابتدا/انتها؛ مثلاً 2 و 98 برای حذف اثر outlierها.
- **Piecewise Linear**: نقاط `(r1,s1)` و `(r2,s2)` منحنی سه‌بخشی را تعیین می‌کنند.
- **Threshold**: `threshold` مرز تصمیم؛ `low` و `high` مقادیر دو کلاس.
- **Intensity Slicing**: بازه `[low,high]` با `highlight` برجسته می‌شود؛ `preserve_background=True` زمینه را حفظ می‌کند.
- **Bit Plane**: `plane=7` بیت پرارزش، `plane=0` بیت کم‌ارزش.
- **Sigmoid (افزوده)**: `cutoff` مرکز گذار، `gain` تندی گذار.
- **asinh (افزوده)**: `alpha` شدت فشرده‌سازی دامنه دینامیکی.
- **Window/Level (افزوده)**: `center` مرکز پنجره و `width` پهنای پنجره؛ برای نمایش ناحیه شدت خاص مفید است.

## هیستوگرام

- **Global Equalization**: `nbins` تعداد binها، معمولاً 256.
- **Histogram Matching**: تصویر ورودی به توزیع تصویر مرجع نزدیک می‌شود. از دکمه Browse مرجع استفاده کنید.
- **Local Equalization**: `size` اندازه پنجره محلی. بزرگ‌تر = رفتار محلی نرم‌تر و محاسبه بیشتر.
- **CLAHE (افزوده)**: `kernel_size` اندازه tile، `clip_limit` محدودکننده تقویت نویز، `nbins` تعداد سطح‌ها.
- **Local Statistics Eq. 3-29**: `window` پنجره، `C` بهره، و `k0..k3` حدود میانگین و انحراف معیار محلی نسبت به مقادیر سراسری.

## همبستگی و هم‌پیچش

`kernel` به صورت سطرهای جداشده با `;` و عناصر جداشده با `,` نوشته می‌شود. مثال:

`0,-1,0;-1,5,-1;0,-1,0`

`boundary` روش رفتار مرزی است: reflect، nearest، mirror، wrap، constant. برای هسته‌های مشتقی که پاسخ منفی دارند، `display_scale=True` پاسخ را برای نمایش به 0..1 مقیاس می‌کند.

- **Separable Gaussian demo** دو پاس یک‌بعدی را صریحاً اجرا می‌کند و با گزینه `difference` اختلاف آن با Gaussian دوبعدی را نشان می‌دهد.
- **Cascade/Composite** رابطه هسته مرکب فصل را با دو هم‌پیچش متوالی در برابر یک هسته مرکب مقایسه می‌کند.

## هموارسازی

- **Box**: `size` اندازه هسته؛ افزایش آن تاری بیشتر می‌دهد.
- **Gaussian**: `sigma` پهنای گاوسی؛ مقدار 1 تا 3 برای مشاهده آموزشی مناسب است.
- **Median**: `size` پنجره مرتب‌سازی؛ برای نویز نمک‌وفلفل مناسب است.
- **Order Statistic (افزوده)**: `kind=min|max|midpoint`.
- **Bilateral (افزوده)**: `sigma_color` حساسیت به اختلاف شدت و `sigma_spatial` مقیاس مکانی؛ لبه‌ها را بهتر از Gaussian حفظ می‌کند.

## تیزسازی

- **Laplacian**: `connectivity=4|8`، `gain` مقدار افزودن جزئیات، `output=response|sharpened`.
- **Unsharp**: `sigma` میزان blur و `amount` وزن mask؛ `amount=1` حالت کلاسیک است.
- **High-Boost**: `k>1` تیزسازی قوی‌تر؛ مقادیر بسیار بزرگ هاله می‌سازند.
- **Roberts/Sobel**: مطابق فصل. Prewitt و Scharr گزینه‌های افزوده برای مقایسه‌اند.

## خانواده پالایه‌ها از Lowpass

- **Highpass from Lowpass**: پاسخ `f-LP(f)`؛ `sigma` مقیاس lowpass است.
- **Bandpass/Bandreject**: دو مقیاس Gaussian لازم است و باید `sigma_large > sigma_small` باشد. Bandpass برابر اختلاف دو lowpass و Bandreject مکمل آن نسبت به ورودی است. این پیاده‌سازی آموزشی، رابطه ساخت خانواده فیلترها از lowpass را نشان می‌دهد.

## ترکیب روش‌ها

`combined_enhancement.py` زنجیره‌ای آموزشی شبیه منطق شکل 3-57 است: لاپلاسین برای جزئیات، Sobel برای لبه، هموارسازی گرادیان برای ماسک پیوسته‌تر، سپس افزودن mask و gamma برای نمایش. پارامترهای `lap_gain`, `sobel_smooth`, `gamma` قابل تغییرند.

## چه الگوریتم‌هایی افزوده‌اند و در متن فصل الزاماً نیستند؟

Sigmoid، asinh، Window/Level، CLAHE، Prewitt، Scharr، Bilateral و برخی order-statisticها برای توسعه آموزشی اضافه شده‌اند. این موارد در GUI با عبارت «افزوده» مشخص شده‌اند تا با محتوای اصلی کتاب اشتباه نشوند.
