"""Shared I/O helpers only. Algorithm mathematics live in each standalone module."""
from __future__ import annotations
from pathlib import Path
import numpy as np
from PIL import Image
from skimage import color, img_as_float


def to_gray_float(image):
    a = np.asarray(image)
    if a.ndim == 3:
        if a.shape[-1] == 4:
            a = a[..., :3]
        a = color.rgb2gray(a)
    a = img_as_float(a).astype(np.float64, copy=False)
    return np.clip(a, 0.0, 1.0)


def normalize01(a):
    a = np.asarray(a, dtype=np.float64)
    lo = np.nanmin(a); hi = np.nanmax(a)
    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
        return np.zeros_like(a, dtype=np.float64)
    return (a - lo) / (hi - lo)


def load_gray(path):
    return to_gray_float(Image.open(path))


def save_gray(path, image):
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    a = np.clip(np.asarray(image), 0, 1)
    Image.fromarray((a * 255 + 0.5).astype(np.uint8), mode='L').save(p)


def cli_single(apply_fn, description, defaults=None):
    import argparse
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument('--input', help='Input image. If omitted, skimage.data.camera() is used.')
    ap.add_argument('--output', default='output.png')
    ap.add_argument('--params', default='', help='Comma-separated key=value pairs, e.g. gamma=0.5,size=5')
    args = ap.parse_args()
    if args.input:
        im = load_gray(args.input)
    else:
        from skimage import data
        im = to_gray_float(data.camera())
    params = dict(defaults or {})
    if args.params.strip():
        for item in args.params.split(','):
            k, v = item.split('=', 1)
            k=k.strip(); v=v.strip()
            if v.lower() in {'true','false'}: v = v.lower() == 'true'
            else:
                try: v = int(v)
                except ValueError:
                    try: v = float(v)
                    except ValueError: pass
            params[k]=v
    out = apply_fn(im, **params)
    save_gray(args.output, out)
    print(f'Saved: {args.output}')
