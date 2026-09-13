# منابع کد و کتابخانه‌های مرجع

این پروژه کد کتاب را کپی نمی‌کند. پیاده‌سازی‌ها آموزشی‌اند و در جاهایی که مناسب بوده از APIهای پروژه‌های متن‌باز استاندارد استفاده می‌کنند.

- NumPy: https://github.com/numpy/numpy
- SciPy: https://github.com/scipy/scipy — به‌ویژه `scipy.ndimage` برای convolution/correlation/Gaussian/median/uniform filtering.
- scikit-image: https://github.com/scikit-image/scikit-image — `exposure`, `filters`, `restoration`, `data`.
- نمونه رسمی Histogram Matching در scikit-image: https://github.com/scikit-image/scikit-image/blob/main/doc/examples/color_exposure/plot_histogram_matching.py
- Pillow: https://github.com/python-pillow/Pillow — خواندن/ذخیره و نمایش تصاویر در GUI.
- Matplotlib: https://github.com/matplotlib/matplotlib — رسم histogram و contact sheet.

## اصل طراحی

برای مباحثی که هدف فصل فهم مکانیک است (مانند correlation/convolution، local statistics و خانواده highpass/bandpass از lowpass)، فرمول/ترکیب مستقیماً در کد نوشته شده است. برای عملیات استاندارد و بهینه‌شده مثل Gaussian، median، equalization و Sobel از کتابخانه‌های علمی تثبیت‌شده استفاده شده است.
