"""Eq. (3-38): compare a cascade of two convolutions with one composite kernel."""
import numpy as np
from scipy.ndimage import convolve
from scipy.signal import convolve2d
try:
    from algorithms._common import to_gray_float, normalize01, cli_single
except ModuleNotFoundError:
    from _common import to_gray_float, normalize01, cli_single

def _k(text):
    return np.array([[float(v) for v in row.split(',')] for row in str(text).split(';')],float)

def apply(image, kernel1='1,2,1;2,4,2;1,2,1', kernel2='0,-1,0;-1,4,-1;0,-1,0', output='difference'):
    f=to_gray_float(image); k1=_k(kernel1); k2=_k(kernel2)
    if k1.sum()!=0: k1=k1/k1.sum()
    casc=convolve(convolve(f,k1,mode='reflect'),k2,mode='reflect')
    comp=convolve2d(k1,k2,mode='full')
    one=convolve(f,comp,mode='reflect')
    if str(output)=='cascade': return normalize01(casc)
    if str(output)=='composite': return normalize01(one)
    if str(output)=='difference': return normalize01(np.abs(casc-one))
    raise ValueError('output must be cascade, composite, or difference')

if __name__ == '__main__': cli_single(apply, 'Cascade versus composite-kernel convolution', {'kernel1':'1,2,1;2,4,2;1,2,1','kernel2':'0,-1,0;-1,4,-1;0,-1,0','output':'difference'})
