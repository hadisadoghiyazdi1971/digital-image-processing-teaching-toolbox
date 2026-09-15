from __future__ import annotations

from pathlib import Path
import math
import random
import struct
import zlib
from typing import Iterable

Image = list[list[int]]


def _shape(image: Image) -> tuple[int, int]:
    if not image or not image[0]:
        raise ValueError("empty image")
    w = len(image[0])
    if any(len(row) != w for row in image):
        raise ValueError("image rows must have equal length")
    return len(image), w


def ensure_uint8_gray(image: Image) -> Image:
    _shape(image)
    return [[0 if v < 0 else 255 if v > 255 else int(v) for v in row] for row in image]


def normalized_histogram(image: Image, levels: int = 256) -> list[float]:
    h, w = _shape(image)
    hist = [0] * levels
    for row in image:
        for v in row:
            hist[int(v)] += 1
    n = h * w
    return [c / n for c in hist]


def raw_histogram(image: Image, levels: int = 256) -> list[int]:
    _shape(image)
    hist = [0] * levels
    for row in image:
        for v in row:
            hist[int(v)] += 1
    return hist


def cdf_from_histogram(p: Iterable[float]) -> list[float]:
    values = list(float(x) for x in p)
    s = sum(values)
    if s <= 0:
        raise ValueError("histogram must have positive mass")
    out, acc = [], 0.0
    for x in values:
        acc += x / s
        out.append(acc)
    return out


def apply_lut(image: Image, lut: list[int]) -> Image:
    return [[lut[v] for v in row] for row in image]


def global_equalization(image: Image) -> tuple[Image, list[int]]:
    p = normalized_histogram(image)
    cdf = cdf_from_histogram(p)
    lut = [max(0, min(255, int(round(255.0 * c)))) for c in cdf]
    return apply_lut(image, lut), lut


def histogram_match(source: Image, reference: Image) -> tuple[Image, list[int]]:
    src_cdf = cdf_from_histogram(normalized_histogram(source))
    ref_cdf = cdf_from_histogram(normalized_histogram(reference))
    lut = [0] * 256
    q = 0
    for k, value in enumerate(src_cdf):
        while q < 255 and ref_cdf[q] < value:
            q += 1
        if q == 0:
            lut[k] = 0
        else:
            a = abs(ref_cdf[q] - value)
            b = abs(ref_cdf[q - 1] - value)
            lut[k] = q if a <= b else q - 1
    return apply_lut(source, lut), lut


