"""Shared image I/O and CLI helpers.

The mathematical implementation of each algorithm remains in its named module.
This file only provides repeated utilities so the standalone examples stay small.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
from PIL import Image
from skimage import color, img_as_float


def to_gray_float(image):
    """Convert an input image to float64 grayscale in the range [0, 1]."""
    a = np.asarray(image)
    if a.ndim == 3:
        if a.shape[-1] == 4:
            a = a[..., :3]
        a = color.rgb2gray(a)
    a = img_as_float(a).astype(np.float64, copy=False)
    return np.clip(a, 0.0, 1.0)


def normalize01(a):
    """Linearly scale an array to [0, 1] for display."""
    a = np.asarray(a, dtype=np.float64)
    lo = np.nanmin(a)
    hi = np.nanmax(a)
    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
        return np.zeros_like(a, dtype=np.float64)
    return (a - lo) / (hi - lo)


def load_gray(path):
    return to_gray_float(Image.open(path))


def save_gray(path, image):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    a = np.clip(np.asarray(image), 0, 1)
    Image.fromarray((a * 255 + 0.5).astype(np.uint8), mode="L").save(p)


def _auto_value(value):
    v = value.strip()
    if v.lower() in {"true", "false"}:
        return v.lower() == "true"
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v


def cli_single(apply_fn, description, defaults=None):
    """Small command-line wrapper used by every standalone algorithm module.

    Preferred syntax (safe for kernels containing commas):
        --param gamma=0.5 --param c=1.0
        --param "kernel=0,-1,0;-1,5,-1;0,-1,0"

    The older comma-separated ``--params`` syntax remains supported for simple
    scalar options, e.g. ``--params gamma=0.5,c=1``.
    """
    import argparse

    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--input", help="Input image. If omitted, skimage.data.camera() is used.")
    ap.add_argument("--output", default="output.png")
    ap.add_argument(
        "--param",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Repeatable parameter. Preferred for strings/kernels containing commas.",
    )
    ap.add_argument(
        "--params",
        default="",
        help="Legacy comma-separated key=value pairs for simple scalar parameters.",
    )
    args = ap.parse_args()

    if args.input:
        im = load_gray(args.input)
    else:
        from skimage import data
        im = to_gray_float(data.camera())

    params = dict(defaults or {})
    if args.params.strip():
        for item in args.params.split(","):
            if not item.strip():
                continue
            k, v = item.split("=", 1)
            params[k.strip()] = _auto_value(v)
    for item in args.param:
        k, v = item.split("=", 1)
        params[k.strip()] = _auto_value(v)

    out = apply_fn(im, **params)
    save_gray(args.output, out)
    print(f"Saved: {args.output}")
