"""Chapter-3 combination inspired by Fig. 3.57.
A positive-center Laplacian detail image is multiplied by a 5x5-smoothed Sobel magnitude,
added to the original, then a gamma transform expands dark intensities.
"""
import numpy as np
from scipy.ndimage import convolve, uniform_filter
from skimage.filters import sobel
try:
    from algorithms._common import to_gray_float, normalize01, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, normalize01, cli_single

def apply(image, lap_gain=1.0, sobel_smooth=5, gamma=0.5):
    f=to_gray_float(image)
    # Positive-center 8-neighbor Laplacian, so adding the response sharpens.
    lap_k=np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]],float)
    lap_detail=float(lap_gain)*convolve(f,lap_k,mode='reflect')
    grad=normalize01(sobel(f))
    n=max(1,int(sobel_smooth)); grad_s=uniform_filter(grad,size=n,mode='reflect')
    mask=lap_detail*grad_s
    enhanced=np.clip(f+mask,0,1)
    return np.power(enhanced,float(gamma))

if __name__ == '__main__': cli_single(apply, 'Combined Chapter-3 enhancement chain', {'lap_gain':1.0,'sobel_smooth':5,'gamma':0.5})
