import numpy as np
import tsalign as tsa
import matplotlib.pyplot as plt
from time import perf_counter

if __name__ == '__main__':
    
    # Generate two time series
    t = np.linspace(0, 3, 1000)
    # generate sine wave as query
    Q = np.sin(2 * np.pi * 5 * t)[:500]
    # generate cosine wave as target
    S = np.cos(2 * np.pi * 5 * t)
    # add a little noise to the cosine wave
    S += 0.1 * np.random.randn(len(t))

    start = perf_counter()
    
    # Align the two time series
    align_timeseries, difference = tsa.align_timeseries(Q, S, distance='zdist')
    
    stop = perf_counter()
    print(f'Alignment took {stop - start} seconds.')

    # Plot the results

    fig, ax = plt.subplots(3, 1, figsize=(10, 10))
    ax[0].plot(Q, label='Query')
    ax[0].plot(S, label='Subject')
    ax[0].legend()
    ax[0].set_title('Original Time Series')
    ax[0].set_ylim(-1.5, 1.5)
    
    ax[1].plot(Q, label='Query')
    ax[1].plot(align_timeseries, label='Aligned Subject')
    ax[1].legend()
    ax[1].set_title('Aligned Time Series')
    ax[1].set_ylim(-1.5, 1.5)
    
    ax[2].plot(difference)
    ax[2].set_title('Difference')
    ax[2].set_ylim(-1.5, 1.5)
    plt.tight_layout()
    plt.savefig('examples/figures/alignment.png')
    plt.show()