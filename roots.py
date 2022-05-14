'''FINIDNG ROOTS
'''
import numpy as np
import sys

SIZE = 1024         # size of canvas
DELTA = 1e-10       # when to stop calculating root
  
class POLY:
    def __init__(self, coefficients, lowerB=-10, upperB=10, n=30):
        assert(len(coefficients) >= 1)
        self.coefficients = coefficients
        self.derivative = np.polyder(self.coefficients, 1)
        self.roots = self.calc_roots(lowerB, upperB, n)

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
                for n in range(maxIter):
                    next_guess = guess - (self.eval(guess) / self.eval_derivative(guess))
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
            print("found polynomial {}".format(f.get_name()))
            print("roots = {}".format(f.roots))
        except:
            print("couldn't find roots...")
    else:
        pass