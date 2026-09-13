"""Extra classical first-derivative operator: Prewitt gradient magnitude."""
from skimage.filters import prewitt
try:
    from algorithms._common import to_gray_float, normalize01, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, normalize01, cli_single

def apply(image): return normalize01(prewitt(to_gray_float(image)))
if __name__ == '__main__': cli_single(apply, 'Prewitt gradient')
