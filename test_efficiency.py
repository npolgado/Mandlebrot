import time
import matplotlib.pyplot as plt
import numpy as np
import roots as r

def print_bar(progress, total, deg, sample):
    '''
    print_bar: uses total and progress to determine progress in percentage

    :param progress: current progress (less than total)
    :param total: total amount of iterations

    :return: None (plots graph)
    '''
    percent = 100 * (progress / float(total))
    bar = '*' * int(percent) + '-' * (100-int(percent))
    print(f"\r|  {deg} <--- {sample}  | {bar} | {percent:.2f}%", end='\r')

def plot_runtimes(times, iters, maxed):
    x = np.linspace(2, (max_degrees+2), (max_degrees))


    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

    ax1.plot(x, times)
    ax1.grid(True, which='both')
    ax1.axhline(y=0, color='k')
    ax1.axvline(x=0, color='k')
    ax1.set_title("Max_Degree vs. Time")

    ax2.plot(x, iters)
    ax2.grid(True, which='both')
    ax2.axhline(y=0, color='k')
    ax2.axvline(x=0, color='k')
    ax2.set_title("Max_Degree vs. Num_Iterations")

    ax3.plot(x, maxed)
    ax3.grid(True, which='both')
    ax3.axhline(y=0, color='k')
    ax3.axvline(x=0, color='k')
    ax3.set_title("Max_Degree vs. Times_Maxed_Out")

    # plt.title("roots.py efficiency")
    plt.show()

if __name__ == "__main__":
    try:
        max_degrees = int(input("up to how many degrees?"))
    except:
        max_degrees = 20
    try:
        max_samples = int(input("up to how many samples?"))
    except:
        max_samples = 32

    total = max_degrees * max_samples
    count = 0
    print_bar(count, total, 0, 0)

    means = []
    avg_iterations = []
    times_maxed = []

    for curr_degree in range(2, max_degrees+2): # Go through every possible degree

        times = [] # array to hold each sample's time
        iters = []
        maxed = []

        for curr_sample in range(0, max_samples): # Go through all samples
            coeff = [int(np.random.uniform(-100, 100)) for y in range(0, curr_degree)]
            poly = r.POLY(coeff)
            count += 1
            print_bar(count, total, curr_degree, curr_sample)
            times.append(poly.time_efficiency)
            iters.append(poly.average_iterations)
            maxed.append(poly.didnt_converge)

        means.append(np.average(times))
        avg_iterations.append(np.average(iters))
        times_maxed.append(np.average(maxed))

    plot_runtimes(means, avg_iterations, times_maxed)
    print(means)