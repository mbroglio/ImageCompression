import numpy as np
import scipy.fftpack

def compute_D(N: int) -> np.ndarray:
    """Computes the standard N x N DCT matrix (DCT-II, orthonormal)."""
    alpha = np.ones((N, 1)) * np.sqrt(2 / N)
    alpha[0, 0] = 1 / np.sqrt(N)
    i = np.arange(N)
    k = np.arange(N).reshape(-1, 1)
    return alpha * np.cos(k * np.pi * (2 * i + 1) / (2 * N))

def custom_dct1(f: np.ndarray) -> np.ndarray:
    """1D Discrete Cosine Transform using matrix multiplication."""
    return compute_D(len(f)) @ f

def custom_dct2(f: np.ndarray) -> np.ndarray:
    """
    2D Discrete Cosine Transform operating first on columns and then on rows,
    matching the exact iterative 1D logic explained in the lecture.
    """
    N = f.shape[0]
    D = compute_D(N)
    c = np.zeros_like(f, dtype=float)
    
    for j in range(N):
        c[:, j] = D @ f[:, j]
        
    for i in range(N):
        c[i, :] = D @ c[i, :]
        
    return c

def fast_dct2(f: np.ndarray) -> np.ndarray:
    """Fast 2D DCT using scipy.fftpack. O(N^2 log N)."""
    return scipy.fftpack.dct(scipy.fftpack.dct(f, axis=0, norm='ortho'), axis=1, norm='ortho')

def fast_idct2(c: np.ndarray) -> np.ndarray:
    """Fast 2D IDCT using scipy.fftpack."""
    return scipy.fftpack.idct(scipy.fftpack.idct(c, axis=0, norm='ortho'), axis=1, norm='ortho')
