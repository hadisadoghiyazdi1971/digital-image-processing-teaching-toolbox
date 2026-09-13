"""Extra order-statistic filters: minimum, maximum, midpoint."""
import numpy as np
from scipy.ndimage import minimum_filter, maximum_filter
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, kind='midpoint', size=3, boundary='reflect'):
    r=to_gray_float(image); n=max(1,int(size)); kind=str(kind).lower()
    lo=minimum_filter(r,size=n,mode=str(boundary)); hi=maximum_filter(r,size=n,mode=str(boundary))
    if kind=='min': return lo
    if kind=='max': return hi
    if kind=='midpoint': return 0.5*(lo+hi)
    raise ValueError('kind must be min, max, or midpoint')

if __name__ == '__main__': cli_single(apply, 'Order-statistic filter', {'kind':'midpoint','size':3,'boundary':'reflect'})
