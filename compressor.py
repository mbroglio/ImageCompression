import numpy as np
from PIL import Image
from dct import fast_dct2, fast_idct2


def compress_image(image_path: str, F: int, d: int) -> tuple[Image.Image, Image.Image]:
    """
    Compress a grayscale image with a block DCT algorithm
    """
    img_array = np.array(Image.open(image_path).convert("L"), dtype=float)
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
            f = img_array[i : i + F, j : j + F]  # pixel block
            c = fast_dct2(f)  # c = DCT2(f)
            c[mask] = 0.0  # zero high-freq coefficients
            compressed_array[i : i + F, j : j + F] = fast_idct2(c)  # f_hat = IDCT2(c)

    compressed_array = np.clip(np.round(compressed_array), 0, 255)
    compressed_img = Image.fromarray(np.uint8(compressed_array))

    return orig_img_trunc, compressed_img
