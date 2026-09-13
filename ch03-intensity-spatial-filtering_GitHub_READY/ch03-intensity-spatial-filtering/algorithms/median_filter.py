"""Nonlinear median smoothing, especially effective against impulse noise."""
from scipy.ndimage import median_filter
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, size=3, boundary='reflect'):
    n=max(1,int(size)); return median_filter(to_gray_float(image),size=n,mode=str(boundary))

if __name__ == '__main__': cli_single(apply, 'Median filter', {'size':3,'boundary':'reflect'})
