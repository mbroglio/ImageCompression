import numpy as np
from PIL import Image
from dct import fast_dct2, fast_idct2

def compress_image(image_path: str, F: int, d: int) -> tuple[Image.Image, Image.Image]:
    """Compress a grayscale image with a JPEG-like block DCT algorithm.

    The image is divided into non-overlapping F x F pixel blocks f.
    For each block:
        c = DCT2(f)               -- apply 2D DCT
        c[k, l] = 0  if k+l >= d  -- zero out high-frequency coefficients
        f_hat = IDCT2(c)          -- reconstruct from surviving coefficients

    Parameters
    ----------
    image_path : str
        Path to a .bmp greyscale (or convertible) image.
    F : int
        Macro-block size. The image is partitioned into F x F squares.
        Pixels that do not fit exactly are discarded.
    d : int
        Frequency cutoff threshold (0 <= d <= 2*F-2).
        Coefficient c[k, l] is zeroed when k + l >= d.

    Returns
    -------
    (orig_img_trunc, compressed_img) : tuple of two PIL Images
        The truncated original and the reconstructed (compressed) image.
    """
    img_array = np.array(Image.open(image_path).convert('L'), dtype=float)
    H, W = img_array.shape
    
    H_trunc = (H // F) * F
    W_trunc = (W // F) * F
    img_array = img_array[:H_trunc, :W_trunc]
    
    orig_img_trunc = Image.fromarray(np.uint8(np.clip(np.round(img_array), 0, 255)))
    compressed_array = np.zeros_like(img_array)
    
    k, l = np.ogrid[:F, :F]
    mask = (k + l) >= d
    
    for i in range(0, H_trunc, F):
        for j in range(0, W_trunc, F):
            f = img_array[i:i+F, j:j+F]        # pixel block
            c = fast_dct2(f)                    # c = DCT2(f)
            c[mask] = 0.0                       # zero high-freq coefficients
            compressed_array[i:i+F, j:j+F] = fast_idct2(c)  # f_hat = IDCT2(c)
            
    compressed_array = np.clip(np.round(compressed_array), 0, 255)
    compressed_img = Image.fromarray(np.uint8(compressed_array))
    
    return orig_img_trunc, compressed_img
