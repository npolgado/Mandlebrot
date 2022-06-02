import pygame, time, random, os

import numpy as np

class Painter:
    def __init__(self, poly_roots=None):
        pygame.init()

        pygame.display.set_caption('Fractals Babyy')

        self.__resolution__ = 250
        self.__scalar__ = 4
        self.__size__ = self.__resolution__ * self.__scalar__
        self.__screen__ = pygame.display.set_mode((self.__size__, self.__size__))

        if poly_roots == None:
            self.__resolution_dict__ = {}
        else:
            self.__resolution_dict__ = poly_roots
            # format dict from old dict (in poly)
            '''
                DICT = {
                    guess = []                  # NOT USED FOR PAINTER
                    root = []                   # CONTAINS DUPLICATES, REDUCE DOWN
                    color = []                  # FILL COLORS BY INDEX 
                }
            '''

        self.clear()
        self.draw_skeleton()
        self.update()

    def get_resolution(self):
        return self.__resolution__

    def draw_skeleton(self):
        pygame.draw.line(self.__screen__, (0,0,0), (self.__size__/2, 0), (self.__size__/2, self.__size__))   # vertical line
        pygame.draw.line(self.__screen__, (0,0,0), (0, self.__size__/2), (self.__size__, self.__size__/2))  # horizontal line

    def draw_resolution(self, x, y, id):

        id_real = round(np.real(id), 5)
        id_imag = round(np.imag(id), 5)

        id_rounded = id_real + id_imag * 1j

        if id_rounded in self.__resolution_dict__.keys():
            color = self.__resolution_dict__[id_rounded]
        else:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.__resolution_dict__[id_rounded] = color

        print(id_rounded, color)
        # time.sleep(1)

        self.__screen__.fill(color, ((x*self.__scalar__,y*self.__scalar__), (self.__scalar__, self.__scalar__)))

        self.update()

    def clear(self):
        self.__screen__.fill((255, 255, 255))
        self.update()

    def update(self):
        pygame.display.flip()

