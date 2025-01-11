# eventNoiseFiltering
This repository is designed to filter event noise by utilizing the presence of neighboring events.

#### Input & Output

## Features
- denoise event data: Processes event-based camera data streams directly.

## Project Structure
```bash
.
├── noise_filter.cpp       # Handles event-based denoising in C++
├── plotAllData.py          # Plotting script for All data
├── plotEventCountFFT_Window.py      # Performs FFT analysis on event count variations using a Hamming window
├── plotTrajectory.py          # Plots trajectory data from tracked events
├── pngToPDF.py                 # Converts PNG images of plots into a single PDF
├── setup.py                 #  Script for building the C++ code for particle tracking
├── trackParticlesC.py                 # Prticle tracking code
└── README.md                 # Project documentation (this file)
```

## Modules Overview
### setup.py
Script for building the C++ code using pybind11. It compiles the particle_tracking.cpp file into a Python module (particle_tracking). This code is now only tested on M1 mac and Windows 11 environments.

```bash
python3 setup.py build_ext --inplace
```

### trackParticlesC.py
Reads and processes CSV files generated from .RAW files, performs particle tracking using a C++ module, and saves the results. It reads event data, optionally filters it by polarity (if needed), and applies parameters such as spatial and temporal thresholds for particle detection. The tracked particle data, including centroid histories and event points, is saved as a pickle file for further analysis.
You need to change parameters (sigma_x, sigma_t, gaussian_threshold, m_threshold) in the scripts.

#### Arguments
- -i Path to the input csv file or directory.

### plotTrajectory.py
Reads particle tracking data from a pickle file and plots the centroid trajectories of particles in 3D. The script also has an option to plot individual events associated with each particle, either fully or by sampling the data for visualization purposes.

#### Arguments
- -i Path to the input CSV file.

### plotEventCountFFT_Window.py
Performs FFT analysis on event count variations from particle tracking data. The script processes pickle files generated from tracking data and calculates the event counts over time. It then applies FFT to the event counts, identifies peaks in the frequency domain, and saves both the peak data and corresponding FFT plots. The results are output in both text and PNG formats for further analysis.

#### Arguments
- -i Path to the input pickle file or directory.

### peak_collection.py
Collects peak frequency data from multiple .txt files, optionally filters them based on specific identifiers (abura, kiku, momoziro, yubi), and generates violin plots to visualize the frequency distribution.

#### Arguments
- -i Input directory containing .txt files.
- -A Process all files regardless of their file names.

### pngToPDF.py
Converts multiple PNG images of plots into a single PDF. The resulting PDFs are saved in a pdf_results folder within the input directory.

#### Arguments
- -i Input directory containing .png files.
- -A Process all .png files regardless of filenames.
