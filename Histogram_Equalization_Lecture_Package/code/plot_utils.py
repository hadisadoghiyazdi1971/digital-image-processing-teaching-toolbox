from __future__ import annotations
from pathlib import Path
import math
from histogram_ops import Image, normalized_histogram, save_png_gray


def _blank(h: int, w: int, value: int = 255) -> Image:
    return [[value] * w for _ in range(h)]


def _line(img: Image, x0: int, y0: int, x1: int, y1: int, value: int = 0) -> None:
    dx = abs(x1-x0); sx = 1 if x0 < x1 else -1
    dy = -abs(y1-y0); sy = 1 if y0 < y1 else -1
    err = dx + dy
    h, w = len(img), len(img[0])
    while True:
        if 0 <= x0 < w and 0 <= y0 < h:
            img[y0][x0] = value
        if x0 == x1 and y0 == y1: break
        e2 = 2*err
        if e2 >= dy: err += dy; x0 += sx
        if e2 <= dx: err += dx; y0 += sy


def save_histogram(image: Image, path, title: str = "Histogram") -> None:
    p = normalized_histogram(image)
    W, H = 800, 450
    L, R, T, B = 60, 20, 25, 50
    canvas = _blank(H, W)
    _line(canvas, L, H-B, W-R, H-B, 0)
    _line(canvas, L, T, L, H-B, 0)
    peak = max(p) or 1.0
    prev = None
    for i, v in enumerate(p):
        x = L + round(i * (W-L-R-1) / 255)
        y = H-B - round(v / peak * (H-T-B-1))
        if prev is not None:
            _line(canvas, prev[0], prev[1], x, y, 32)
        prev = (x, y)
    # small grid marks; title is stored in companion .txt to keep stdlib-only plotting compact
    for i in range(0, 256, 32):
        x = L + round(i * (W-L-R-1) / 255)
        _line(canvas, x, H-B, x, H-B+5, 0)
    path = Path(path)
    save_png_gray(path, canvas)
    path.with_suffix(".txt").write_text(title + "\n", encoding="utf-8")


def save_joint_histogram(pxy: list[list[float]], path, title: str = "Joint histogram") -> None:
    bins = len(pxy)
    scale = 6
    W = H = bins * scale
    canvas = _blank(H, W)
    m = max(max(row) for row in pxy) or 1.0
    lm = math.log1p(m)
    for i in range(bins):
        for j in range(bins):
            q = math.log1p(pxy[i][j]) / lm if lm else 0.0
            val = 255 - int(round(255*q))
            y0 = (bins-1-i)*scale
            x0 = j*scale
            for y in range(y0, y0+scale):
                canvas[y][x0:x0+scale] = [val]*scale
    path = Path(path)
    save_png_gray(path, canvas)
    path.with_suffix(".txt").write_text(title + "\n", encoding="utf-8")
