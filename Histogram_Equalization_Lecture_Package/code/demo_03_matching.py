from pathlib import Path
from histogram_ops import load_gray_or_synthetic, load_gray, synthetic_reference, histogram_match, save_image
from plot_utils import save_histogram

def run(input_path=None, reference_path=None, out_dir="outputs/03_histogram_matching"):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    src = load_gray_or_synthetic(input_path)
    ref = load_gray(reference_path) if reference_path else synthetic_reference(len(src), len(src[0]))
    matched, lut = histogram_match(src, ref)
    for name, im in [("source",src),("reference",ref),("matched",matched)]:
        save_image(out/f"{name}.png", im)
        save_histogram(im, out/f"hist_{name}.png", f"{name.title()} histogram")
    (out/"lut.csv").write_text("input,output\n" + "\n".join(f"{i},{v}" for i,v in enumerate(lut)), encoding="utf-8")
if __name__ == "__main__": run()
