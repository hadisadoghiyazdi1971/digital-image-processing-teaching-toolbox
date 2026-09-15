from pathlib import Path
from histogram_ops import load_gray_or_synthetic, bbhe, save_image
from plot_utils import save_histogram

def run(input_path=None, out_dir="outputs/05_bbhe"):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    img = load_gray_or_synthetic(input_path)
    result, lut = bbhe(img)
    save_image(out/"input.png", img); save_image(out/"bbhe.png", result)
    save_histogram(result, out/"hist_bbhe.png", "BBHE histogram")
    (out/"lut.csv").write_text("input,output\n" + "\n".join(f"{i},{v}" for i,v in enumerate(lut)), encoding="utf-8")
if __name__ == "__main__": run()
