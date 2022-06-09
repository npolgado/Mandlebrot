'''
NEWTON'S FRACTAL

Using roots.py, create a live animation which shows "newton's fractal"
REF 1 - INSPIRATION : https://youtu.be/-RdOwhmqP5s
REF 2 - HORNER'S METHOD: https://en.wikipedia.org/wiki/Horner%27s_method


TODO:
    - fix handing window when doing anything on comp (ERIC) (https://stackoverflow.com/questions/10354638/pygame-draw-single-pixel)
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

def window_mainloop(fr):
    isDone = False
    while True:

        fr.painter.handle_gui()

        if not isDone:
            try:
                fr.find_all_roots(fr.painter.get_resolution(), fr.painter.get_resolution())
                isDone = True
                # print("\r                   ", end='\r')
            except Exception as e:
                print(f"error finding all roots: \n\t{e}")

        cur_t = time.strftime("%b %d %Y %H:%M:%S", time.gmtime(time.time()))
        print(f"\r |{isDone}| |{cur_t}|", end='\r')

if __name__ == "__main__":
    if len(sys.argv) > 1: 
        # has args
        args = [float(x) for x in sys.argv[1:]]
        
        try:
            f = r.POLY(args, lowerB=-2, upperB=2, n=0)
            print(f"--- SUCESS ---\nloaded polynomial {f.get_name()}\tin {f.time_efficiency} seconds")
            print(f"root -->\n\t{f.roots}")
        except Exception as e:
            print(f"ERROR loading polynomial: \n\t{e}")

        # try:
        #     print(f"PLOTTING {f.get_name()}...")
        #     plot_complex(f.roots)
        # except Exception as e:
        #     print(f"ERROR printing roots: \n\t{e}")

        try:
            fr = r.FRACTAL(f, showWindow=True)
        except Exception as e:
            print(f"couldn't find which root that is: \n\t{e}")

        try:
            window_mainloop(fr)
        except Exception as e:
            print(f"ERROR running mainloop: \n\t{e}")

    else:
        print(f"couldn't load initial polynomial arguments, try running main.py with parameters # # # # # (# = number, USE SPACES")
        pass

    
    # time.sleep(30)