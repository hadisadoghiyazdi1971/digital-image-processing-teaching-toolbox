"""Global histogram equalization, discrete image implementation."""
from skimage import exposure
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, nbins=256):
    return exposure.equalize_hist(to_gray_float(image), nbins=int(nbins))

if __name__ == '__main__': cli_single(apply, 'Global histogram equalization', {'nbins':256})
