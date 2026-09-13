"""Eqs. (3-50)-(3-54): Laplacian response and Laplacian sharpening."""
import numpy as np
from scipy.ndimage import convolve
try:
    from algorithms._common import to_gray_float, normalize01, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, normalize01, cli_single

def apply(image, connectivity=8, gain=1.0, output='sharpened'):
    f=to_gray_float(image); conn=int(connectivity)
    if conn==4: k=np.array([[0,1,0],[1,-4,1],[0,1,0]],float)
    elif conn==8: k=np.array([[1,1,1],[1,-8,1],[1,1,1]],float)
    else: raise ValueError('connectivity must be 4 or 8')
    lap=convolve(f,k,mode='reflect')
    if str(output)=='response': return normalize01(lap)
    # center-negative kernel => subtract response from original
    return np.clip(f - float(gain)*lap,0,1)

if __name__ == '__main__': cli_single(apply, 'Laplacian sharpening', {'connectivity':8,'gain':1.0,'output':'sharpened'})
