import numpy as np
from PIL import Image
from dct import fast_dct2, fast_idct2

def compress_image(image_path: str, F: int, d: int) -> tuple[Image.Image, Image.Image]:
    """
    Compresses a grayscale image using block-based DCT.
    
    Args:
        image_path: Path to the .bmp image.
        F: Macro-block size (F x F).
        d: Frequency cutoff threshold (0 <= d <= 2F - 2).
        
    Returns:
        Tuple of (original_image, compressed_image) both as PIL Images.
    """
    # Load image and convert to grayscale
    orig_img = Image.open(image_path).convert('L')
    img_array = np.array(orig_img, dtype=float)
    
    H, W = img_array.shape
    
    # Discard edge remainders
    H_trunc = (H // F) * F
    W_trunc = (W // F) * F
    img_array = img_array[:H_trunc, :W_trunc]
    
    # Truncated original image for side-by-side comparison
    orig_img_trunc = Image.fromarray(np.uint8(np.clip(np.round(img_array), 0, 255)))
    
    compressed_array = np.zeros_like(img_array)
    
    # Process each FxF block
    for i in range(0, H_trunc, F):
        for j in range(0, W_trunc, F):
            # Extract block
            block = img_array[i:i+F, j:j+F]
            
            # Apply Fast DCT2
            dct_block = fast_dct2(block)
            
            # Zero out frequencies where k + l > d
            # Create indices grids using broadcasting
            k, l = np.ogrid[0:F, 0:F]
            mask = (k + l) > d
            dct_block[mask] = 0.0
            
            # Apply Fast IDCT2
            idct_block = fast_idct2(dct_block)
            
            # Place back into compressed array
            compressed_array[i:i+F, j:j+F] = idct_block
            
    # Round to nearest integer and clip to [0, 255]
    compressed_array = np.round(compressed_array)
    compressed_array = np.clip(compressed_array, 0, 255)
    
    compressed_img = Image.fromarray(np.uint8(compressed_array))
    
    return orig_img_trunc, compressed_img
