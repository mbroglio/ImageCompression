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
    print("=" * 90)
    print("TEST DCT 1D - PRIMA RIGA DEL BLOCCHETTO 8×8")
    print("=" * 90)
    
    print(f"\nVettore di input (prima riga):")
    print(test_vector_1D)
    
    result_dct1 = custom_dct1(test_vector_1D)
    
    print(f"\nRisultato DCT 1D (custom_dct1):")
    print(result_dct1)
    
    print(f"\nValori attesi (da assignment):")
    print(expected_dct1_1D)
    
    # Calcolo errore
    errore_1d = np.abs(result_dct1 - expected_dct1_1D)
    errore_relativo_1d = 100 * np.linalg.norm(errore_1d) / np.linalg.norm(expected_dct1_1D)
    
    print(f"\nErrore assoluto massimo: {np.max(errore_1d):.6e}")
    print(f"Errore relativo (norma L2): {errore_relativo_1d:.6f}%")
    
    print("\nDettaglio confronto elemento per elemento:")
    print(f"{'Indice':<8} {'Risultato':<15} {'Atteso':<15} {'Errore':<15}")
    print("-" * 55)
    for i in range(len(result_dct1)):
        err = abs(result_dct1[i] - expected_dct1_1D[i])
        print(f"{i:<8} {result_dct1[i]:<15.6e} {expected_dct1_1D[i]:<15.6e} {err:<15.6e}")
    
    tolerance_1d = 5.0  # 5%
    if errore_relativo_1d < tolerance_1d:
        print(f"\n✓ TEST DCT 1D SUPERATO (errore {errore_relativo_1d:.6f}% < {tolerance_1d}%)")
    else:
        print(f"\n✗ TEST DCT 1D FALLITO (errore {errore_relativo_1d:.6f}% >= {tolerance_1d}%)")
        
    # Test 2D DCT on the full matrix
    print("\n" + "=" * 90)
    print("TEST DCT 2D - BLOCCHETTO 8×8 COMPLETO")
    print("=" * 90)
    
    print(f"\nMatrice di input:")
    print(test_matrix_8x8)
    
    result_dct2_custom = custom_dct2(test_matrix_8x8)
    
    print(f"\nRisultato DCT 2D (custom_dct2):")
    print(result_dct2_custom)
    
    print(f"\nValori attesi (da assignment):")
    print(expected_dct2_8x8)
    
    # Calcolo errore 2D
    errore_2d = np.abs(result_dct2_custom - expected_dct2_8x8)
    errore_relativo_2d = 100 * np.linalg.norm(errore_2d) / np.linalg.norm(expected_dct2_8x8)
    
    print(f"\nErrore assoluto massimo: {np.max(errore_2d):.6e}")
    print(f"Errore relativo (norma L2): {errore_relativo_2d:.6f}%")
    
    print("\nDettaglio confronto (primis 3 elementi della prima riga):")
    print(f"{'Risultato':<15} {'Atteso':<15} {'Errore':<15}")
    print("-" * 45)
    for i in range(3):
        err = abs(result_dct2_custom[0, i] - expected_dct2_8x8[0, i])
        print(f"{result_dct2_custom[0, i]:<15.6e} {expected_dct2_8x8[0, i]:<15.6e} {err:<15.6e}")
    
    tolerance_2d = 5.0  # 5%
    if errore_relativo_2d < tolerance_2d:
        print(f"\n✓ TEST DCT 2D (CUSTOM) SUPERATO (errore {errore_relativo_2d:.6f}% < {tolerance_2d}%)")
    else:
        print(f"\n✗ TEST DCT 2D (CUSTOM) FALLITO (errore {errore_relativo_2d:.6f}% >= {tolerance_2d}%)")
    
    # Test 2D Fast DCT
    print("\n" + "=" * 90)
    print("TEST DCT 2D - IMPLEMENTAZIONE VELOCE (scipy)")
    print("=" * 90)
    
    result_dct2_fast = fast_dct2(test_matrix_8x8)
    
    errore_2d_fast = np.abs(result_dct2_fast - expected_dct2_8x8)
    errore_relativo_2d_fast = 100 * np.linalg.norm(errore_2d_fast) / np.linalg.norm(expected_dct2_8x8)
    
    print(f"\nErrore assoluto massimo: {np.max(errore_2d_fast):.6e}")
    print(f"Errore relativo (norma L2): {errore_relativo_2d_fast:.6f}%")
    
    if errore_relativo_2d_fast < tolerance_2d:
        print(f"✓ TEST DCT 2D (FAST) SUPERATO (errore {errore_relativo_2d_fast:.6f}% < {tolerance_2d}%)")
    else:
        print(f"✗ TEST DCT 2D (FAST) FALLITO (errore {errore_relativo_2d_fast:.6f}% >= {tolerance_2d}%)")
    
    # Test consistenza fra custom e fast
    print("\n" + "=" * 90)
    print("TEST CONSISTENZA: custom_dct2 vs fast_dct2")
    print("=" * 90)
    
    differenza_custom_vs_fast = np.linalg.norm(result_dct2_custom - result_dct2_fast)
    print(f"\nDifferenza (norma L2) fra custom_dct2 e fast_dct2: {differenza_custom_vs_fast:.6e}")
    
    if differenza_custom_vs_fast < 1e-10:
        print("✓ Le due implementazioni sono numericamente identiche")
    else:
        print(f"⚠ Differenza rilevabile tra le implementazioni (< 1e-10)")
    
    # Test ortonormalità
    print("\n" + "=" * 90)
    print("TEST ORTONORMALITÀ: IDCT(DCT(x)) = x")
    print("=" * 90)
    
    from dct import fast_idct2
    
    reconstructed = fast_idct2(result_dct2_custom)
    reconstruction_error = np.linalg.norm(reconstructed - test_matrix_8x8) / np.linalg.norm(test_matrix_8x8)
    reconstruction_error_max = np.max(np.abs(reconstructed - test_matrix_8x8))
    
    print(f"\nErrore di ricostruzione relativo: {reconstruction_error:.6e}")
    print(f"Errore massimo elemento: {reconstruction_error_max:.6e}")
    
    if reconstruction_error < 1e-10:
        print("✓ La proprietà di ortonormalità è verificata")
    else:
        print("✗ La proprietà di ortonormalità NON è verificata")
    
    # Riepilogo
    print("\n" + "=" * 90)
    print("RIEPILOGO RISULTATI")
    print("=" * 90)
    
    all_pass = (
        errore_relativo_1d < tolerance_1d and 
        errore_relativo_2d < tolerance_2d and 
        errore_relativo_2d_fast < tolerance_2d and
        reconstruction_error < 1e-10
    )
    
    print(f"DCT 1D:           {'✓ PASS' if errore_relativo_1d < tolerance_1d else '✗ FAIL'}")
    print(f"DCT 2D (Custom):  {'✓ PASS' if errore_relativo_2d < tolerance_2d else '✗ FAIL'}")
    print(f"DCT 2D (Fast):    {'✓ PASS' if errore_relativo_2d_fast < tolerance_2d else '✗ FAIL'}")
    print(f"Ortonormalità:    {'✓ PASS' if reconstruction_error < 1e-10 else '✗ FAIL'}")
    print(f"\nRisultato globale: {'✓✓✓ TUTTI I TEST SUPERATI ✓✓✓' if all_pass else '✗✗✗ ALCUNI TEST FALLITI ✗✗✗'}")

if __name__ == "__main__":
    run_tests()
