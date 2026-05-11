import numpy as np
from PIL import Image
from dct import fast_dct2, fast_idct2

def compress_image(image_path: str, F: int, d: int) -> tuple[Image.Image, Image.Image]:
    """
    Compresses a grayscale image using block-based DCT.
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
            block = img_array[i:i+F, j:j+F]
            dct_block = fast_dct2(block)
            dct_block[mask] = 0.0
            compressed_array[i:i+F, j:j+F] = fast_idct2(dct_block)
            
    compressed_array = np.clip(np.round(compressed_array), 0, 255)
    compressed_img = Image.fromarray(np.uint8(compressed_array))
    
    return orig_img_trunc, compressed_img
