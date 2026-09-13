"""Gaussian lowpass smoothing; separable in standard implementations."""
from scipy.ndimage import gaussian_filter
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, sigma=2.0, boundary='reflect'):
    return gaussian_filter(to_gray_float(image),sigma=float(sigma),mode=str(boundary))

if __name__ == '__main__': cli_single(apply, 'Gaussian filter', {'sigma':2.0,'boundary':'reflect'})
