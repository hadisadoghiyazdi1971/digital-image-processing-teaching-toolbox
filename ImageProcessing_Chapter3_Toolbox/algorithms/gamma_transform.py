"""Eq. (3-5): power-law (gamma) transform."""
import numpy as np
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, gamma=0.5, c=1.0):
    r = to_gray_float(image)
    return np.clip(float(c) * np.power(r, float(gamma)), 0, 1)

if __name__ == '__main__': cli_single(apply, 'Gamma transform', {'gamma':0.5,'c':1.0})
