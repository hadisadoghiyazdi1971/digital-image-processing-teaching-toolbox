"""Eq. (3-43)/(3-44) idea: implement a 2-D Gaussian via two 1-D passes.
This shows separability explicitly instead of calling a 2-D Gaussian filter.
"""
import numpy as np
from scipy.ndimage import convolve1d, gaussian_filter
try:
    from algorithms._common import to_gray_float, normalize01, cli_single
except ModuleNotFoundError:
    from _common import to_gray_float, normalize01, cli_single

def _kernel1d(sigma, truncate=3.0):
    sigma=max(float(sigma),1e-6); radius=max(1,int(truncate*sigma+0.5))
    x=np.arange(-radius,radius+1,dtype=float)
    k=np.exp(-(x*x)/(2*sigma*sigma)); k/=k.sum(); return k

def apply(image, sigma=2.0, output='separable'):
    f=to_gray_float(image); k=_kernel1d(sigma)
    sep=convolve1d(convolve1d(f,k,axis=1,mode='reflect'),k,axis=0,mode='reflect')
    if str(output)=='separable': return sep
    direct=gaussian_filter(f,float(sigma),mode='reflect',truncate=3.0)
    if str(output)=='difference': return normalize01(np.abs(sep-direct))
    raise ValueError('output must be separable or difference')

if __name__ == '__main__': cli_single(apply, 'Separable Gaussian demo', {'sigma':2.0,'output':'separable'})
