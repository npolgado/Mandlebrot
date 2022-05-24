'''
NEWTON'S FRACTAL

Using roots.py, create a live animation which shows "newton's fractal"

using https://youtu.be/-RdOwhmqP5s
'''
import matplotlib.pyplot as plt
import numpy as np
import roots as r
import sys, time

# default WIDTH / HEIGHT
WIDTH = 1080
HEIGHT = 720

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

def plot_complex(roots, coeff): #TODO: make this plot the axis for more details
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

def find_all_roots(fr, WIDTH, HEIGHT):
    for x in range(0, HEIGHT):
        for y in range(0, WIDTH):
            root = fr.which_root(x, y)
            fr.painter.draw_pixel(x, y, root)               # painter
            # print(f"x={x} y={y} has the root= {fr.which_root(x,y)}")

# default poly
# curr_poly = r.POLY([5, 4, 3, 2, 1, 10], n=50)
# fr = r.FRACTAL(curr_poly)

if __name__ == "__main__":
    if len(sys.argv) > 1: 
        # has args
        args = [int(x) for x in sys.argv[1:]]
        print("finding roots to polynomial {}...".format(args))
        
        try:
            f = r.POLY(args)
        except Exception as e:
            print(f"ERROR loading polynomial: \n\t{e}")

        try:
            plot_complex(f.roots, f.coefficients)
        except Exception as e:
            print(f"ERROR printing roots: \n\t{e}")

        try:
            fr = r.FRACTAL(f)
            print(f"found root: {fr.which_root(1,1)}")
        except Exception as e:
            print(f"couldn't find which root that is: \n\t{e}")

        # finding all points on the canvas

        try:
            find_all_roots(fr, fr.painter.get_pixels(), fr.painter.get_pixels())
            print("found all roots!!")
        except Exception as e:
            print(f"error with all roots: {e}\n\t")
    else:
        pass

    print("loading polynomial...\n")
    print("loading Gui...\n")

    time.sleep(3)