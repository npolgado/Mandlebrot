'''
NEWTON'S FRACTAL

Using roots.py, create a live animation which shows "newton's fractal"
REF 1 - https://youtu.be/-RdOwhmqP5s


TODO:
    - fix handing window when doing anything on comp (ERIC)
    - add roots to plot (ERIC)
    - add axis to plot (ERIC)
    - change scaling to be seperate for WIDTH and HEIGHT (diff window sizes) (BOTH)
    - improve drawing speed (BOTH)
    - improve calc time_efficiency (NICK)
    - improve root.py logic (adjusting, less memory) (NICK)
'''
import matplotlib.pyplot as plt
import numpy as np
import roots as r
import sys, time

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

def plot_complex(roots): #TODO: make this plot the axis for more details
    '''
    plot_complex: using the roots and coefficients of the polynomial, 
    plot the roots using matplotlib

    :param roots: array of polynomial roots
    :param coeff: array of polynomial coefficients in decending order (highest degree first!)

    :return: matplotlib plot of roots from polynomial with labels
    '''
    x = [np.real(ele) for ele in roots]  # extract real part
    y = [np.imag(ele) for ele in roots]  # extract imaginary part
    
    # plot the complex numbers
    fig = plt.figure()
    ax = fig.add_subplot()
    c = ax.scatter(x, y)
    plt.ylabel('Imaginary')
    plt.xlabel('Real')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) > 1: 
        # has args
        args = [int(x) for x in sys.argv[1:]]
        print("finding roots to polynomial {}...".format(args))
        
        try:
            f = r.POLY(args, lowerB=-500, upperB=500, n=20)
            print(f"\tloaded polynomial in {f.time_efficiency} seconds")
            print(f"\nFOUND ROOTS \n{f.roots}\n")
            # print(f"\tFOUND ROOTS \n{f.dict.values()}\n")
        except Exception as e:
            print(f"ERROR loading polynomial: \n\t{e}")

        # try:
        #     plot_complex(f.roots)
        # except Exception as e:
        #     print(f"ERROR printing roots: \n\t{e}")

        try:
            fr = r.FRACTAL(f)
        except Exception as e:
            print(f"couldn't find which root that is: \n\t{e}")

        try:
            fr.find_all_roots(fr.painter.get_resolution(), fr.painter.get_resolution())
            print("found all roots!!")
        except Exception as e:
            print(f"error with all roots: {e}\n\t")
    else:
        print(f"couldn't load initial polynomial arguments, try running main.py with parameters # # # # # (# = number, USE SPACES")
        pass
    time.sleep(30)