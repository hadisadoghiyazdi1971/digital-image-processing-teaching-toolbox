"""Extra rotationally improved 3x3 first-derivative operator: Scharr."""
from skimage.filters import scharr
try:
    from algorithms._common import to_gray_float, normalize01, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, normalize01, cli_single

def apply(image): return normalize01(scharr(to_gray_float(image)))
if __name__ == '__main__': cli_single(apply, 'Scharr gradient')
