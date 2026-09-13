"""Piecewise contrast stretching using percentile endpoints."""
import numpy as np
from skimage.exposure import rescale_intensity
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, p_low=2.0, p_high=98.0):
    r = to_gray_float(image)
    lo, hi = np.percentile(r, [float(p_low), float(p_high)])
    if hi <= lo: return r.copy()
    return rescale_intensity(r, in_range=(lo, hi), out_range=(0,1))

if __name__ == '__main__': cli_single(apply, 'Contrast stretch', {'p_low':2.0,'p_high':98.0})
