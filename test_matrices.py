import numpy as np
from dct import custom_dct1, custom_dct2, fast_dct2

# Reference 8x8 matrix provided in the assignment PDF
test_matrix_8x8 = np.array([
    [231,  32, 233, 161,  24,  71, 140, 245],
    [247,  40, 248, 245, 124, 204,  36, 107],
    [234, 202, 245, 167,   9, 217, 239, 173],
    [193, 190, 100, 167,  43, 180,   8,  70],
    [ 11,  24, 210, 177,  81, 243,   8, 112],
    [ 97, 195, 203,  47, 125, 114, 165, 181],
    [193,  70, 174, 167,  41,  30, 127, 245],
    [ 87, 149,  57, 192,  65, 129, 178, 228]
], dtype=float)

# Expected DCT2 output rounded to 2 decimal places (from e-notation in PDF)
expected_dct2_8x8 = np.array([
    [ 1.11e+03,  4.40e+01,  7.59e+01, -1.38e+02,  3.50e+00,  1.22e+02,  1.95e+02, -1.01e+02],
    [ 7.71e+01,  1.14e+02, -2.18e+01,  4.13e+01,  8.77e+00,  9.90e+01,  1.38e+02,  1.09e+01],
    [ 4.48e+01, -6.27e+01,  1.11e+02, -7.63e+01,  1.24e+02,  9.55e+01, -3.98e+01,  5.85e+01],
    [-6.99e+01, -4.02e+01, -2.34e+01, -7.67e+01,  2.66e+01, -3.68e+01,  6.61e+01,  1.25e+02],
    [-1.09e+02, -4.33e+01, -5.55e+01,  8.17e+00,  3.02e+01, -2.86e+01,  2.44e+00, -9.41e+01],
    [-5.38e+00,  5.66e+01,  1.73e+02, -3.54e+01,  3.23e+01,  3.34e+01, -5.81e+01,  1.90e+01],
    [ 7.88e+01, -6.45e+01,  1.18e+02, -1.50e+01, -1.37e+02, -3.06e+01, -1.05e+02,  3.98e+01],
    [ 1.97e+01, -7.81e+01,  9.72e-01, -7.23e+01, -2.15e+01,  8.13e+01,  6.37e+01,  5.90e+00]
])

# First row of the test matrix for 1D verification
test_vector_1D = test_matrix_8x8[0, :]

# Expected DCT1 output for the first row vector
expected_dct1_1D = np.array([
    4.01e+02,  6.60e+00,  1.09e+02, -1.12e+02, 6.54e+01,  1.21e+02,  1.16e+02,  2.88e+01
])

def run_tests():
    print("--- Running DCT Scaling Verification Tests ---")
    
    # Test 1D DCT on the first row
    result_dct1 = custom_dct1(test_vector_1D)
    
    print("\n1D DCT Result (first row):")
    print(result_dct1)
    print("Expected 1D DCT Result:")
    print(expected_dct1_1D)
    
    # We round to a single decimal place to check relative equality 
    # since expected values were rounded to 3 sig-figs dynamically in the PDF (e.g. 1.21e+02).
    diff1 = np.linalg.norm(result_dct1 - expected_dct1_1D) / np.linalg.norm(expected_dct1_1D)
    
    if diff1 < 0.05:
        print("-> 1D DCT Test: SUCCESS")
    else:
        print("-> 1D DCT Test: FAILED")
        
    # Test 2D Custom DCT
    result_dct2_custom = custom_dct2(test_matrix_8x8)
    
    print("\n2D Custom DCT2 Result:")
    print("Difference from expected:", np.linalg.norm(result_dct2_custom - expected_dct2_8x8) / np.linalg.norm(expected_dct2_8x8))
    
    # Test 2D Fast DCT
    result_dct2_fast = fast_dct2(test_matrix_8x8)
    
    diff2_custom = np.linalg.norm(result_dct2_custom - expected_dct2_8x8) / np.linalg.norm(expected_dct2_8x8)
    diff2_fast = np.linalg.norm(result_dct2_fast - expected_dct2_8x8) / np.linalg.norm(expected_dct2_8x8)
    
    if diff2_custom < 0.05:
        print("-> 2D Custom DCT Test: SUCCESS")
    else:
        print("-> 2D Custom DCT Test: FAILED")
        
    if diff2_fast < 0.05:
        print("-> 2D Fast Library DCT Test: SUCCESS")
    else:
        print("-> 2D Fast Library DCT Test: FAILED")
        
    print("\nIf all tests are SUCCESS, our ortho scaling identically matches the provided math lab requirements.")

if __name__ == "__main__":
    run_tests()
