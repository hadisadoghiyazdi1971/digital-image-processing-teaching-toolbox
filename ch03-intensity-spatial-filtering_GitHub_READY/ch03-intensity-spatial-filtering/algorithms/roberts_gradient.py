"""Roberts cross first-derivative gradient magnitude."""
from skimage.filters import roberts
try:
    from algorithms._common import to_gray_float, normalize01, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, normalize01, cli_single

def apply(image): return normalize01(roberts(to_gray_float(image)))
if __name__ == '__main__': cli_single(apply, 'Roberts gradient')
