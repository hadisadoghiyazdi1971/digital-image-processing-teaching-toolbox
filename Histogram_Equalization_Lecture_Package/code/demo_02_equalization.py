from pathlib import Path
from histogram_ops import load_gray_or_synthetic, global_equalization, save_image
from plot_utils import save_histogram

def run(input_path=None, out_dir="outputs/02_global_equalization"):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    img = load_gray_or_synthetic(input_path)
    eq, lut = global_equalization(img)
    save_image(out/"input.png", img); save_image(out/"equalized.png", eq)
    save_histogram(img, out/"hist_input.png", "Input histogram")
    save_histogram(eq, out/"hist_equalized.png", "Equalized histogram")
    (out/"lut.csv").write_text("input,output\n" + "\n".join(f"{i},{v}" for i,v in enumerate(lut)), encoding="utf-8")
if __name__ == "__main__": run()
