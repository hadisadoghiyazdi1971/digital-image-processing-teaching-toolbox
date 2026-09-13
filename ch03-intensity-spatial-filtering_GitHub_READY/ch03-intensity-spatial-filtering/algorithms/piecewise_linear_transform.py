"""Three-segment piecewise-linear mapping with control points (r1,s1),(r2,s2)."""
import numpy as np
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, r1=0.25, s1=0.08, r2=0.75, s2=0.92):
    r = to_gray_float(image)
    r1,s1,r2,s2 = map(float,(r1,s1,r2,s2))
    if not (0 <= r1 < r2 <= 1): raise ValueError('Require 0 <= r1 < r2 <= 1')
    xp=np.array([0,r1,r2,1.0]); fp=np.array([0,s1,s2,1.0])
    return np.clip(np.interp(r, xp, fp), 0, 1)

if __name__ == '__main__': cli_single(apply, 'Piecewise linear transform', {'r1':.25,'s1':.08,'r2':.75,'s2':.92})
