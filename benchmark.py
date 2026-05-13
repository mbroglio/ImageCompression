import numpy as np
import time
import matplotlib.pyplot as plt
from dct import custom_dct2, fast_dct2

def run_performance_test():
    """
    Test execution time of custom_dct2 (O(N^3)) vs scipy fast_dct2 (O(N^2 log N))
    Generates a semi-log plot up to a reasonable N that doesn't hang.
    """
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    custom_times = []
    fast_times = []

    print("Running Benchmark...")
    for N in sizes:
        print(f"Testing N={N}...")
        test_mat = np.random.rand(N, N)
        
        start = time.perf_counter()
        custom_dct2(test_mat)
        end = time.perf_counter()
        custom_times.append(end - start)
    
        start = time.perf_counter()
        fast_dct2(test_mat)
        end = time.perf_counter()
        fast_times.append(end - start)

    plt.figure(figsize=(10, 6))
    plt.title("Performance Comparison: Custom DCT2 vs Scipy DCT2")
    
    # We plot where custom_times is not nan
    valid_sizes = [sizes[i] for i in range(len(sizes)) if not np.isnan(custom_times[i])]
    valid_custom_times = [t for t in custom_times if not np.isnan(t)]
    
    plt.plot(valid_sizes, valid_custom_times, 'ro-', label="Custom DCT2 (O(N^3))")
    plt.plot(sizes, fast_times, 'bo-', label="Scipy Fast DCT2 (O(N^2 log N))")
    
    plt.yscale('log')
    plt.xlabel('Matrix Size (N x N)')
    plt.ylabel('Execution Time (seconds) - Log Scale')
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.tight_layout()
    plt.savefig('performance_comparison.png')
    plt.show()

if __name__ == "__main__":
    run_performance_test()
