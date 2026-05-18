import numpy as np
import time
import matplotlib.pyplot as plt
from dct import custom_dct2, fast_dct2

def run_performance_test():
    """
    Test execution time of custom_dct2 (O(N^3)) vs scipy fast_dct2 (O(N^2 log N))
    Generates a semi-log plot (log scale on y-axis) showing theoretical complexity curves.
    """
    custom_sizes = [16, 32, 64, 128, 256, 512, 1024]
    fast_sizes = [16, 32, 64, 128, 256, 512, 1024]
    custom_times = []
    fast_times = []

    print("Running Benchmark...")
    
    # Test custom_dct2 (O(N^3))
    print("\n--- Custom DCT2 (Matrix-based, O(N³)) ---")
    for N in custom_sizes:
        print(f"Testing N={N}...", end=" ")
        test_mat = np.random.rand(N, N)
        
        start = time.perf_counter()
        custom_dct2(test_mat)
        end = time.perf_counter()
        elapsed = end - start
        custom_times.append(elapsed)
        print(f"Time: {elapsed:.6f}s")
    
    # Test fast_dct2 (O(N^2 log N))
    print("\n--- Fast DCT2 (FFT-based, O(N² log N)) ---")
    for N in fast_sizes:
        print(f"Testing N={N}...", end=" ")
        test_mat = np.random.rand(N, N)
        
        start = time.perf_counter()
        fast_dct2(test_mat)
        end = time.perf_counter()
        elapsed = end - start
        fast_times.append(elapsed)
        print(f"Time: {elapsed:.6f}s")

    # Create semi-log plot (log scale on y-axis only)
    plt.figure(figsize=(10, 6))
    plt.title("Performance Comparison: Custom DCT2 vs Scipy DCT2", fontsize=14, fontweight='bold')
    
    plt.plot(custom_sizes, custom_times, 'ro-', linewidth=2, markersize=8, label="Custom DCT2 (O(N³))")
    plt.plot(fast_sizes, fast_times, 'bo-', linewidth=2, markersize=8, label="Scipy Fast DCT2 (O(N² log N))")
    
    plt.yscale('log')
    plt.xlabel('Matrix Size (N × N)', fontsize=12)
    plt.ylabel('Execution Time (seconds) - Log Scale', fontsize=12)
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend(fontsize=11, loc='upper left')
    plt.tight_layout()
    
    print("\nSaving plot to 'performance_comparison.png'...")
    plt.savefig('performance_comparison.png', dpi=150)
    plt.show()

if __name__ == "__main__":
    run_performance_test()
