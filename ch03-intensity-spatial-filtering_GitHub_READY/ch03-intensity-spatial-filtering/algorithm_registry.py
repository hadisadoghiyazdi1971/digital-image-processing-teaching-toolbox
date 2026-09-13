from importlib import import_module

A = {
'منفی (کتاب 3-3)': ('تبدیلات شدت','algorithms.negative_transform',[]),
'لگاریتمی (کتاب 3-4)': ('تبدیلات شدت','algorithms.log_transform',[('c','float',1.0)]),
'معکوس لگاریتمی / نمایی': ('تبدیلات شدت','algorithms.inverse_log_transform',[('alpha','float',5.0)]),
'گاما / توانی (کتاب 3-5)': ('تبدیلات شدت','algorithms.gamma_transform',[('gamma','float',0.5),('c','float',1.0)]),
'کشش کنتراست درصدی': ('تبدیلات شدت','algorithms.contrast_stretch',[('p_low','float',2.0),('p_high','float',98.0)]),
'خطی چندپاره': ('تبدیلات شدت','algorithms.piecewise_linear_transform',[('r1','float',0.25),('s1','float',0.08),('r2','float',0.75),('s2','float',0.92)]),
'آستانه‌گذاری': ('تبدیلات شدت','algorithms.threshold_transform',[('threshold','float',0.5),('low','float',0.0),('high','float',1.0)]),
'برش شدت': ('تبدیلات شدت','algorithms.intensity_slicing',[('low','float',0.35),('high','float',0.65),('highlight','float',1.0),('preserve_background','bool',True)]),
'صفحه بیت': ('تبدیلات شدت','algorithms.bit_plane_slicing',[('plane','int',7)]),
'سیگموید (افزوده)': ('تبدیلات شدت','algorithms.sigmoid_transform',[('cutoff','float',0.5),('gain','float',10.0)]),
'asinh (افزوده)': ('تبدیلات شدت','algorithms.asinh_transform',[('alpha','float',10.0)]),
'Window/Level (افزوده)': ('تبدیلات شدت','algorithms.window_level_transform',[('center','float',0.5),('width','float',0.5)]),
'همسان‌سازی سراسری': ('هیستوگرام','algorithms.hist_equalization',[('nbins','int',256)]),
'تطبیق هیستوگرام': ('هیستوگرام','algorithms.hist_matching',[('reference','reference',None)]),
'همسان‌سازی محلی': ('هیستوگرام','algorithms.local_hist_equalization',[('size','int',31)]),
'CLAHE (افزوده)': ('هیستوگرام','algorithms.clahe_equalization',[('kernel_size','int',32),('clip_limit','float',0.01),('nbins','int',256)]),
'تقویت آماری محلی (3-29)': ('هیستوگرام','algorithms.local_statistics_enhancement',[('window','int',3),('C','float',4.0),('k0','float',0.0),('k1','float',0.4),('k2','float',0.0),('k3','float',0.4)]),
'همبستگی 2D': ('اصول پالایش مکانی','algorithms.correlation_filter',[('kernel','str','0,-1,0;-1,5,-1;0,-1,0'),('boundary','enum','reflect',['reflect','nearest','mirror','wrap','constant']),('display_scale','bool',True)]),
'هم‌پیچش 2D': ('اصول پالایش مکانی','algorithms.convolution_filter',[('kernel','str','0,-1,0;-1,5,-1;0,-1,0'),('boundary','enum','reflect',['reflect','nearest','mirror','wrap','constant']),('display_scale','bool',True)]),
'گاوسی جدایی‌پذیر (آموزشی)': ('اصول پالایش مکانی','algorithms.separable_gaussian_demo',[('sigma','float',2.0),('output','enum','separable',['separable','difference'])]),
'هسته مرکب / آبشاری (آموزشی)': ('اصول پالایش مکانی','algorithms.cascaded_convolution',[('kernel1','str','1,2,1;2,4,2;1,2,1'),('kernel2','str','0,-1,0;-1,4,-1;0,-1,0'),('output','enum','difference',['cascade','composite','difference'])]),
'میانگین جعبه‌ای': ('هموارسازی','algorithms.box_filter',[('size','int',5),('boundary','enum','reflect',['reflect','nearest','mirror','wrap','constant'])]),
'گاوسی': ('هموارسازی','algorithms.gaussian_filter',[('sigma','float',2.0),('boundary','enum','reflect',['reflect','nearest','mirror','wrap','constant'])]),
'میانه': ('هموارسازی','algorithms.median_filter',[('size','int',3),('boundary','enum','reflect',['reflect','nearest','mirror','wrap','constant'])]),
'آمار ترتیبی (افزوده)': ('هموارسازی','algorithms.order_statistic_filters',[('kind','enum','midpoint',['min','max','midpoint']),('size','int',3),('boundary','enum','reflect',['reflect','nearest','mirror','wrap','constant'])]),
'دوطرفه Bilateral (افزوده)': ('هموارسازی','algorithms.bilateral_filter',[('sigma_color','float',0.08),('sigma_spatial','float',3.0)]),
'لاپلاسین و تیزسازی': ('تیزسازی','algorithms.laplacian_sharpen',[('connectivity','enum','8',['4','8']),('gain','float',1.0),('output','enum','sharpened',['sharpened','response'])]),
'Unsharp Mask': ('تیزسازی','algorithms.unsharp_mask',[('sigma','float',2.0),('amount','float',1.0)]),
'High-Boost': ('تیزسازی','algorithms.highboost_filter',[('sigma','float',2.0),('k','float',2.5)]),
'گرادیان Roberts': ('تیزسازی','algorithms.roberts_gradient',[]),
'گرادیان Prewitt (افزوده)': ('تیزسازی','algorithms.prewitt_gradient',[]),
'گرادیان Sobel': ('تیزسازی','algorithms.sobel_gradient',[]),
'گرادیان Scharr (افزوده)': ('تیزسازی','algorithms.scharr_gradient',[]),
'بالاگذر از پایین‌گذر': ('خانواده پالایه‌ها','algorithms.highpass_from_lowpass',[('sigma','float',2.0),('display_scale','bool',True)]),
'میان‌گذر / میان‌نگذر': ('خانواده پالایه‌ها','algorithms.bandpass_bandreject',[('sigma_small','float',1.0),('sigma_large','float',5.0),('kind','enum','bandpass',['bandpass','bandreject']),('display_scale','bool',True)]),
'زنجیره ترکیبی فصل 3': ('ترکیبی','algorithms.combined_enhancement',[('lap_gain','float',1.0),('sobel_smooth','int',5),('gamma','float',0.5)]),
}

def categories(): return sorted({v[0] for v in A.values()})
def algorithms_for(cat): return [k for k,v in A.items() if v[0]==cat]
def get(name): return A[name]
def load_apply(name): return import_module(A[name][1]).apply
