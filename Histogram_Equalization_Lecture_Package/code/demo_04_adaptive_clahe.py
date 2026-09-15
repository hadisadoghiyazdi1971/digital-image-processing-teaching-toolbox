from pathlib import Path
from histogram_ops import load_gray_or_synthetic, clahe_equalization, save_image
from plot_utils import save_histogram

def run(input_path=None, out_dir="outputs/04_clahe"):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    img = load_gray_or_synthetic(input_path)
    result = clahe_equalization(img, clip_limit=2.0, tile_grid=(8,8))
    save_image(out/"input.png", img); save_image(out/"clahe.png", result)
    save_histogram(img, out/"hist_input.png", "Input histogram")
    save_histogram(result, out/"hist_clahe.png", "CLAHE histogram")
if __name__ == "__main__": run()
