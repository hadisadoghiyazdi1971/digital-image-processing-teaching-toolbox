# نگاشت بخش‌های فصل ۳ به کدها

| بخش آموزشی | فایل‌های اصلی |
|---|---|
| 3.1 مدل `g(x,y)=T[f(x,y)]` و `s=T(r)` | همه فایل‌های `*_transform.py` |
| 3.2 Negative / Log / Power / Piecewise / Threshold / Slicing / Bit planes | `negative_transform.py`, `log_transform.py`, `gamma_transform.py`, `piecewise_linear_transform.py`, `threshold_transform.py`, `intensity_slicing.py`, `bit_plane_slicing.py` |
| 3.3 Histogram equalization / specification / local processing / local statistics | `hist_equalization.py`, `hist_matching.py`, `local_hist_equalization.py`, `local_statistics_enhancement.py` |
| 3.4 Correlation / convolution / kernel composition / separability | `correlation_filter.py`, `convolution_filter.py`, `cascaded_convolution.py`, `separable_gaussian_demo.py` |
| 3.5 Smoothing spatial filters | `box_filter.py`, `gaussian_filter.py`, `median_filter.py` |
| 3.6 Sharpening: Laplacian / unsharp / highboost / gradient | `laplacian_sharpen.py`, `unsharp_mask.py`, `highboost_filter.py`, `roberts_gradient.py`, `sobel_gradient.py` |
| 3.7 Highpass / bandreject / bandpass from lowpass | `highpass_from_lowpass.py`, `bandpass_bandreject.py`; تصویر `zone_plate` در GUI |
| 3.8 Combining enhancement methods | `combined_enhancement.py` |
| توسعه خارج از هسته فصل | `sigmoid_transform.py`, `asinh_transform.py`, `window_level_transform.py`, `clahe_equalization.py`, `bilateral_filter.py`, `prewitt_gradient.py`, `scharr_gradient.py`, `order_statistic_filters.py` |

## نکته درباره استقلال فایل‌ها

هر فایل الگوریتمی یک `apply()` مستقل دارد و مستقیم نیز قابل اجراست. فقط `_common.py` برای کارهای غیرالگوریتمیِ تکراری (خواندن، خاکستری‌کردن، ذخیره و parser خط فرمان) مشترک است؛ بنابراین دانشجو می‌تواند فایل الگوریتم را جدا باز کند و منطق همان روش را در یک محل ببیند.
