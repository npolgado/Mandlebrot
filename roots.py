'''FINIDNG ROOTS
'''
import numpy as np
import painter as p
import time

SIZE = 1024         # size of canvas
DELTA = 1e-4        # when to stop calculating root
XBOUNDS = 4         # used to calculate the scaling factor for points on find_all_roots
YBOUNDS = 4         # used to calculate the scaling factor for points on find_all_roots

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

class COMPLEX():
    def __init__(self, real, imaginary):
        self.re = float(real)
        self.im = float(imaginary)
    
    def real(self):
        return self.re

    def imag(self):
        return self.im

    def subtract(self, number):
        if type(number) == COMPLEX: # number is complex
            re = self.real() - number.real()
            im = self.imag() - number.imag()
            return COMPLEX(re, im)
        else:
            re = self.real() - number
            im = self.imag() - number
            return COMPLEX(re, im)
    
    def add(self, number):
        if type(number) == COMPLEX: # number is complex
            re = self.real() + number.real()
            im = self.imag() + number.imag()
            return COMPLEX(re, im)
        else:
            re = self.real() + number
            im = self.imag() + number
            return COMPLEX(re, im)

    def divide(self, number):
        if type(number) == COMPLEX: # number is complex
            ac = self.real() * number.real()
            ad = self.real() * number.imag()
            bd = self.imag() * number.imag()
            bc = self.imag() * number.real()
            den = (number.real()**2 + number.imag()**2)
            tmp = (ac+bd)/den
            tmp2 = (bc-ad)/den
            return COMPLEX(tmp, tmp2)
        else:
            return COMPLEX((self.real()/number), self.imag()/number) # number is magnitude

    def multiply(self, number):
        if type(number) == COMPLEX: # number is complex
            ac = self.real() * number.real()
            ad = self.real() * number.imag()
            bd = self.imag() * number.imag()
            bc = self.imag() * number.real()
            tmp = (ac - bd)
            tmp2 = (ad + bc)
            return COMPLEX(tmp, tmp2)
        else:
            return COMPLEX((self.real()*number), self.imag()*number) # number is magnitude

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
        count = 0

        Wscale = XBOUNDS / WIDTH # for 1000, this is 0.002 or the factor to adjust root calculations by
        Hscale = YBOUNDS / HEIGHT # for 1000, this is 0.002 or the factor to adjust root calculations by
       
        w_off = WIDTH / 2
        h_off = HEIGHT / 2

        for x in list(np.linspace(-WIDTH/2, WIDTH/2, WIDTH+1)):
            for y in list(np.linspace(-HEIGHT/2, HEIGHT/2, HEIGHT+1)):
                r = x * Wscale
                i = y * Hscale
                # position = COMPLEX(r, j)
                position = r + (i*1j)
                # position_rounded = self.poly.round_complex(position, 3)

                root = self.poly.round_complex(self.which_root(position), 3)
                    
                if self.showWindow:
                    self.painter.draw_resolution(x+w_off, y+h_off, root)
                
                # count+=1
                # progress = round(float((count/tot)*100), 3)
                # print_bar(count, tot)

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
            
            f_x = self.poly.eval(self.poly.coefficients, guess)
            fp_x = self.poly.eval(self.poly.derivative, guess)

            next_guess = guess - (f_x / fp_x)
            n_guess_r = self.poly.round_complex(next_guess, 3)

            if n_guess_r in self.dict: # found in dict already
                return self.dict[n_guess_r]

            if abs(next_guess - guess) < DELTA: # newly calculated root
                return next_guess               # return actual guess for painting

            guess = next_guess    

        return root_finder_helper(next_guess, self.poly)

class POLY():
    def __init__(self, coefficients, lowerB=-2, upperB=2, n=10):    
        assert(len(coefficients) >= 1)
        if n == 0:
            n = int(len(coefficients)*1.5)+10 # scaled to polynomial length

        self.total_n = int(n*n) # will run through 'n' real *  'n' imag samples
        self.roots_hashed = 0 # number of times a sample was in the dictionary already
        self.roots_calculated = 0 # number of times the sample was calculated through iteration

        self.dict = {}  # init lookup dict
        self.coefficients = coefficients
        self.derivative = list(np.polyder(self.coefficients, 1))

        start_t = time.time()         
        self.roots = self.calc_roots(lowerB, upperB, n)
        end_t = time.time() 

        self.percent_hashed = float((self.roots_hashed / self.total_n) * 100)
        self.percent_calculated = float((self.roots_calculated / self.total_n) * 100)
        self.time_efficiency = float(end_t - start_t)

    def round_complex(self, number, decimal):
        re = float(number.real)
        re_r = round(re, decimal)

        im = float(number.imag)
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
        sampleR = [np.random.uniform(lowerB, upperB) for x in range(N)]
        sampleI = [np.random.uniform(lowerB, upperB) for x in range(N)]

        # roots_saved = 0     # keeps track of how many times the efficiency was triggered
        # num_iterations = []
        # num_maxed_out = 0

        for r in sampleR:
            for i in sampleI:
                guess = r + i*1j
                guess_rounded = self.round_complex(guess, 3)

                if guess_rounded in self.dict:
                    # already found root
                    self.roots_hashed += 1
                    # roots_saved += 1
                    # print(f"already found root (num: {roots_saved})")
                    continue
                else:
                    # root not found
                    # do next_guess
                    original_guess = guess
                    original_guess_r = self.round_complex(original_guess, 3)

                    guesses_path = []
                    guesses_path.append(original_guess_r)

                    isFound = False
                    for iteration in range(maxIter):

                        # if iteration > (2*int(len(self.coefficients)+1)): 
                        #     break # CASE: ran past expect iterations -> root

                        f_x = self.eval(self.coefficients, guess)
                        f_p_x = self.eval(self.derivative, guess)

                        next_guess = guess - (f_x / f_p_x)
                        next_guess_r = self.round_complex(next_guess, 3)

                        if next_guess_r in self.dict:
                            self.roots_hashed += 1
                            # roots_saved += 1
                            # num_iterations.append(iteration)
                            # isFound = True
                            # print(f"already found root (num: {roots_saved})")
                            break

                        guesses_path.append(next_guess_r)

                        if abs(next_guess - guess) < DELTA:  
                            # found a new root!
                            # self.dict[original_guess_r] = next_guess_r
                            self.roots_calculated += int(len(guesses_path))
                            # num_iterations.append(iteration)
                            # isFound = True

                            # add all path elements to the dictionary 
                            for ele in guesses_path:
                                self.dict[ele] = next_guess_r
                            break

                        # not a root this iteration
                        guess = next_guess 
        #             if not isFound:
        #                 num_maxed_out += 1
        #             num_iterations.append(iteration)
        # avg_iter = np.average(num_iterations)
        # self.average_iterations = avg_iter
        # self.didnt_converge = num_maxed_out 

        # print(f"optimized {roots_saved} roots")
        # self.known_roots = roots_saved
        return list(set(self.dict.values()))            

    def eval(self, lst, x):
        '''
        eval: to find the value of the polynomial with value x
        :param x: value to evaluate polynomial
        :return: polynomial evaluated with x
        '''
        p=0
        for i in lst:
            p = p*x+i
        return p   

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
