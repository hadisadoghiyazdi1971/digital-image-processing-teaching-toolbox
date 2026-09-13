"""Chapter 3 relation hp = delta-lp, implemented as image - lowpass(image)."""
from scipy.ndimage import gaussian_filter
try:
    from algorithms._common import to_gray_float, normalize01, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, normalize01, cli_single

def apply(image, sigma=2.0, display_scale=True):
    f=to_gray_float(image); hp=f-gaussian_filter(f,float(sigma),mode='reflect')
    return normalize01(hp) if bool(display_scale) else hp

if __name__ == '__main__': cli_single(apply, 'Highpass from lowpass', {'sigma':2.0,'display_scale':True})
