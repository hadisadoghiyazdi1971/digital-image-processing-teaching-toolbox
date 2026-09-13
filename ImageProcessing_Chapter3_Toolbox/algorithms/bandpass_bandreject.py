"""Lowpass-derived bandpass/bandreject using two Gaussian scales.
Bandpass = LP(sigma_small)-LP(sigma_large); Bandreject = image-bandpass.
"""
import numpy as np
from scipy.ndimage import gaussian_filter
try:
    from algorithms._common import to_gray_float, normalize01, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, normalize01, cli_single

def apply(image, sigma_small=1.0, sigma_large=5.0, kind='bandpass', display_scale=True):
    f=to_gray_float(image); s1=float(sigma_small); s2=float(sigma_large)
    if s2 <= s1: raise ValueError('sigma_large must exceed sigma_small')
    bp=gaussian_filter(f,s1,mode='reflect')-gaussian_filter(f,s2,mode='reflect')
    out=bp if str(kind)=='bandpass' else f-bp
    return normalize01(out) if bool(display_scale) else np.clip(out,0,1)

if __name__ == '__main__': cli_single(apply, 'Bandpass/bandreject from lowpass', {'sigma_small':1.0,'sigma_large':5.0,'kind':'bandpass','display_scale':True})
