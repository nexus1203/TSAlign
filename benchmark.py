import numpy as np
from time import perf_counter
from matplotlib import pyplot as plt
import seaborn as sns
import tsalign as tsa


if __name__ == '__main__':
    
    # Number of times to repeat each test
    repetitions = 25
    max_pow = 7
    # Storing time taken for each test
    time_taken = {i: [] for i in range(8)}

    # Generating and aligning time series
    for i in range(max_pow):
        for _ in range(repetitions):
            t = np.linspace(0, 3, 10**(i+1))
            sine = np.sin(2 * np.pi * 5 * t)
            cosine = np.cos(2 * np.pi * 5 * t) + np.random.normal(0, 0.1, len(sine))
            query = sine[:len(sine)//2]
            subject = cosine

            # time the alignment
            start = perf_counter()
            aligned, difference = tsa.align_timeseries(query, subject)
            end = perf_counter()
            
            print(f'Alignment of {10**(i+1)} elements took {end - start} seconds.')
            time_taken[i].append(end - start)

    # Initialize arrays for x-values, mean times, and standard deviations
    x_values = []
    mean_times = []
    std_times = []

    for i in range(max_pow):
        times = np.array(time_taken[i])
        if times.size > 0 and not np.isnan(times).any():
            x_values.append(10**(i+1))
            mean_times.append(np.mean(times))
            std_times.append(np.std(times))
        else:
            print(f"Skipping data for 10^{i+1} Elements due to empty or invalid data.")

    # Convert lists to arrays for plotting
    x_values = np.array(x_values)
    mean_times = np.array(mean_times)
    std_times = np.array(std_times)

    # Plotting
    plt.figure(figsize=(10, 6))

    # Plotting the mean line
    plt.plot(x_values, mean_times, 'o-', label='Mean Time', color='black')

    # Shaded area representing the standard deviation
    plt.fill_between(x_values, mean_times - (2.5*std_times), mean_times + (2.5*std_times), alpha=0.3, 
                     label='Standard Deviation', color='grey')

    plt.xscale('log')  # Setting the x-axis to a logarithmic scale
    plt.xlabel('Array size (log scale)')
    plt.ylabel('Time taken (s)')
    plt.title('Mean Time and Distribution Taken to Align Time Series of Different Sizes')
    plt.legend()
    plt.savefig('benchmarks/benchmark.png')
    # plt.show()
    
    # Writing to a text file
    with open('benchmarks/benchmark_data.csv', 'w') as f:
        f.write('Array Size,Mean Time (s),Standard Deviation (s)\n')
        for i in range(len(x_values)):
            f.write(f'{x_values[i]:.1e},{mean_times[i]:.6f},{std_times[i]:.6f}\n')