def _clip_histogram(hist: list[int], clip_count: int) -> list[int]:
    clipped = hist[:]
    excess = 0
    for i, v in enumerate(clipped):
        if v > clip_count:
            excess += v - clip_count
            clipped[i] = clip_count
    if excess:
        base, rem = divmod(excess, 256)
        if base:
            clipped = [v + base for v in clipped]
        # spread remainder quasi-uniformly, avoiding a low-level bias
        if rem:
            step = max(1, 256 // rem)
            idx = 0
            for _ in range(rem):
                clipped[idx % 256] += 1
                idx += step
    return clipped


def _tile_lut(image: Image, y0: int, y1: int, x0: int, x1: int, clip_limit: float) -> list[int]:
    hist = [0] * 256
    n = 0
    for y in range(y0, y1):
        row = image[y]
        for x in range(x0, x1):
            hist[row[x]] += 1
            n += 1
    if n <= 0:
        return list(range(256))
    # Same normalized idea used by common CLAHE implementations:
    # clip_limit=1 means about average bin occupancy; 2 means twice that.
    clip_count = max(1, int(round(float(clip_limit) * n / 256.0)))
    hist = _clip_histogram(hist, clip_count)
    total = sum(hist)
    lut, acc = [0] * 256, 0
    for i, c in enumerate(hist):
        acc += c
        lut[i] = max(0, min(255, int(round(255.0 * acc / total))))
    return lut


def clahe_equalization(image: Image, clip_limit: float = 2.0, tile_grid=(8, 8)) -> Image:
    """Dependency-free CLAHE with clipped tile histograms and bilinear LUT interpolation."""
    h, w = _shape(image)
    gx, gy = int(tile_grid[0]), int(tile_grid[1])
    if gx <= 0 or gy <= 0:
        raise ValueError("tile_grid values must be positive")
    gx, gy = min(gx, w), min(gy, h)

    x_edges = [round(i * w / gx) for i in range(gx + 1)]
    y_edges = [round(i * h / gy) for i in range(gy + 1)]
    luts: list[list[list[int]]] = []
    for ty in range(gy):
        row_luts = []
        for tx in range(gx):
            row_luts.append(_tile_lut(image, y_edges[ty], y_edges[ty + 1], x_edges[tx], x_edges[tx + 1], clip_limit))
        luts.append(row_luts)

    out = [[0] * w for _ in range(h)]
    tw = w / gx
    th = h / gy
    for y in range(h):
        fy = (y + 0.5) / th - 0.5
        y0 = math.floor(fy)
        wy = fy - y0
        y1 = y0 + 1
        if y0 < 0:
            y0 = y1 = 0; wy = 0.0
        elif y1 >= gy:
            y0 = y1 = gy - 1; wy = 0.0
        for x in range(w):
            fx = (x + 0.5) / tw - 0.5
            x0 = math.floor(fx)
            wx = fx - x0
            x1 = x0 + 1
            if x0 < 0:
                x0 = x1 = 0; wx = 0.0
            elif x1 >= gx:
                x0 = x1 = gx - 1; wx = 0.0
            v = image[y][x]
            a = luts[y0][x0][v]
            b = luts[y0][x1][v]
            c = luts[y1][x0][v]
            d = luts[y1][x1][v]
            top = a * (1.0 - wx) + b * wx
            bot = c * (1.0 - wx) + d * wx
            out[y][x] = max(0, min(255, int(round(top * (1.0 - wy) + bot * wy))))
    return out


def image_mean(image: Image) -> float:
    h, w = _shape(image)
    return sum(sum(row) for row in image) / (h * w)


def image_std(image: Image) -> float:
    h, w = _shape(image)
    mu = image_mean(image)
    return math.sqrt(sum((v - mu) ** 2 for row in image for v in row) / (h * w))


def bbhe(image: Image) -> tuple[Image, list[int]]:
    hist = raw_histogram(image)
    mean_level = int(math.floor(image_mean(image)))
    lut = list(range(256))

    low = hist[: mean_level + 1]
    low_sum = sum(low)
    if low_sum:
        acc = 0
        for i, c in enumerate(low):
            acc += c
            lut[i] = max(0, min(mean_level, int(round(mean_level * acc / low_sum))))

    if mean_level < 255:
        lo = mean_level + 1
        high = hist[lo:]
        high_sum = sum(high)
        if high_sum:
            acc = 0
            span = 255 - lo
            for j, c in enumerate(high):
                acc += c
                lut[lo + j] = max(lo, min(255, int(round(lo + span * acc / high_sum))))

    return apply_lut(image, lut), lut


def shannon_entropy(image: Image) -> float:
    p = normalized_histogram(image)
    return -sum(v * math.log2(v) for v in p if v > 0)


def kl_to_uniform(image: Image) -> float:
    p = normalized_histogram(image)
    u = 1.0 / len(p)
    return sum(v * math.log2(v / u) for v in p if v > 0)


def ambe(a: Image, b: Image) -> float:
    return abs(image_mean(a) - image_mean(b))


def joint_histogram(a: Image, b: Image, bins: int = 64) -> list[list[float]]:
    ha, wa = _shape(a); hb, wb = _shape(b)
    if (ha, wa) != (hb, wb):
        raise ValueError("images must have the same shape for a joint histogram")
    counts = [[0] * bins for _ in range(bins)]
    for y in range(ha):
        for x in range(wa):
            ia = min(bins - 1, a[y][x] * bins // 256)
            ib = min(bins - 1, b[y][x] * bins // 256)
            counts[ia][ib] += 1
    n = ha * wa
    return [[c / n for c in row] for row in counts]


def mutual_information(a: Image, b: Image, bins: int = 64) -> float:
    pxy = joint_histogram(a, b, bins=bins)
    px = [sum(row) for row in pxy]
    py = [sum(pxy[i][j] for i in range(bins)) for j in range(bins)]
    total = 0.0
    for i in range(bins):
        for j in range(bins):
            p = pxy[i][j]
            if p > 0 and px[i] > 0 and py[j] > 0:
                total += p * math.log2(p / (px[i] * py[j]))
    return total


def roll_horizontal(image: Image, shift: int) -> Image:
    h, w = _shape(image)
    s = shift % w
    if not s:
        return [row[:] for row in image]
    return [row[-s:] + row[:-s] for row in image]


def shuffled_same_histogram(image: Image, seed: int = 11) -> Image:
    h, w = _shape(image)
    vals = [v for row in image for v in row]
    rng = random.Random(seed)
    rng.shuffle(vals)
    return [vals[y * w:(y + 1) * w] for y in range(h)]


def synthetic_low_contrast(size: int = 384) -> Image:
    rng = random.Random(7)
    out = [[0] * size for _ in range(size)]
    for y in range(size):
        for x in range(size):
            base = 92 + 36 * (x / max(1, size - 1))
            circle = 18 if (x-size*0.35)**2 + (y-size*0.45)**2 < (size*0.17)**2 else 0
            rectangle = -16 if (size*0.58 < x < size*0.86 and size*0.18 < y < size*0.52) else 0
            texture = 5 * math.sin(x / 13.0) + 4 * math.cos(y / 17.0)
            noise = rng.gauss(0, 2.5)
            v = int(round(base + circle + rectangle + texture + noise))
            out[y][x] = max(0, min(255, v))
    return out


def synthetic_reference(height: int = 384, width: int | None = None) -> Image:
    width = height if width is None else width
    out = [[0] * width for _ in range(height)]
    cx, cy = width / 2, height / 2
    for y in range(height):
        for x in range(width):
            radial = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            v = int(round(210 - 0.42 * radial + 18 * math.sin((x + y) / 24.0)))
            out[y][x] = max(25, min(240, v))
    return out


# ------------------------ dependency-free image I/O ------------------------

def _png_chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def save_png_gray(path: str | Path, image: Image) -> None:
    h, w = _shape(image)
    raw = bytearray()
    for row in image:
        raw.append(0)  # PNG filter: None
        raw.extend(max(0, min(255, int(v))) for v in row)
    payload = b"\x89PNG\r\n\x1a\n"
    payload += _png_chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0))
    payload += _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    payload += _png_chunk(b"IEND", b"")
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(payload)


def save_pgm(path: str | Path, image: Image) -> None:
    h, w = _shape(image)
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("wb") as f:
        f.write(f"P5\n{w} {h}\n255\n".encode("ascii"))
        for row in image:
            f.write(bytes(row))


def _read_pgm(path: Path) -> Image:
    data = path.read_bytes()
    pos = 0
    def token() -> bytes:
        nonlocal pos
        while pos < len(data):
            if data[pos:pos+1] == b"#":
                while pos < len(data) and data[pos:pos+1] not in (b"\n", b"\r"):
                    pos += 1
            elif data[pos:pos+1].isspace():
                pos += 1
            else:
                break
        start = pos
        while pos < len(data) and not data[pos:pos+1].isspace():
            pos += 1
        return data[start:pos]
    magic = token(); w = int(token()); h = int(token()); maxv = int(token())
    while pos < len(data) and data[pos:pos+1].isspace(): pos += 1
    if maxv <= 0:
        raise ValueError("invalid PGM max value")
    if magic == b"P5":
        if maxv > 255:
            raise ValueError("only 8-bit binary PGM is supported")
        pix = data[pos:pos+w*h]
        if len(pix) != w*h:
            raise ValueError("truncated PGM")
        return [list(pix[y*w:(y+1)*w]) for y in range(h)]
    if magic == b"P2":
        vals = []
        while len(vals) < w*h:
            t = token()
            if not t: break
            vals.append(round(int(t) * 255 / maxv))
        if len(vals) != w*h:
            raise ValueError("truncated ASCII PGM")
        return [vals[y*w:(y+1)*w] for y in range(h)]
    raise ValueError("unsupported PGM format")


def _read_bmp(path: Path) -> Image:
    data = path.read_bytes()
    if data[:2] != b"BM":
        raise ValueError("not a BMP file")
    off = struct.unpack_from("<I", data, 10)[0]
    dib = struct.unpack_from("<I", data, 14)[0]
    if dib < 40:
        raise ValueError("unsupported BMP header")
    w = struct.unpack_from("<i", data, 18)[0]
    h_signed = struct.unpack_from("<i", data, 22)[0]
    planes, bpp = struct.unpack_from("<HH", data, 26)
    comp = struct.unpack_from("<I", data, 30)[0]
    if planes != 1 or comp != 0 or bpp not in (8, 24, 32):
        raise ValueError("supported BMP: uncompressed 8/24/32-bit only")
    top_down = h_signed < 0
    h = abs(h_signed)
    if w <= 0 or h <= 0:
        raise ValueError("invalid BMP dimensions")
    palette = None
    if bpp == 8:
        colors_used = struct.unpack_from("<I", data, 46)[0] or 256
        palette = []
        p0 = 14 + dib
        for i in range(colors_used):
            b, g, r, _ = struct.unpack_from("<BBBB", data, p0 + 4*i)
            palette.append((r, g, b))
    stride = ((w * bpp + 31) // 32) * 4
    rows = [[0]*w for _ in range(h)]
    for out_y in range(h):
        src_y = out_y if top_down else h - 1 - out_y
        start = off + src_y * stride
        if bpp == 8:
            for x in range(w):
                idx = data[start+x]
                r,g,b = palette[idx] if palette and idx < len(palette) else (idx,idx,idx)
                rows[out_y][x] = int(round(0.299*r + 0.587*g + 0.114*b))
        else:
            px = bpp // 8
            for x in range(w):
                b, g, r = data[start + px*x:start + px*x + 3]
                rows[out_y][x] = int(round(0.299*r + 0.587*g + 0.114*b))
    return rows


def load_gray(path: str) -> Image:
    p = Path(path)
    ext = p.suffix.lower()
    if ext in (".pgm", ".pnm"):
        return _read_pgm(p)
    if ext == ".bmp":
        return _read_bmp(p)
    # Optional convenience only; never installed by RUN_ALL.bat.
    try:
        from PIL import Image as PILImage  # type: ignore
        im = PILImage.open(p).convert("L")
        w, h = im.size
        vals = list(im.getdata())
        return [vals[y*w:(y+1)*w] for y in range(h)]
    except ImportError as e:
        raise ValueError(
            "Dependency-free mode supports PGM and BMP inputs. "
            "PNG/JPEG input is also supported if Pillow is already installed, "
            "but Pillow is not required for the lecture demos."
        ) from e


def load_gray_or_synthetic(path: str | None) -> Image:
    return load_gray(path) if path else synthetic_low_contrast()


def save_image(path: str | Path, image: Image) -> None:
    p = Path(path)
    if p.suffix.lower() == ".pgm":
        save_pgm(p, image)
    else:
        save_png_gray(p, image)
