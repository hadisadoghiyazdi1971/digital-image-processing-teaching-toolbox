"""Extra transform: logistic/sigmoid contrast remapping around a cutoff."""
import numpy as np
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, cutoff=0.5, gain=10.0):
    r=to_gray_float(image); c=float(cutoff); g=float(gain)
    y=1/(1+np.exp(-g*(r-c)))
    y0=1/(1+np.exp(g*c)); y1=1/(1+np.exp(-g*(1-c)))
    return np.clip((y-y0)/(y1-y0+1e-12),0,1)

if __name__ == '__main__': cli_single(apply, 'Sigmoid transform', {'cutoff':.5,'gain':10.0})
