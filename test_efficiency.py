import time
import matplotlib.pyplot as plt
import numpy as np
import roots as r

def print_bar(progress, total):
    '''
    print_bar: uses total and progress to determine progress in percentage

    :param progress: current progress (less than total)
    :param total: total amount of iterations

    :return: None (plots graph)
    '''
    percent = 100 * (progress / float(total))
    bar = '*' * int(percent) + '-' * (100-int(percent))
    print(f"\r|{bar}| {percent:.2f}%", end='\r')

def plot_runtimes(x, y):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    plt.xlim(1, max_degrees+3)

    plt.ylabel('Time (seconds)')
    plt.xlabel('Maximum Degree')
    plt.title('Polynomial Length vs Time to Compute')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    max_degrees = 40
    max_samples = 5

    total = max_degrees * max_samples
    count = 0
    print_bar(count, total)

    means = []
    for curr_degree in range(2, max_degrees+2): # Go through every possible degree
        times = [] # array to hold each sample's time
        for curr_sample in range(0, max_samples): # Go through all samples 
            coeff = [int(np.random.uniform(-100, 100)) for y in range(0, curr_degree)]
            poly = r.POLY(coeff)
            count += 1
            print_bar(count, total)
            times.append(poly.time_efficiency)
        means.append(np.average(times))
    plot_runtimes(np.linspace(2, (max_degrees+2), (max_degrees)), means)
    print(means)