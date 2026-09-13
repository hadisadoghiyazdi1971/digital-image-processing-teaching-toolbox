# نگاشت کامل فصل ۳ به فایل‌های کد

| بخش فصل | مفهوم | فایل/فایل‌های اصلی | وضعیت |
|---|---|---|---|
| 3.1 | مدل `g(x,y)=T[f(x,y)]` و `s=T(r)` | همه فایل‌های transform/filter | هسته فصل |
| 3.2 | Negative | `algorithms/negative_transform.py` | هسته فصل |
| 3.2 | Log | `algorithms/log_transform.py` | هسته فصل |
| 3.2 | Power/Gamma | `algorithms/gamma_transform.py` | هسته فصل |
| 3.2 | Contrast stretching / piecewise linear | `contrast_stretch.py`, `piecewise_linear_transform.py` | هسته فصل |
| 3.2 | Thresholding | `threshold_transform.py` | هسته فصل |
| 3.2 | Intensity-level slicing | `intensity_slicing.py` | هسته فصل |
| 3.2 | Bit-plane slicing | `bit_plane_slicing.py` | هسته فصل |
| 3.3 | Histogram equalization | `hist_equalization.py` | هسته فصل |
| 3.3 | Histogram matching/specification | `hist_matching.py` | هسته فصل |
| 3.3 | Local histogram processing | `local_hist_equalization.py` | هسته فصل |
| 3.3 | Local-statistics enhancement | `local_statistics_enhancement.py` | هسته فصل |
| 3.4 | Correlation | `correlation_filter.py` | هسته فصل |
| 3.4 | Convolution | `convolution_filter.py` | هسته فصل |
| 3.4 | Cascaded/composite kernel | `cascaded_convolution.py` | هسته فصل/آموزشی |
| 3.4 | Separable kernels | `separable_gaussian_demo.py` | هسته فصل/آموزشی |
| 3.5 | Box/Averaging lowpass | `box_filter.py` | هسته فصل |
| 3.5 | Gaussian lowpass | `gaussian_filter.py` | هسته فصل |
| 3.5 | Median / order statistic | `median_filter.py` | هسته فصل |
| 3.6 | Laplacian | `laplacian_sharpen.py` | هسته فصل |
| 3.6 | Unsharp masking | `unsharp_mask.py` | هسته فصل |
| 3.6 | High-boost | `highboost_filter.py` | هسته فصل |
| 3.6 | Roberts gradient | `roberts_gradient.py` | هسته فصل |
| 3.6 | Sobel gradient | `sobel_gradient.py` | هسته فصل |
| 3.7 | Highpass from lowpass | `highpass_from_lowpass.py` | هسته فصل |
| 3.7 | Bandpass / bandreject | `bandpass_bandreject.py` | هسته فصل |
| 3.7 | Zone plate | `image_sources.py` + GUI | هسته فصل/آزمایش |
| 3.8 | Combining enhancement methods | `combined_enhancement.py` | هسته فصل |
| توسعه | Inverse-log / exponential | `inverse_log_transform.py` | افزوده |
| توسعه | Sigmoid | `sigmoid_transform.py` | افزوده |
| توسعه | asinh | `asinh_transform.py` | افزوده |
| توسعه | Window/Level | `window_level_transform.py` | افزوده |
| توسعه | CLAHE | `clahe_equalization.py` | افزوده |
| توسعه | Bilateral | `bilateral_filter.py` | افزوده |
| توسعه | Prewitt | `prewitt_gradient.py` | افزوده |
| توسعه | Scharr | `scharr_gradient.py` | افزوده |
| توسعه | Min/Max/Midpoint order-statistic | `order_statistic_filters.py` | افزوده |

## استقلال فایل‌ها

هر الگوریتم تابع `apply()` خود را دارد و مستقیماً از خط فرمان نیز قابل اجراست. فایل `_common.py` فقط خواندن/ذخیره تصویر، نرمال‌سازی و parser مشترک خط فرمان را نگه می‌دارد؛ ریاضیات هر روش در فایل نام‌دار همان الگوریتم قرار دارد.
