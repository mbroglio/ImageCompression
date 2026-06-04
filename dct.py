import numpy as np
import scipy.fftpack

def compute_D(N: int) -> np.ndarray:
    """Computes the N x N DCT-II orthonormal matrix D.
    
    Entry D[k, n] = alpha_k * cos(pi*k*(2*n+1) / (2*N)), where
    alpha_0 = 1/sqrt(N) and alpha_k = sqrt(2/N) for k > 0.
    """
    alpha = np.ones((N, 1)) * np.sqrt(2 / N)
    alpha[0, 0] = 1 / np.sqrt(N)
    i = np.arange(N)
    k = np.arange(N).reshape(-1, 1)
    return alpha * np.cos(k * np.pi * (2 * i + 1) / (2 * N))

def custom_dct1(f: np.ndarray) -> np.ndarray:
    """1D DCT-II via matrix multiplication: C = D @ f.  O(N^2).
    
    Parameters
    ----------
    f : array of length N (the input signal/vector).
    
    Returns
    -------
    C : array of length N (DCT coefficients).
    """
    return compute_D(len(f)) @ f

def custom_dct2(f: np.ndarray) -> np.ndarray:
    """2D DCT-II via separable 1D transforms: C = D @ f @ D^T.  O(N^3).
    
    Applies the 1D DCT first along columns, then along rows, matching
    the iterative formulation explained in the lecture notes.
    In the compression context, N equals the macro-block size F.
    
    Parameters
    ----------
    f : square N x N input matrix (e.g. a grayscale pixel block).
    
    Returns
    -------
    C : N x N matrix of DCT coefficients.
    """
    N = f.shape[0]
    D = compute_D(N)
    c = np.zeros_like(f, dtype=float)
    
    for j in range(N):         # DCT along each column
        c[:, j] = D @ f[:, j]
        
    for i in range(N):         # DCT along each row of the intermediate result
        c[i, :] = D @ c[i, :]
        
    return c

def fast_dct2(f: np.ndarray) -> np.ndarray:
    """Fast 2D DCT-II using scipy.fftpack (FFT-based).  O(N^2 log N).
    
    Equivalent to C = D @ f @ D^T but computed via FFT.
    In the compression context N equals the macro-block size F.
    """
    return scipy.fftpack.dct(scipy.fftpack.dct(f, axis=0, norm='ortho'), axis=1, norm='ortho')

def fast_idct2(c: np.ndarray) -> np.ndarray:
    """Fast 2D IDCT-II using scipy.fftpack (FFT-based).  O(N^2 log N).
    
    Inverse of fast_dct2: reconstructs f from its DCT coefficients c.
    """
    return scipy.fftpack.idct(scipy.fftpack.idct(c, axis=0, norm='ortho'), axis=1, norm='ortho')
