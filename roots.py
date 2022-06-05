'''FINIDNG ROOTS
'''
import numpy as np
import painter as p
import time

SIZE = 1024         # size of canvas
DELTA = 1e-4       # when to stop calculating root

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
    def __init__(self, poly, showWindow=True):
        self.showWindow = showWindow
        self.poly = poly        
        self.dict = poly.dict
        self.painter = p.Painter(self.dict, showWindow=self.showWindow) #extra param not implemented

    def find_all_roots(self, WIDTH, HEIGHT):
        '''
        find_all_roots: uses the FRACTAL object and a width and height to find the root at every point

        :param fr: FRACTAL OBJECT
        :param WIDTH: num points in x axis dimension
        :param HEIGHT: num points in y axis dimension
        :return: nothing, call which_root and draw for every point
        '''
        tot = WIDTH * HEIGHT
        Wscale  = 4 / WIDTH # for 1000, this is 0.002 or the factor to adjust root calculations by
        Hscale  = 4 / HEIGHT # for 1000, this is 0.002 or the factor to adjust root calculations by
        count = 0
        w_off = WIDTH / 2
        h_off = HEIGHT / 2

        for x in list(np.linspace(-WIDTH/2, WIDTH/2, WIDTH+1)):
            for y in list(np.linspace(-HEIGHT/2, HEIGHT/2, HEIGHT+1)):
                r = x * Wscale
                i = y * Hscale
                position = r + i*1j
                position_rounded = self.poly.round_complex(position, 3)

                root = self.poly.round_complex(self.which_root(position), 3)
                    
                if self.showWindow:
                    self.painter.draw_resolution(x+w_off, y+h_off, root)
                
                count+=1
                progress = round(float((count/tot)*100), 3)
                
                print(f"\r{progress}%|{position_rounded}|{root}", end='\r')

    def which_root(self, guess, maxIter=1000):
        '''
        which_root: uses lookup table from polynomial to find all the values on the canvas

        :param x: real component, or x coordinate
        :param y: imaginary component, or y coordinate
        :return: the root which this initial guess calculates
        '''
        o_g_r = self.poly.round_complex(guess, 3)

        if o_g_r in self.dict: # found in dict already
            return self.dict[o_g_r]

        for iteration in range(maxIter):
            next_guess = guess - (self.poly.eval(guess) / self.poly.eval_derivative(guess))
            n_g_r = self.poly.round_complex(next_guess, 3)

            if n_g_r in self.dict: # found in dict already
                return self.dict[n_g_r]

            if abs(next_guess - guess) < DELTA:
                self.dict[o_g_r] = n_g_r # add new find to dict
                return next_guess

            # not a root this iteration
            guess = next_guess    

        return root_finder_helper(next_guess, self.poly)

class POLY():
    def __init__(self, coefficients, lowerB=-10, upperB=10, n=20):
        assert(len(coefficients) >= 1)

        self.dict = {}
        self.coefficients = coefficients
        self.derivative = list(np.polyder(self.coefficients, 1))

        start_t = time.time()         
        self.roots = self.calc_roots(lowerB, upperB, n)
        end_t = time.time() 

        self.time_efficiency = float(end_t - start_t)

    def round_complex(self, complex, decimal):
        re = float(complex.real)
        re_r = round(re, decimal)

        im = float(complex.imag)
        im_r = round(im, decimal)

        ans = re_r + im_r*1j
        # print(f"{re} + {im}*1j = {ans}")
        return ans

    def calc_roots(self, lowerB, upperB, N, maxIter=1000):
        '''
        calc_roots: return the roots of the polynomial object
        :param lowerB: lower bound for generating inital guesses
        :param upperB: upper bound for generating inital guesses
        :param N: sample size, N=sqrt(num_guesses)
        :return: array of complex root values
        '''
        sampleR = [np.random.uniform(-2, 2) for x in range(N)]
        sampleI = [np.random.uniform(-2, 2) for x in range(N)]

        roots_saved = 0     # keeps track of how many times the efficiency was triggered
        num_iterations = []
        num_maxed_out = 0

        for r in sampleR:
            for i in sampleI:
                guess = r + i*1j
                guess_rounded = self.round_complex(guess, 3)
                guesses_path = []

                if guess_rounded in self.dict:
                    # already found root
                    roots_saved += 1
                    # print(f"already found root (num: {roots_saved})")
                    continue
                else:
                    # root not found
                    # do next_guess
                    original_guess = guess
                    original_guess_r = self.round_complex(original_guess, 3)

                    guesses_path.append(original_guess_r)

                    isFound = False
                    for iteration in range(maxIter):
                        if iteration > (2*int(len(self.coefficients)-1)):
                            break
                        f_x = self.eval(guess)
                        f_p_x = self.eval_derivative(guess)
                        next_guess = guess - (f_x / f_p_x)
                        # print(f"{guess} - ({f_x} / {f_p_x}) = {next_guess}")
                        next_guess_r = self.round_complex(next_guess, 3)

                        if next_guess_r in self.dict:
                            roots_saved += 1
                            num_iterations.append(iteration)
                            isFound = True
                            # print(f"already found root (num: {roots_saved})")
                            break

                        guesses_path.append(next_guess_r)

                        if abs(next_guess - guess) < DELTA:  
                            # found a new root!
                            self.dict[original_guess_r] = next_guess_r
                            num_iterations.append(iteration)
                            isFound = True

                            # add all path elements to the dictionary 
                            for ele in guesses_path:
                                self.dict[ele] = next_guess_r
                            break

                        # not a root this iteration
                        guess = next_guess 
                    if not isFound:
                        num_maxed_out += 1
                    num_iterations.append(iteration)
        avg_iter = np.average(num_iterations)
        self.average_iterations = avg_iter
        self.didnt_converge = num_maxed_out 

        # print(f"optimized {roots_saved} roots")
        return list(set(self.dict.values()))            

    def eval(self, x):
        '''
        eval: to find the value of the polynomial with value x
        :param x: value to evaluate polynomial
        :return: polynomial evaluated with x
        '''
        p=0
        for i in self.coefficients:
            p = p*x+i
        return p
        # ans = 0
        # count = 0
        # for i in reversed(self.coefficients):
        #     ans += i*np.power(x, count)
        #     count += 1
        # return ans

    def eval_derivative(self, x):
        '''
        eval_derivative: to find the value of the derivative with value x
        :param x: value to evaluate polynomial
        :return: derivative evaluated with x
        '''
        p=0
        for i in self.derivative:
            p = p*x+i
        return p
        # ans = 0
        # count = 0
        # for i in reversed(self.derivative):
        #     ans += i*np.power(x, count)
        #     count += 1
        # return ans    

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
