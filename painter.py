import pygame, time, random, os, sys
import numpy as np

class Painter:
    def __init__(self, poly_dict=None, showWindow=True):
        self.showWindow = showWindow
        self.i = 0
        self.__resolution__ = 500
        self.__scalar__ = 1000//self.__resolution__
        self.__size__ = self.__resolution__ * self.__scalar__
        self.__resolution_dict__ = {}

        if poly_dict != None:
            self.sort_dict(poly_dict)          

        if self.showWindow:
            pygame.init()
            pygame.display.set_caption('Fractals Babyy')
            window_flags = (pygame.RESIZABLE)
            self.__screen__ = pygame.display.set_mode((self.__size__, self.__size__), flags=window_flags)
            self.clear()
            self.draw_skeleton()
            self.update()

        pygame.mouse.set_visible(False)

    def handle_gui(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def sort_dict(self, poly_dict):
        # get unique roots in the previous dictionary
        roots = list(set(poly_dict.values())) 
        
        # map each root to a unique color
        color_map = []
        for root in roots:
            color_map.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        
        for guess in poly_dict.keys():
            root = poly_dict[guess]
            self.__resolution_dict__[guess] = color_map[roots.index(root)]

    def get_resolution(self):
        return self.__resolution__

    def draw_skeleton(self):
        pygame.draw.line(self.__screen__, (0,0,0), (self.__size__/2, 0), (self.__size__/2, self.__size__))   # vertical line
        pygame.draw.line(self.__screen__, (0,0,0), (0, self.__size__/2), (self.__size__, self.__size__/2))  # horizontal line

    def draw_resolution(self, x, y, id):
        pygame.event.get()
        # if (self.i % 10000 == 0):
        #     print(self.i)
        # self.i += 1
        # pass

        # id_real = round(np.real(id), 5)
        # id_imag = round(np.imag(id), 5)
        
        # id_rounded = id_real + id_imag * 1j
        
        if id in self.__resolution_dict__:
            color = self.__resolution_dict__[id]
        else:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.__resolution_dict__[id] = color
        
        # print(id_rounded, color)
        # time.sleep(1)

        # self.__screen__.set_at((x*self.__scalar__, y*self.__scalar__), color)
        self.__screen__.fill(color, ((x*self.__scalar__,y*self.__scalar__), (self.__scalar__, self.__scalar__)))
        self.update()

    def clear(self):
        self.__screen__.fill((255, 255, 255))
        self.update()

    def update(self):
        pygame.display.flip()

