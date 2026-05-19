import numpy as np
from PIL import Image
import time
import csv
from compressor import compress_image

def calculate_psnr(original, compressed):
    """
    Calcola il PSNR tra immagine originale e compressa.
    
    PSNR = 10 * log10(255^2 / MSE)
    """
    # Converte entrambe a float per il calcolo
    orig_array = np.array(original, dtype=float)
    comp_array = np.array(compressed, dtype=float)
    
    # Calcola MSE
    mse = np.mean((orig_array - comp_array) ** 2)
    
    if mse == 0:
        return float('inf')
    
    psnr = 10 * np.log10(255**2 / mse)
    return psnr

def run_compression_tests():
    """
    Esegue i test di compressione su immagini reali con parametri variabili.
    Calcola il tempo di esecuzione e salva i risultati in CSV.
    """
    
    # Definizione test: (nome_immagine, parametri)
    # parametri: lista di (F, d)
    tests = [
        ("gradient.bmp", [(8, 4), (8, 8), (8, 12), (8, 14)]),
        ("bridge.bmp", [(8, 4), (8, 8), (8, 12), (16, 16)]),
        ("shoe.bmp", [(8, 4), (8, 8), (8, 12), (4, 6)]),
    ]
    
    print("=" * 90)
    print("VALIDAZIONE COMPRESSIONE DCT - ESPERIMENTI SU IMMAGINI REALI")
    print("=" * 90)
    
    results = []
    
    for img_name, params in tests:
        image_path = f"images/{img_name}"
        
        try:
            # Carica l'immagine originale (grayscale)
            original_img = Image.open(image_path).convert('L')
            original_array = np.array(original_img, dtype=float)
            width, height = original_img.size
            resolution = f"{width}×{height}"
            
            print(f"\n{'─' * 90}")
            print(f"Immagine: {img_name} ({resolution})")
            print(f"{'─' * 90}")
            print(f"{'F':>3} | {'d':>3} | {'Tempo (ms)':>12}")
            print(f"{'-'*3}-+-{'-'*3}-+-{'-'*12}")
            
            for F, d in params:
                # Misura il tempo di compressione
                start_time = time.perf_counter()
                orig_img_trunc, compressed_img = compress_image(image_path, F, d)
                end_time = time.perf_counter()
                
                elapsed_ms = (end_time - start_time) * 1000
                
                # Formatta i risultati
                time_str = f"{elapsed_ms:.1f}"
                
                print(f"{F:>3} | {d:>3} | {time_str:>12}")
                
                results.append({
                    'image': img_name,
                    'resolution': resolution,
                    'F': F,
                    'd': d,
                    'time_ms': elapsed_ms
                })
                
        except FileNotFoundError:
            print(f"⚠ Immagine non trovata: {image_path}")
        except Exception as e:
            print(f"❌ Errore durante l'elaborazione di {img_name}: {e}")
    
    # Salva i risultati in CSV
    csv_file = "compression_results.csv"
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['image', 'resolution', 'F', 'd', 'time_ms'])
            writer.writeheader()
            writer.writerows(results)
        print(f"\n{'=' * 90}")
        print(f"✓ Risultati salvati in: {csv_file}")
        print(f"{'=' * 90}")
    except Exception as e:
        print(f"❌ Errore durante il salvataggio del CSV: {e}")
    
    # Stampa un riepilogo in formato LaTeX per facile copia nella tabella
    print(f"\n{'=' * 90}")
    print("FORMATO LATEX PER LA TABELLA")
    print(f"{'=' * 90}\n")
    
    current_image = None
    for result in results:
        if current_image != result['image']:
            current_image = result['image']
            print(f"% {result['image']} ({result['resolution']})")
        
        print(f"& {result['F']} & {result['d']} & {result['time_ms']:.1f} \\\\")
    
    return results

def test_fixed_F_varying_d():
    """
    Test con F fissato (F=8) e d variabile (d=2, 4, 8)
    Misura i tempi di compressione per analizzare l'effetto del parametro d
    """
    print("\n" + "="*90)
    print("ANALISI PARAMETRICA: F FISSATO (F=8), d VARIABILE (d=2, 4, 8)")
    print("="*90)
    
    F = 8
    d_values = [2, 4, 8]
    image_path = "images/gradient.bmp"
    
    try:
        original_img = Image.open(image_path).convert('L')
        width, height = original_img.size
        resolution = f"{width}×{height}"
        
        print(f"\nImmagine: gradient.bmp ({resolution})")
        print(f"\n{'F':>3} | {'d':>3} | {'Tempo (ms)':>15}")
        print("-"*35)
        
        results = []
        for d in d_values:
            start_time = time.perf_counter()
            _, _ = compress_image(image_path, F, d)
            end_time = time.perf_counter()
            
            elapsed_ms = (end_time - start_time) * 1000
            print(f"{F:>3} | {d:>3} | {elapsed_ms:>15.2f}")
            results.append((F, d, elapsed_ms))
        
        return results
    except Exception as e:
        print(f"❌ Errore: {e}")
        return []

def test_fixed_d_varying_F():
    """
    Test con d fissato (d=3) e F variabile (F=4, 10, 16)
    Misura i tempi di compressione per analizzare l'effetto del parametro F
    """
    print("\n" + "="*90)
    print("ANALISI PARAMETRICA: d FISSATO (d=3), F VARIABILE (F=4, 10, 16)")
    print("="*90)
    
    d = 3
    F_values = [4, 10, 16]
    image_path = "images/gradient.bmp"
    
    try:
        original_img = Image.open(image_path).convert('L')
        width, height = original_img.size
        resolution = f"{width}×{height}"
        
        print(f"\nImmagine: gradient.bmp ({resolution})")
        print(f"\n{'F':>3} | {'d':>3} | {'Tempo (ms)':>15}")
        print("-"*35)
        
        results = []
        for F in F_values:
            # Verifica che d sia valido per questo F (0 <= d <= 2F-2)
            max_d = 2 * F - 2
            if d > max_d:
                print(f"{F:>3} | {d:>3} | {'N/A (d > 2F-2)':>15}")
                continue
                
            start_time = time.perf_counter()
            _, _ = compress_image(image_path, F, d)
            end_time = time.perf_counter()
            
            elapsed_ms = (end_time - start_time) * 1000
            print(f"{F:>3} | {d:>3} | {elapsed_ms:>15.2f}")
            results.append((F, d, elapsed_ms))
        
        return results
    except Exception as e:
        print(f"❌ Errore: {e}")
        return []

if __name__ == "__main__":
    results = run_compression_tests()
    print(f"\n{'=' * 90}")
    print(f"✓ Test completati: {len(results)} configurazioni elaborate")
    print(f"{'=' * 90}")
    
    # Esegui i test parametrici
    results_f_var = test_fixed_F_varying_d()
    results_d_var = test_fixed_d_varying_F()
    
    print("\n" + "="*90)
    print("RIEPILOGO ANALISI PARAMETRICA")
    print("="*90)
    
    if results_f_var:
        print("\nAnalisi 1 - F=8 variabile d:")
        for F, d, t in results_f_var:
            print(f"  F={F}, d={d}: {t:.2f} ms")
    
    if results_d_var:
        print("\nAnalisi 2 - d=3 variabile F:")
        for F, d, t in results_d_var:
            print(f"  F={F}, d={d}: {t:.2f} ms")
    
    print(f"\n{'=' * 90}")
