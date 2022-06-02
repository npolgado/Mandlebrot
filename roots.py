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
    '''
    root_finder_helper: find the nearest root in the case that a root in never found

    :param next_guess: the last iteration guess that couldn't find a root
    :param poly: root.py POLY structure 
    :return: the root that is closest to the next_guess param
    '''
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
        self.dict = poly.dict
        self.painter = p.Painter(poly.dict) #extra param not implemented

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
                position = x + y*1j
                position_rounded = self.poly.round_complex(position, 8)

                if position_rounded in self.dict.keys(): # root known... 
                    self.painter.draw_resolution(x, y, position_rounded)
                else:
                    root = self.poly.round_complex(self.which_root(position), 8)
                    self.painter.draw_resolution(x, y, root)

    def which_root(self, guess, maxIter=1000):
        '''
        which_root: uses lookup table from polynomial to find all the values on the canvas

        :param x: real component, or x coordinate
        :param y: imaginary component, or y coordinate
        :return: the root which this initial guess calculates
        '''
        original_guess = guess

        for iteration in range(maxIter):
            next_guess = guess - (self.poly.eval(guess) / self.poly.eval_derivative(guess))
            if abs(next_guess - guess) < DELTA:  
                # found a new root!
                return next_guess

            # not a root this iteration
            guess = next_guess    

        return root_finder_helper(next_guess, self.poly)

class POLY():
    def __init__(self, coefficients, lowerB=-10, upperB=10, n=20):
        assert(len(coefficients) >= 1)

        self.dict = {}
        self.lowerB = lowerB
        self.upperB = upperB
        self.n = n
        self.coefficients = coefficients
        self.derivative = np.polyder(self.coefficients, 1)

        start_t = time.time()         
        self.roots = self.calc_roots(lowerB, upperB, n)
        end_t = time.time() 

        self.time_efficiency = float(end_t - start_t)

    def round_complex(self, complex, decimal):
        return round(np.real(complex), decimal) + round(np.imag(complex), decimal)*1j

    def calc_roots(self, lowerB, upperB, N, maxIter=1000):
        '''
        calc_roots: return the roots of the polynomial object
        :param lowerB: lower bound for generating inital guesses
        :param upperB: upper bound for generating inital guesses
        :param N: sample size, N=sqrt(num_guesses)
        :return: array of complex root values
        '''
        sampleR = [np.random.uniform(lowerB, upperB) for x in range(N)]
        sampleI = [np.random.uniform(lowerB, upperB) for x in range(N)]

        roots_found = 0     # keeps track of how many times the efficiency was triggered
        for r in sampleR:
            for i in sampleI:
                guess = r + i*1j
                guesses_path = []
                
                if self.round_complex(guess, 8) in self.dict.keys():
                    # already found root
                    roots_found += 1
                    print(f"already found root (num: {roots_found})")
                    continue
                
                else
                    # root not found
                    # do next_guess
                    original_guess = guess
                    for iteration in range(maxIter):
                        next_guess = guess - (self.eval(guess) / self.eval_derivative(guess))
                        if abs(next_guess - guess) < DELTA:  
                            # found a new root!
                            self.dict[self.round_complex(original_guess, 8)] = self.round_complex(next_guess, 8)

                            # add all path elements to the dictionary 
                            for ele in guesses_path:
                                self.dict[self.round_complex(ele, 8)] = self.round_complex(next_guess, 8)
                            break

                        # not a root this iteration
                        guesses_path.append(next_guess)
                        guess = next_guess    

        return list(set(self.dict.values()))            

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
