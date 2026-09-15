from __future__ import annotations
import argparse
from pathlib import Path

from demo_01_histogram import run as run1
from demo_02_equalization import run as run2
from demo_03_matching import run as run3
from demo_04_adaptive_clahe import run as run4
from demo_05_bbhe import run as run5
from demo_06_information_theory import run as run6
from histogram_ops import (load_gray_or_synthetic, global_equalization, clahe_equalization,
    bbhe, shannon_entropy, kl_to_uniform, ambe, image_mean, image_std)

def main():
    parser = argparse.ArgumentParser(description="Dependency-free histogram processing demos for Python 3.12")
    parser.add_argument("--input", default=None, help="optional grayscale PGM/BMP input; PNG/JPEG works if Pillow already exists")
    parser.add_argument("--reference", default=None, help="optional reference PGM/BMP for histogram matching")
    args = parser.parse_args()

    Path("outputs").mkdir(exist_ok=True)
    run1(args.input); run2(args.input); run3(args.input, args.reference); run4(args.input); run5(args.input); run6(args.input)

    img = load_gray_or_synthetic(args.input)
    he, _ = global_equalization(img)
    cl = clahe_equalization(img)
    bh, _ = bbhe(img)
    rows = [("input", img), ("global_he", he), ("clahe", cl), ("bbhe", bh)]
    lines = ["method,mean,std,entropy_bits,kl_to_uniform_bits,ambe_vs_input"]
    for name, arr in rows:
        lines.append(f"{name},{image_mean(arr):.6f},{image_std(arr):.6f},{shannon_entropy(arr):.6f},{kl_to_uniform(arr):.6f},{ambe(img,arr):.6f}")
    Path("outputs/summary_metrics.csv").write_text("\n".join(lines)+"\n", encoding="utf-8")
    print("Done. Results are in the outputs folder.")

if __name__ == "__main__": main()
