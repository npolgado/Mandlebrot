import matplotlib.pyplot as plt
import numpy as np
import main as m
import sys, time

# def print_bar(progress, total):
#     '''
#     print_bar: uses total and progress to determine progress in percentage

#     :param progress: current progress (less than total)
#     :param total: total amount of iterations

#     :return: None (plots graph)
#     '''
#     percent = 100 * (progress / float(total))
#     bar = '*' * int(percent) + '-' * (100-int(percent))
#     print(f"\r|{bar}| {percent:.2f}%", end='\r')

def get_iter(c:complex, thresh:int =4, max_steps:int =25) -> int:
    # Z_(n) = (Z_(n-1))^2 + c
    # Z_(0) = c
    z=c
    i=1
    while i<max_steps and (z*z.conjugate()).real<thresh:
        z=z*z +c
        i+=1
    return i

def plotter(n, thresh, max_steps=25):
    mx = 2.48 / (n-1)
    my = 2.26 / (n-1)
    mapper = lambda x,y: (mx*x - 2, my*y - 1.13)
    img=np.full((n,n), 255)
    # total = n*n
    # count = 0
    # print_bar(count, total)
    for x in range(n):
        for y in range(n):
            it = get_iter(complex(*mapper(x,y)), thresh=thresh, max_steps=max_steps)
            img[y][x] = 255 - it
            # print(f"\r {x} , {y}", end='\r')
            # count += 1
            # print_bar(count, total)
    return img

if __name__ == "__main__":
    if len(sys.argv) > 1: 
        print(sys.argv[1:])
        n = int(sys.argv[1])
        print("loading image...")
        img = plotter(n, thresh=4, max_steps=50)
        print("Image found!")
        plt.imshow(img, cmap="Spectral")
        plt.axis("off")
        plt.show()
    else:
        print("didn't load N... \n\tusing 1000...")
        n=1000
        print("loading image...")
        img = plotter(n, thresh=4, max_steps=50)
        print("Image found!")
        plt.imshow(img, cmap="plasma")
        plt.axis("off")
        plt.show()