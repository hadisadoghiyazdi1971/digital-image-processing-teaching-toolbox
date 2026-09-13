"""Extra transform: asinh compression, useful for large dynamic range without log singularity."""
import numpy as np
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, alpha=10.0):
    r=to_gray_float(image); a=max(float(alpha),1e-9)
    return np.arcsinh(a*r)/np.arcsinh(a)

if __name__ == '__main__': cli_single(apply, 'Asinh transform', {'alpha':10.0})
