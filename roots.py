'''FINIDNG ROOTS
'''
import numpy as np
import painter as p
import time

SIZE = 1024         # size of canvas
DELTA = 1e-10       # when to stop calculating root

'''
QUICK NOTES:

- how do we handle changing the roots,
  recalculating poly, and changing the oo func
'''

def root_finder_helper(next_guess, poly):
    closest = abs(next_guess - poly.roots[0])
    index = 0
    for i, root in enumerate(poly.roots[1:]):
        new_closest = abs(next_guess - root)
        if  new_closest < closest:
            closest = new_closest
            index = i
    return poly.roots[index]

class FRACTAL(): #use this as the dictionary, input must be a poly
    def __init__(self, poly):
        self.poly = poly        
        self.dict = self.poly.calculated
        self.painter = p.Painter() #extra param not implemented

    def find_all_roots(self, WIDTH, HEIGHT):
        '''
        find_all_roots: uses the FRACTAL object and a width and height to find the root at every point

        :param fr: FRACTAL OBJECT
        :param WIDTH: num points in x axis dimension
        :param HEIGHT: num points in y axis dimension
        :return: nothing, call which_root and draw for every point
        '''
        for x in range(HEIGHT):
            for y in range(WIDTH):
                root = self.which_root(x, y)              # FIND ROOT @ POINT
                self.painter.draw_resolution(x, y, root)  # CALL TO DRAW POINT
                # print(f"x={x} y={y} has the root= {fr.which_root(x,y)}")

    def which_root(self, x, y, maxIter=1000):
        '''
        which_root: uses lookup table from polynomial to find all the values on the canvas

        :param x: real component, or x coordinate
        :param y: imaginary component, or y coordinate
        :return: the root which this initial guess calculates
        '''
        guess = x + y*1j
        # print(f"which_root --> ({x}, {y})")

        for i, known_guess in enumerate(self.dict['guess']):    # check table
            if abs(guess - known_guess) < DELTA:
                # print(f"DICTIONARY ROOT@{self.dict['root'][i]}")
                return self.dict['root'][i]                     # if calculated already: return root
        
        for n in range(maxIter):                                   # if not in table: do calc
            next_guess = guess - (self.poly.eval(guess) / self.poly.eval_derivative(guess))
            if abs(next_guess - guess) < DELTA:                 # found new ans
                # print(f"CALCULATION ROOT@{next_guess}")
                return next_guess
            guess = next_guess
        
        return root_finder_helper(next_guess, self.poly)

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

    def adjust(self, new_coeff, lowerB=-10, upperB=10, n=20):
        '''
        adjust: given a new polynomial coefficient input, reset data inside this object to new appropriate roots

        :param new_coeff: array of coefficients from highest degree decending
        :param lowerb: (optional) lower bound for calculation samples
        :param upperb: (optional) upper bound for calculation samples
        :param n: number of iterations per sample point
        :return: nothing: changes values
        '''
        assert(len(new_coeff) >= 1)

        self.calculated = { #RESET DP, no need for previous data
            'guess' : [],
            'root': []
        }

        self.coefficients = new_coeff
        self.lowerB = lowerB
        self.upperB = upperB
        self.n = n
        self.derivative = np.polyder(self.coefficients, 1)
        self.roots = self.calc_roots(lowerB, upperB, n)

    def calc_roots(self, lowerB, upperB, N, doPrint=False):
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
                            for root in roots:                                                        # add to known if not already found
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

# CLI HANDLING
if __name__ == "__main__":
    print("compiled! use as a library!")
