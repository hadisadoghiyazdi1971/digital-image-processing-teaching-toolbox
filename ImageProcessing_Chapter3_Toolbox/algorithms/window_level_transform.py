"""Extra transform: medical-style window/level mapping."""
import numpy as np
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, center=0.5, width=0.5):
    r=to_gray_float(image); c=float(center); w=max(float(width),1e-6)
    lo=c-w/2; hi=c+w/2
    return np.clip((r-lo)/(hi-lo),0,1)

if __name__ == '__main__': cli_single(apply, 'Window/level transform', {'center':.5,'width':.5})
