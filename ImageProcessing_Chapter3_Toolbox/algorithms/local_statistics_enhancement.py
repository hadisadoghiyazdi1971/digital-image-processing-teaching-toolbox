"""Eq. (3-29): selective enhancement using local mean/std relative to global statistics."""
import numpy as np
from scipy.ndimage import uniform_filter
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, window=3, C=4.0, k0=0.0, k1=0.4, k2=0.0, k3=0.4):
    f=to_gray_float(image); n=max(3,int(window)); n += (n+1)%2
    mG=float(f.mean()); sG=float(f.std())
    m=uniform_filter(f,size=n,mode='reflect')
    m2=uniform_filter(f*f,size=n,mode='reflect')
    s=np.sqrt(np.maximum(m2-m*m,0))
    cond=(m>=float(k0)*mG)&(m<=float(k1)*mG)&(s>=float(k2)*sG)&(s<=float(k3)*sG)
    out=f.copy(); out[cond]=float(C)*out[cond]
    return np.clip(out,0,1)

if __name__ == '__main__': cli_single(apply, 'Local statistics enhancement', {'window':3,'C':4.0,'k0':0.0,'k1':0.4,'k2':0.0,'k3':0.4})
