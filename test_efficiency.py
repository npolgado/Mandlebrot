import time, sys
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

if __name__ == "__main__":
    max_degrees = 20
    max_samples = 10

    total = max_degrees * max_samples
    count = 0
    # print_bar(count, total)

    means = []
    for x in range(0, max_degrees):
        times = []

        for i in range(0, x):
            for j in range(0, max_samples):
                coeff = [int(np.random.uniform(-100, 100)) for x in range(0, max_degrees)]
                start_t = time.time()
                poly = r.POLY(coeff)
                end_t = time.time()
                times.append(float(end_t - start_t))
        
        means.append(float(sum(times) / len(times)))

print(means)