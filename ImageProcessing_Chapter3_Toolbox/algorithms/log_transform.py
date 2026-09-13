"""Eq. (3-4): logarithmic dynamic-range compression."""
import numpy as np
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, c=1.0):
    r = to_gray_float(image)
    y = float(c) * np.log1p(r)
    return np.clip(y / np.log(2.0), 0, 1)

if __name__ == '__main__': cli_single(apply, 'Log transform', {'c':1.0})
