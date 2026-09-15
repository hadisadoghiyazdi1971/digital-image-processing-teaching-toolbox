from pathlib import Path
from histogram_ops import (load_gray_or_synthetic, global_equalization, shannon_entropy,
    kl_to_uniform, mutual_information, joint_histogram, save_image, roll_horizontal,
    shuffled_same_histogram)
from plot_utils import save_joint_histogram

def run(input_path=None, out_dir="outputs/06_information_theory"):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    img = load_gray_or_synthetic(input_path)
    eq, _ = global_equalization(img)
    shifted = roll_horizontal(img, 12)
    shuffled = shuffled_same_histogram(img, 11)
    values = {
        "entropy_input_bits": shannon_entropy(img),
        "entropy_equalized_bits": shannon_entropy(eq),
        "kl_input_to_uniform_bits": kl_to_uniform(img),
        "kl_equalized_to_uniform_bits": kl_to_uniform(eq),
        "mi_input_with_itself_bits": mutual_information(img, img),
        "mi_input_with_shifted_bits": mutual_information(img, shifted),
        "mi_input_with_shuffled_bits": mutual_information(img, shuffled),
    }
    (out/"metrics.txt").write_text("\n".join(f"{k} = {v:.6f}" for k,v in values.items()) + "\n", encoding="utf-8")
    save_image(out/"input.png", img); save_image(out/"equalized.png", eq)
    save_image(out/"shifted.png", shifted); save_image(out/"shuffled_same_histogram.png", shuffled)
    save_joint_histogram(joint_histogram(img, shifted), out/"joint_hist_input_shifted.png", "Joint histogram: input vs shifted")
if __name__ == "__main__": run()
