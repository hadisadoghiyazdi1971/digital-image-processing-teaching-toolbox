"""Extra: CLAHE/adaptive histogram equalization with contrast limiting."""
from skimage import exposure
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, kernel_size=32, clip_limit=0.01, nbins=256):
    return exposure.equalize_adapthist(to_gray_float(image), kernel_size=int(kernel_size), clip_limit=float(clip_limit), nbins=int(nbins))

if __name__ == '__main__': cli_single(apply, 'CLAHE', {'kernel_size':32,'clip_limit':0.01,'nbins':256})
