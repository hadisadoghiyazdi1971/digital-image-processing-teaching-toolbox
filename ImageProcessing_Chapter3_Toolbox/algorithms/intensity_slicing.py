"""Intensity-level slicing: highlight [low, high], optionally preserve background."""
import numpy as np
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, low=0.35, high=0.65, highlight=1.0, preserve_background=True):
    r=to_gray_float(image); low=float(low); high=float(high)
    mask=(r>=low)&(r<=high)
    if bool(preserve_background): out=r.copy()
    else: out=np.zeros_like(r)
    out[mask]=float(highlight)
    return np.clip(out,0,1)

if __name__ == '__main__': cli_single(apply, 'Intensity slicing', {'low':.35,'high':.65,'highlight':1.0,'preserve_background':True})
