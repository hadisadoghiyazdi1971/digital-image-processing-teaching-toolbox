"""Extra edge-preserving smoother using scikit-image bilateral denoising."""
from skimage.restoration import denoise_bilateral
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, sigma_color=0.08, sigma_spatial=3.0):
    return denoise_bilateral(to_gray_float(image), sigma_color=float(sigma_color), sigma_spatial=float(sigma_spatial), channel_axis=None)

if __name__ == '__main__': cli_single(apply, 'Bilateral filter', {'sigma_color':0.08,'sigma_spatial':3.0})
