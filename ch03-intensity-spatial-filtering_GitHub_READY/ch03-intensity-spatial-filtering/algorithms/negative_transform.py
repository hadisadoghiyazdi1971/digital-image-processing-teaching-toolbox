"""Eq. (3-3): image negative, s = 1-r for normalized intensity."""
import numpy as np
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image):
    r = to_gray_float(image)
    return 1.0 - r

if __name__ == '__main__': cli_single(apply, 'Negative intensity transform')
