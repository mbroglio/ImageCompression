import numpy as np
import scipy.fftpack

def compute_D(N: int) -> np.ndarray:
    """
    Computes the standard N x N DCT matrix (DCT-II, orthonormal).
    Translated from the MATLAB logic:
    alpha_0 = 1 / sqrt(N)
    alpha_k = sqrt(2/N) for k > 0
    D(k, i) = alpha_k * cos(k * pi * (2*i + 1) / (2*N))
    """
    D = np.zeros((N, N))
    alpha = np.ones(N) * np.sqrt(2 / N)
    alpha[0] = 1 / np.sqrt(N)
    
    for k in range(N):
        for i in range(N):
            D[k, i] = alpha[k] * np.cos(k * np.pi * (2 * i + 1) / (2 * N))
    return D

def custom_dct1(f: np.ndarray) -> np.ndarray:
    """
    1D Discrete Cosine Transform using matrix multiplication setup.
    f: 1D numpy array
    """
    N = len(f)
    D = compute_D(N)
    return D @ f

def custom_idct1(c: np.ndarray) -> np.ndarray:
    """
    1D Inverse Discrete Cosine Transform.
    c: 1D numpy array
    """
    N = len(c)
    D = compute_D(N)
    return D.T @ c

def custom_dct2(f: np.ndarray) -> np.ndarray:
    """
    2D Discrete Cosine Transform implemented fundamentally via O(N^3)
    standard loops logic per row and column.
    """
    N, M = f.shape
    assert N == M, "Input must be a square matrix for this implementation"
    
    D = compute_D(N)
    c = np.zeros_like(f, dtype=float)
    
    # DCT1 on columns
    for j in range(N):
        c[:, j] = D @ f[:, j]
        
    # DCT1 on rows
    for i in range(N):
        c[i, :] = D @ c[i, :]
        
    return c

def custom_idct2(c: np.ndarray) -> np.ndarray:
    """
    2D Inverse Discrete Cosine Transform natively bounded to loops/matrix mult.
    """
    N, M = c.shape
    assert N == M, "Input must be a square matrix"
    
    D = compute_D(N)
    f = np.zeros_like(c, dtype=float)
    
    # IDCT1 on columns
    for j in range(N):
        f[:, j] = D.T @ c[:, j]
        
    # IDCT1 on rows
    for i in range(N):
        f[i, :] = D.T @ f[i, :]
        
    return f

def fast_dct2(f: np.ndarray) -> np.ndarray:
    """
    Fast 2D DCT using scipy.fftpack. O(N^2 log N).
    Needs to match our orthonormal scaling.
    """
    return scipy.fftpack.dct(scipy.fftpack.dct(f, axis=0, norm='ortho'), axis=1, norm='ortho')

def fast_idct2(c: np.ndarray) -> np.ndarray:
    """
    Fast 2D IDCT using scipy.fftpack.
    """
    return scipy.fftpack.idct(scipy.fftpack.idct(c, axis=0, norm='ortho'), axis=1, norm='ortho')

if __name__ == "__main__":
    # Small test logic
    f_test = np.random.rand(8, 8)
    
    c_custom = custom_dct2(f_test)
    c_fast = fast_dct2(f_test)
    
    print("Difference between custom and fast scipy DCT-II:", np.linalg.norm(c_custom - c_fast))
