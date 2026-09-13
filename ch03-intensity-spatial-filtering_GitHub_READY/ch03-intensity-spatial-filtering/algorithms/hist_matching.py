"""Histogram specification/matching: z = G^{-1}(T(r))."""
from skimage.exposure import match_histograms
try:
    from algorithms._common import to_gray_float
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float

def apply(image, reference):
    a=to_gray_float(image); b=to_gray_float(reference)
    return match_histograms(a,b,channel_axis=None)

if __name__ == '__main__':
    import argparse
    try:
        from algorithms._common import load_gray, save_gray
    except ModuleNotFoundError:
        from _common import load_gray, save_gray
    ap=argparse.ArgumentParser(description='Histogram matching')
    ap.add_argument('--input', required=True); ap.add_argument('--reference', required=True); ap.add_argument('--output', default='matched.png')
    a=ap.parse_args(); save_gray(a.output, apply(load_gray(a.input), load_gray(a.reference))); print('Saved:',a.output)
