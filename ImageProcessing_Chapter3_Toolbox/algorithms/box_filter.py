"""Normalized box (arithmetic mean) smoothing filter."""
from scipy.ndimage import uniform_filter
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, size=5, boundary='reflect'):
    n=max(1,int(size)); return uniform_filter(to_gray_float(image),size=n,mode=str(boundary))

if __name__ == '__main__': cli_single(apply, 'Box filter', {'size':5,'boundary':'reflect'})
