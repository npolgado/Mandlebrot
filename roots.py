'''FINIDNG ROOTS
'''
import matplotlib.pyplot as plt
import numpy as np
import sys

SIZE = 1024         # size of canvas
DELTA = 1e-10       # when to stop calculating root
N = 1000            # max iterations (avoiding endless loops)

def poly_name(coeff):
    '''
    poly_name: from the coefficients of the polynomial, 
    return a string that is human readable of the polynomial
    
    :param coeff: array of polynomial coefficients in decending order (highest degree first!)

    :return: string of written out polynomial
    '''
    ans = ''
    count = len(coeff)-1
    for i in coeff:
        if count == 0:
            ans += str(i)
            ans += '\n'
        else:
            ans += '{}x**'.format(i) + str(count)
            ans += ' + '    
        count -= 1
    return ans

def plot_complex(roots, coeff):
    '''
    plot_complex: using the roots and coefficients of the polynomial, 
    plot the roots using matplotlib

    :param roots: array of polynomial roots
    :param coeff: array of polynomial coefficients in decending order (highest degree first!)

    :return: matplotlib plot of roots from polynomial with labels
    '''
    # extract real part
    x = [ele.real for ele in roots]
    # extract imaginary part
    y = [ele.imag for ele in roots]
    
    # plot the complex numbers
    fig = plt.figure()
    ax = fig.add_subplot()
    c = ax.scatter(x, y)
    plt.ylabel('Imaginary')
    plt.xlabel('Real')
    plt.title("Complex Roots of Polynomial\n{}".format(poly_name(coeff)))
    plt.grid(True)
    plt.show()

def calc_poly(coeff, x):
    '''
    calc_result to find the value of the polynomial with value x

    :param coeff: array of polynomial coefficients in decending order (highest degree first!)
    :param x: value to evaluate polynomial

    :return: polynomial evaluated with x
    '''
    ans = 0
    count = 0
    for i in reversed(coeff):
        ans += i*np.power(x, count)
        count += 1
    return ans

def approx_root(coeff, deriv, lowerB=-10, upperB=10, sampleSize=25):
    '''
    approx_root: given the polynomial and bounds, approximate the complex
    roots using sampling and newton's method

    :param coeff: array of polynomial coefficients in decending order (highest degree first!)
    :param deriv: array of polynomial derivative coefficients
    :param lowerB: given lower bound of initial guess 
    :param upperB: given upper bound of initial guess 
    :param sampleSize: number of samples to be approximated (sampleSize * sampleSize is the total space)

    :return: polynomial roots evaluated using Newton's method
    '''
    sampleR = [np.random.uniform(lowerB, upperB) for x in range(sampleSize)]
    sampleI = [np.random.uniform(lowerB, upperB) for x in range(sampleSize)]

    roots = []

    for r in sampleR:
        for i in sampleI:
            guess = r + i*1j
            for n in range(N):
                next_guess = guess - (calc_poly(coeff, guess) / calc_poly(deriv, guess))
                if abs(next_guess - guess) < DELTA:
                    is_in = False
                    for root in roots:
                        if abs(next_guess - root) < DELTA:
                            is_in = True
                            break
                    if not is_in:
                        roots.append(next_guess)
                    break
                guess = next_guess
    return roots

if __name__ == "__main__":
    try:
        arguments = sys.argv[1:]
    except:
        arguments = []

    print(arguments)

    try:
        arg_list = arguments[0].split(',')
        coeff = [int(x) for x in arg_list] 
        deriv = np.polyder(coeff, 1)
    except:
        try:
            coeff = np.array(input("enter the values of the polynomial (seperated by spaces):\n").split(" "), dtype=np.int32)
            deriv = np.polyder(coeff, 1)
        except:
            print("couldn't load coefficients..\n")
            coeff = [np.round(np.random.rand()*100) for x in range(np.round(np.random.rand()*10))]
            deriv = np.polyder(coeff, 1)
    
    print("found coefficients {}, with a derivative of {}".format(coeff, deriv))

    try:
        lb = int(arguments[1])
        ub = int(arguments[2])
    except:
        print('no arguments for boundaries...\n')
     
    try:
        ss = int(arguments[3])
    except:
        print('no arguments for sample size...\n')

    try:
        root = approx_root(coeff, deriv, lb, ub, ss)
    except:
        root = approx_root(coeff, deriv)

    print("average root found at: {}\n\n".format(str(root)))
    plot_complex(root, coeff)