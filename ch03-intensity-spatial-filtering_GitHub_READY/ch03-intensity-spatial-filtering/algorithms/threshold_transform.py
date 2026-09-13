"""Binary thresholding as the limiting case of contrast stretching."""
import numpy as np
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, threshold=0.5, low=0.0, high=1.0):
    r=to_gray_float(image)
    return np.where(r >= float(threshold), float(high), float(low))

if __name__ == '__main__': cli_single(apply, 'Threshold transform', {'threshold':.5,'low':0.0,'high':1.0})
