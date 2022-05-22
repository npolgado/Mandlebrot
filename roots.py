'''FINIDNG ROOTS
'''
import matplotlib.pyplot as plt
import numpy as np
import sys
import painter as p

SIZE = 1024         # size of canvas
DELTA = 1e-10       # when to stop calculating root

'''
QUICK NOTES:

To increased compute speed, consider DP dictionary lookup

- how do we handle changing the roots,
  recalculating poly, and changing the oo func
'''

def plot_complex(roots, coeff):
    '''
    plot_complex: using the roots and coefficients of the polynomial, 
    plot the roots using matplotlib

    :param roots: array of polynomial roots
    :param coeff: array of polynomial coefficients in decending order (highest degree first!)

    :return: matplotlib plot of roots from polynomial with labels
    '''
    # extract real part
    x = [np.real(ele) for ele in roots]
    # extract imaginary part
    y = [np.imag(ele) for ele in roots]
    
    # plot the complex numbers
    fig = plt.figure()
    ax = fig.add_subplot()
    c = ax.scatter(x, y)
    plt.ylabel('Imaginary')
    plt.xlabel('Real')
    plt.grid(True)
    plt.show()

class POLY():
    def __init__(self, coefficients, lowerB=-10, upperB=10, n=30):
        assert(len(coefficients) >= 1)

        self.calculated = { #DP to make compute faster
            'guess' : [],
            'root': []
        }

        # self.painter = p.Painter()

        self.lowerB = lowerB
        self.upperB = upperB
        self.n = n
        self.coefficients = coefficients
        self.derivative = np.polyder(self.coefficients, 1)
        self.roots = self.calc_roots(lowerB, upperB, n)

    def adjust(self, new_coeff):
        assert(len(new_coeff) >= 1)
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
                for i, known in enumerate(self.calculated.get('guess')):                        # check if guess if in dict
                    if abs(guess - known) < DELTA:                                              # known root already calculated
                        alreadyFound = True

                        if len(roots) < 1:
                            roots.append(next_guess)  
                        else:
                            isIn = False
                            for m, root in enumerate(roots):                                        # add to known if not already found
                                if abs(guess - root) < DELTA:
                                    isIn = True
                            
                            if isIn == False:
                                roots.append(next_guess)                                            # add to return if new root
                                # self.painter.draw_pixel(np.real(original_guess), np.imag(original_guess))    # painter  
                            break
                
                # DO CALC IF NOT FOUND
                if alreadyFound == False:
                    original_guess = guess                                                      # record original for lookup

                    for n in range(maxIter):
                        next_guess = guess - (self.eval(guess) / self.eval_derivative(guess))

                        if abs(next_guess - guess) < DELTA:                                     # found new ans
                            self.calculated['guess'].append(original_guess)                     # regardless, add found root and guess to dict
                            self.calculated['root'].append(next_guess) 

                            if len(roots) < 1:
                                roots.append(next_guess)
                            else:
                                isIn = False
                                for m, root in enumerate(roots):                                # add to known if not already found
                                    if abs(next_guess - root) < DELTA:
                                        isIn = True
                                
                                if isIn == False:
                                    roots.append(next_guess)                                    # add to return if new root
                                    # self.painter.draw_pixel(np.real(original_guess), np.imag(original_guess))   # painter  
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
        f = POLY(args)
        # parent = super(f.__class__, f)
        # print(f"{parent.calculated}")
    else:
        pass