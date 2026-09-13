"""Eq. (3-34): 2-D spatial correlation with a user-supplied kernel."""
import numpy as np
from scipy.ndimage import correlate
try:
    from algorithms._common import to_gray_float, normalize01, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, normalize01, cli_single

def _kernel(text):
    if isinstance(text, str): return np.array([[float(v) for v in row.split(',')] for row in text.split(';')],dtype=float)
    return np.asarray(text,dtype=float)

def apply(image, kernel='0,-1,0;-1,5,-1;0,-1,0', boundary='reflect', display_scale=True):
    r=to_gray_float(image); k=_kernel(kernel)
    out=correlate(r,k,mode=str(boundary))
    return normalize01(out) if bool(display_scale) else np.clip(out,0,1)

if __name__ == '__main__': cli_single(apply, '2-D correlation', {'kernel':'0,-1,0;-1,5,-1;0,-1,0','boundary':'reflect','display_scale':True})
