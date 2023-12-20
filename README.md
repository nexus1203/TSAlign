# TSAlign

TSAlign is a simple and fast Python package for aligning 1D time series data. It provides several functions to compute distances between time series and align them based on these distances. This package is particularly useful in signal processing, time series analysis, and similar domains where alignment of time series data is a common task.

## Features

- **Distance Calculation:** Compute various distances between time series, such as simple Euclidean, mean-adjusted, and z-normalized distances.
- **FFT-based Convolution:** Utilize Fast Fourier Transform for efficient computation of rolling distances.
- **Time Series Alignment:** Align a query time series with a subject time series based on the minimum distance.

## Installation

Clone the repository:

```bash
git clone https://github.com/nexus1203/TSAlign.git
cd TSAlign
```
or install locally using setup.py

```bash
python setup.py install
```

## Usage
The primary functionality of TSAlign is to align two time series based on a specified distance metric. The available distance metrics are:

- 'sdist': Simple Euclidean distance
- 'mdist': Mean-adjusted Euclidean distance
- 'zdist': Z-normalized (mean- and amplitude-adjusted) Euclidean distance

## Example
Here's a basic example of how to use TSAlign to align two time series:

```python
import numpy as np
import tsalign as tsa

# Generate two time series
t = np.linspace(0, 3, 1000)
Q = np.sin(2 * np.pi * 5 * t)[:500]  # Query: Sine wave
S = np.cos(2 * np.pi * 5 * t)  # Subject: Cosine wave with noise
S += 0.1 * np.random.randn(len(t))

# Align the time series using mean-adjusted distance
aligned_series, difference = tsa.align_timeseries(Q, S, distance='zdist')
```
## Visualization
To visualize the original, aligned, and difference of the time series:
```python
import matplotlib.pyplot as plt

# Plot the original and aligned time series along with their difference
plt.figure(figsize=(10, 10))

# Original Time Series
plt.subplot(3, 1, 1)
plt.plot(Q, label='Query')
plt.plot(S, label='Subject')
plt.legend()
plt.title('Original Time Series')
plt.ylim(-1.5, 1.5)

# Aligned Time Series
plt.subplot(3, 1, 2)
plt.plot(Q, label='Query')
plt.plot(aligned_series, label='Aligned Subject')
plt.legend()
plt.title('Aligned Time Series')
plt.ylim(-1.5, 1.5)

# Difference
plt.subplot(3, 1, 3)
plt.plot(difference)
plt.title('Difference')
plt.ylim(-1.5, 1.5)

plt.tight_layout()
plt.savefig('alignment.png')
plt.show()
```

## Visualization
![image](https://github.com/nexus1203/TSAlign/blob/main/examples/figures/alignment.png)

## Benchmarks
![image](https://github.com/nexus1203/TSAlign/blob/main/benchmarks/benchmark.png)

### Benchmark Stats
| Array Size | Mean Time (s) | Standard Deviation (s) |
|------------|---------------|------------------------|
| 1.0e+01    | 0.000265      | 0.000068               |
| 1.0e+02    | 0.000272      | 0.000072               |
| 1.0e+03    | 0.000330      | 0.000121               |
| 1.0e+04    | 0.000841      | 0.000303               |
| 1.0e+05    | 0.010003      | 0.001382               |
| 1.0e+06    | 0.108963      | 0.014162               |
| 1.0e+07    | 1.150634      | 0.203717               |


:memo: License
This project is licensed under the MIT License. See LICENSE for more details.
