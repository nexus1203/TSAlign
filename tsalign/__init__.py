import numpy as np
from scipy.signal import fftconvolve
        

def mnorm(x):
    """
    Perform mean normalization on a given time series.

    Parameters:
    x (numpy.ndarray): The input time series array.

    Returns:
    numpy.ndarray: The mean-normalized time series.
    """
    return x - np.mean(x)

def znorm(x, epsilon=1e-6):
    """
    Perform mean- and amplitude-adjustment (z-normalization) on a given time series.

    Parameters:
    x (numpy.ndarray): The input time series array.
    epsilon (float): A small value to prevent division by zero in case of zero standard deviation.

    Returns:
    numpy.ndarray: The z-normalized time series.
    """
    std = np.std(x, ddof=0)
    return (x - np.mean(x)) / max(std, epsilon)

def adjust_cumsum_length(cumsum_S, Q_length, conv_length):
    """
    Adjust the length of the cumulative sum array to match the length needed for convolution.

    Parameters:
    cumsum_S (numpy.ndarray): The cumulative sum array of the time series S.
    Q_length (int): The length of the query time series Q.
    conv_length (int): The expected length after convolution.

    Returns:
    numpy.ndarray: The adjusted cumulative sum array.
    """
    cumsum_adjusted = cumsum_S[Q_length - 1:]
    if cumsum_adjusted.shape[0] > conv_length:
        cumsum_adjusted = cumsum_adjusted[:conv_length]
    elif cumsum_adjusted.shape[0] < conv_length:
        padding = np.zeros(conv_length - cumsum_adjusted.shape[0])
        cumsum_adjusted = np.concatenate([cumsum_adjusted, padding])
    return cumsum_adjusted - cumsum_S[:conv_length]

def fft_sdist(Q, S):
    """
    Calculate the rolling Euclidean distance between two time series using Fast Fourier Transform.

    Parameters:
    Q (numpy.ndarray): The query time series.
    S (numpy.ndarray): The target time series.

    Returns:
    numpy.ndarray: The array of rolling Euclidean distances.
    """
    conv = fftconvolve(S, Q[::-1], mode='valid')
    cumsum_S = np.cumsum(np.square(S))
    adjusted_cumsum_S = adjust_cumsum_length(cumsum_S, len(Q), len(conv))
    return np.sum(np.square(Q)) - 2 * conv + adjusted_cumsum_S

def fft_mdist(Q, S):
    """
    Calculate the rolling mean-adjusted Euclidean distance between two time series using FFT.

    Parameters:
    Q (numpy.ndarray): The query time series.
    S (numpy.ndarray): The target time series.

    Returns:
    numpy.ndarray: The array of rolling mean-adjusted Euclidean distances.
    """
    Q = mnorm(Q)
    return fft_sdist(Q, S)

def fft_zdist(Q, S, epsilon=1e-6):
    """
    Calculate the rolling mean- and amplitude-adjusted (z-normalized) Euclidean distance using FFT.

    Parameters:
    Q (numpy.ndarray): The query time series.
    S (numpy.ndarray): The target time series.
    epsilon (float): A small value to prevent division by zero in standard deviation.

    Returns:
    numpy.ndarray: The array of rolling z-normalized Euclidean distances.
    """
    Q = znorm(Q, epsilon)
    return fft_sdist(Q, S)

def sdist(Q, S):
    """
    Interface for calculating rolling Euclidean Distance using FFT.

    Parameters:
    Q (numpy.ndarray): The query time series.
    S (numpy.ndarray): The target time series.

    Returns:
    numpy.ndarray: The array of rolling Euclidean distances.
    """
    return fft_sdist(Q, S)

def mdist(Q, S):
    """
    Interface for calculating rolling mean-adjusted Euclidean Distance using FFT.

    Parameters:
    Q (numpy.ndarray): The query time series.
    S (numpy.ndarray): The target time series.

    Returns:
    numpy.ndarray: The array of rolling mean-adjusted Euclidean distances.
    """
    return fft_mdist(Q, S)

def zdist(Q, S, epsilon=1e-6):
    """
    Interface for calculating rolling mean- and amplitude-adjusted Euclidean Distance using FFT.

    Parameters:
    Q (numpy.ndarray): The query time series.
    S (numpy.ndarray): The target time series.
    epsilon (float): A small value to prevent division by zero in standard deviation.

    Returns:
    numpy.ndarray: The array of rolling z-normalized Euclidean distances.
    """
    return fft_zdist(Q, S, epsilon)

def align_timeseries(query_series, subject_series, distance='zdist'):
    """
    Align two time series using the given distance function.

    Parameters:
    query_series (numpy.ndarray): The query time series.
    subject_series (numpy.ndarray): The subject time series that is to be aligned with the query time series.
    distance (str): The distance function to use. Options are 'sdist', 'mdist', and 'zdist'.

    Returns:
    numpy.ndarray: The aligned time series.
    numpy.ndarray: The difference between the query and target time series after alignment.
    """
    if distance == 'sdist':
        dist = sdist
    elif distance == 'mdist':
        dist = mdist
    elif distance == 'zdist':
        dist = zdist
    else:
        raise ValueError('Invalid distance function. Options are "sdist", "mdist", and "zdist".')
    dists = dist(query_series, subject_series)
    min_idx = int(np.argmin(dists))
    align_timeseries = subject_series[min_idx:min_idx + len(query_series)]
    difference = query_series - align_timeseries
    return align_timeseries, difference
