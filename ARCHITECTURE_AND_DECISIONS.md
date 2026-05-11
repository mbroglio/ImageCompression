# Image Compression using DCT - Architecture & Decisions Log

## 1. Project Overview
Implement a Python-based open-source desktop application for image compression utilizing the Discrete Cosine Transform (DCT), translating logic from provided MATLAB scripts and meeting specified assignment constraints.

## 2. Technical Stack & Libraries
- **Language**: Python 3
- **GUI**: `customtkinter` (for a modern, scalable UI compared to standard tkinter)
- **Math/Matrices**: `numpy` for matrix operations, `scipy.fftpack` for fast DCT/IDCT in benchmark comparisons.
- **Image Processing**: `Pillow` (PIL) for reading, manipulating, and displaying `.bmp` images.
- **Plotting**: `matplotlib` for generating the semi-logarithmic performance comparison plot.

## 3. Implementation Steps & Status
- [x] **Step 0**: Initialize project, setup architecture documentation and environment.
- [x] **Step 1**: Implement custom 1D and 2D DCT (`custom_dct1`, `custom_dct2`) using standard loops/matrix multiplication.
- [x] **Step 2**: Verify custom DCT against the $8 \times 8$ test matrices ensuring scaling matches exactly.
- [x] **Step 3**: Benchmark custom `dct2` vs `scipy.fftpack` and plot exactly on a semi-log scale.
- [x] **Step 4**: Develop GUI for image selection, block size ($F$), and cutoff ($d$) inputs.
- [x] **Step 5**: Implement block-based image compression pipeline (Block split -> Fast DCT2 -> Zero-out high frequencies -> Fast IDCT2 -> Reconstruct block/image).
- [x] **Step 6**: Display original vs compressed images side-by-side.

## 4. Architectural Decisions & Math Assumptions
- **Custom DCT Implementation**: The 1D custom DCT will be implemented using the mathematical definition, and the 2D DCT will be built by applying the 1D transform to rows and then columns to guarantee $O(N^3)$ complexity.
- **DCT Scaling**: Standard orthogonal scaling will be used to ensure unitary properties. We will rigorously test to match the expected outputs from the assignment PDF.
- **GUI Framework**: Opted for `customtkinter` for a better user experience over standard `tkinter`.
- **Image Boundaries**: Edge remainders will be discarded as per requirements when splitting into $F \times F$ blocks.
- **Value Clamping**: Final pixel values will be rounded to nearest integer and explicitly clipped to $[0, 255]$ range before casting to `uint8`.