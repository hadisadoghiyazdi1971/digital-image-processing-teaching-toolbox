"""Eq. (3-56) with k>1: high-boost filtering."""
import numpy as np
from scipy.ndimage import gaussian_filter
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, sigma=2.0, k=2.5):
    f=to_gray_float(image); blur=gaussian_filter(f,float(sigma),mode='reflect'); mask=f-blur
    return np.clip(f+float(k)*mask,0,1)

if __name__ == '__main__': cli_single(apply, 'High-boost filter', {'sigma':2.0,'k':2.5})
