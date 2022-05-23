'''FINIDNG ROOTS
'''
import matplotlib.pyplot as plt
import numpy as np
import painter as p
import time, sys

SIZE = 1024         # size of canvas
DELTA = 1e-10       # when to stop calculating root

'''
QUICK NOTES:

- how do we handle changing the roots,
  recalculating poly, and changing the oo func
'''

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
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            root = fr.which_root(x,y)
            fr.painter.draw_pixel(x, y)               # painter
            # print(f"x={x} y={y} has the root= {fr.which_root(x,y)}")

class FRACTAL(): #use this as the dictionary, input must be a poly
    def __init__(self, poly):
        self.poly = poly        
        self.dict = self.poly.calculated
        self.painter = p.Painter()

    def which_root(self, x, y):
        '''
        which_root: uses lookup table from polynomial to find all the values on the canvas

        :param x: real component, or x coordinate
        :param y: imaginary component, or y coordinate
        :return: the root which this initial guess calculates
        '''
        guess = x + y*1j

        for i, known_guess in enumerate(self.dict['guess']):    # check table

            if abs(guess - known_guess) < DELTA:
                return self.dict['root'][i]                     # if calculated already: return root
        
        for n in range(1000):                                   # if not in table: do calc
            next_guess = guess - (self.poly.eval(guess) / self.poly.eval_derivative(guess))
            if abs(next_guess - guess) < DELTA:                 # found new ans
                return next_guess
            guess = next_guess

class POLY():
    def __init__(self, coefficients, lowerB=-10, upperB=10, n=20):
        assert(len(coefficients) >= 1)

        self.calculated = { #DP to make compute faster
            'guess' : [],
            'root': []
        }

        self.lowerB = lowerB
        self.upperB = upperB
        self.n = n
        self.coefficients = coefficients
        self.derivative = np.polyder(self.coefficients, 1)
        start_t = time.time()         
        self.roots = self.calc_roots(lowerB, upperB, n)
        end_t = time.time() 
        self.time_efficiency = float(end_t - start_t)

    def adjust(self, new_coeff):
        assert(len(new_coeff) >= 1)

        self.calculated = { #RESET DP, no need for previous data
            'guess' : [],
            'root': []
        }

        self.coefficients = new_coeff
        self.derivative = np.polyder(self.coefficients, 1)
        self.roots = self.calc_roots(self.lowerB, self.upperB, self.n)

    def calc_roots(self, lowerB, upperB, N):
        '''
        calc_roots: return the roots of the polynomial object
        :param lowerB: lower bound for generating inital guesses
        :param upperB: upper bound for generating inital guesses
        :param N: sample size, N=sqrt(num_guesses)
        :return: array of complex root values
        '''
        maxIter = 1000
        sampleR = [np.random.uniform(lowerB, upperB) for x in range(N)]
        sampleI = [np.random.uniform(lowerB, upperB) for x in range(N)]

        roots = []

        for r in sampleR:
            for i in sampleI:
                guess = r + i*1j
                alreadyFound = False

                # PRE CHECK FOR ANSWER
                for known in self.calculated.get('guess'):                                                          # check if guess if in dict
                    if abs(guess - known) < DELTA:                                                                  # known root already calculated
                        alreadyFound = True

                        if len(roots) < 1:
                            roots.append(next_guess)
                        else:
                            isIn = False
                            for m, root in enumerate(roots):                                                        # add to known if not already found
                                if abs(guess - root) < DELTA:
                                    isIn = True
                            
                            if isIn == False:
                                roots.append(next_guess)                                                            # add to return if new root
                            break
                
                # DO CALC IF NOT FOUND
                if alreadyFound == False:
                    original_guess = guess                                                                          # record original for lookup

                    for n in range(maxIter):
                        next_guess = guess - (self.eval(guess) / self.eval_derivative(guess))

                        if abs(next_guess - guess) < DELTA:                                                         # found new ans
                            self.calculated['guess'].append(original_guess)                                         # regardless, add found root and guess to dict
                            self.calculated['root'].append(next_guess) 

                            if len(roots) < 1:
                                roots.append(next_guess) 
                            else:
                                isIn = False
                                for m, root in enumerate(roots):                                                    # add to known if not already found
                                    if abs(next_guess - root) < DELTA:
                                        isIn = True
                                
                                if isIn == False:
                                    roots.append(next_guess)                                                        # add to return if new root
                                break
                        guess = next_guess
        return roots

    def eval(self, x):
        '''
        eval: to find the value of the polynomial with value x
        :param x: value to evaluate polynomial
        :return: polynomial evaluated with x
        '''
        ans = 0
        count = 0
        for i in reversed(self.coefficients):
            ans += i*np.power(x, count)
            count += 1
        return ans

    def eval_derivative(self, x):
        '''
        eval_derivative: to find the value of the derivative with value x
        :param x: value to evaluate polynomial
        :return: derivative evaluated with x
        '''
        ans = 0
        count = 0
        for i in reversed(self.derivative):
            ans += i*np.power(x, count)
            count += 1
        return ans    

    def get_name(self):
        '''
        get_name: find the string formatted human readable polynomial of the object
        :return: string with human readable polynomial
        '''
        ans = ''
        count = len(self.coefficients)-1
        for i in self.coefficients:
            if bool(i):
                if count == 0:
                    ans += str(i)
                    ans += '\n'
                else:
                    ans += '{}x**'.format(i) + str(count)
                    ans += ' + '    
                count -= 1
            else:
                count -= 1
        return ans

#CLI HANDLING
if __name__ == "__main__":
    if len(sys.argv) > 1: 
        #has args
        args = [int(x) for x in sys.argv[1:]]
        print("finding roots to polynomial {}...".format(args))
        
        try:
            f = POLY(args)
        except:
            print("ERROR loading polynomial...")

        try:
            print(f"{f.get_name()}\t")
        except:
            print("ERROR printing polynomial name...")

        try:
            print(f"{np.reshape(f.roots, (len(f.roots), 1))}")
        except:
            print("ERROR printing roots...")

        # try:
        #     plot_complex(f.roots, f.coefficients)
        # except:
        #     print("ERROR printing roots...")

        try:
            fr = FRACTAL(f)
            print(f"found root: {fr.which_root(1,1)}")
        except:
            print("couldn't find which root that is...")

        try:
            find_all_roots(fr, 1000, 1000)
            print("found all roots!!")
        except:
            print("error with all roots")
    else:
        pass