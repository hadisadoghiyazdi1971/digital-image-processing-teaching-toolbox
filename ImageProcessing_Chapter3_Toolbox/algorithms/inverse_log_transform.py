"""Inverse-log/exponential family shown with the logarithmic transforms in Chapter 3."""
import numpy as np
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:
    from _common import to_gray_float, cli_single

def apply(image, alpha=5.0):
    r=to_gray_float(image); a=max(float(alpha),1e-9)
    # Normalized exponential map: 0->0 and 1->1.
    return np.expm1(a*r)/np.expm1(a)

if __name__ == '__main__': cli_single(apply, 'Inverse-log / exponential intensity transform', {'alpha':5.0})
