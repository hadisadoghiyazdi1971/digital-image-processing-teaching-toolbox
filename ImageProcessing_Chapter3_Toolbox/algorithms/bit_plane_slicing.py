"""8-bit bit-plane slicing. plane=7 is MSB, plane=0 is LSB."""
import numpy as np
try:
    from algorithms._common import to_gray_float, cli_single
except ModuleNotFoundError:  # direct execution: python algorithms/<file>.py
    from _common import to_gray_float, cli_single

def apply(image, plane=7):
    r=(to_gray_float(image)*255+0.5).astype(np.uint8)
    p=int(plane)
    if not 0 <= p <= 7: raise ValueError('plane must be 0..7')
    return ((r >> p) & 1).astype(float)

if __name__ == '__main__': cli_single(apply, 'Bit-plane slicing', {'plane':7})
