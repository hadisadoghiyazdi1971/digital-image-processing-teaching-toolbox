from pathlib import Path
from histogram_ops import load_gray_or_synthetic, normalized_histogram, save_image
from plot_utils import save_histogram

def run(input_path=None, out_dir="outputs/01_histogram"):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    img = load_gray_or_synthetic(input_path)
    save_image(out/"input.png", img)
    save_histogram(img, out/"histogram.png", "Normalized histogram")
    p = normalized_histogram(img)
    (out/"histogram.csv").write_text("gray_level,probability\n" + "\n".join(f"{i},{v:.12g}" for i,v in enumerate(p)), encoding="utf-8")
if __name__ == "__main__": run()
