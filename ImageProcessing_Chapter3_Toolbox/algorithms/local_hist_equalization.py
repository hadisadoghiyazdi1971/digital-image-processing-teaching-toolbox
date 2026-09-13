"""Local histogram equalization using a moving square footprint (rank filter)."""
import numpy as np
from skimage.filters import rank
from skimage.morphology import footprint_rectangle
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, size=31):
    r=(to_gray_float(image)*255+0.5).astype(np.uint8)
    s=max(3,int(size)); s += (s+1)%2
    out=rank.equalize(r, footprint=footprint_rectangle((s, s)))
    return out.astype(float)/255.0

if __name__ == '__main__': cli_single(apply, 'Local histogram equalization', {'size':31})
