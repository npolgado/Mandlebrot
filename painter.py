import pygame, time, random, os, sys
import numpy as np

# best polynomials:
# 1 8 2 8 1 0 (x**5 + x)
# 1 2 3 4 5 6 7 8 9 10 11 12
#

# TODO: improve color.
#  have a few different color schemes (ie. green) that come packaged with 10 colors that are randomly assigned


class Painter:
    def __init__(self, poly_dict=None, showWindow=True):
        self.showWindow = showWindow
        self.i = 0
        self.__resolution__ = 1000
        self.__scalar__ = 1     # NICK TODO: comment how users should work with these two variables

        self.__size__ = self.__resolution__ * self.__scalar__
        self.__resolution_dict__ = {}

        self.fractal_colors_used = []
        self.colors_used = 0
        self.__init_color_array__()

        if poly_dict != None:
            self.map_color(poly_dict)

        if self.showWindow:
            pygame.init()
            pygame.display.set_caption('Fractals Babyy')
            window_flags = (pygame.RESIZABLE)
            self.__screen__ = pygame.display.set_mode((self.__size__, self.__size__), flags=window_flags)
            self.clear()
            self.draw_skeleton()
            self.update()

        # pygame.mouse.set_visible(False)

    def handle_gui(self):
        if self.showWindow:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

    def map_color(self, poly_dict):
        # get unique roots in the previous dictionary
        roots = list(set(poly_dict.values())) 
        
        # map each root to a unique color
        color_map = []
        for root in roots:
            col = self.__get_color__()
            color_map.append(col)
        
        for guess in poly_dict.keys():
            root = poly_dict[guess]
            self.__resolution_dict__[guess] = color_map[roots.index(root)]

    def get_resolution(self):
        return self.__resolution__

    def draw_skeleton(self):
        pygame.draw.line(self.__screen__, (0,0,0), (self.__size__/2, 0), (self.__size__/2, self.__size__))   # vertical line
        pygame.draw.line(self.__screen__, (0,0,0), (0, self.__size__/2), (self.__size__, self.__size__/2))  # horizontal line

    def draw_resolution(self, x, y, id):
        pygame.event.get()  # prevents 'pygame not responding' when click or keyboard

        if id in self.__resolution_dict__:
            color = self.__resolution_dict__[id]
        else:
            color = self.fractal_colors_used[np.random.randint(0, len(self.fractal_colors_used)-1)] #choose a random color NOTE: will never reach

        # https://zetcode.com/gui/pyqt5/painting/
        # self.__screen__.set_at() # might be good to test over .fill
        # self.__screen__.blits() # this is also another idea, bliting multiple rectangles after they get calcd.
        self.__screen__.fill(color, ((x*self.__scalar__,y*self.__scalar__), (self.__scalar__, self.__scalar__)))
        self.update()

    def __init_color_array__(self, seed=1):
        if seed == 1:   # green theme
            self.fractal_colors_used = [(0, 255, 255), (8, 143, 143), (125, 249, 255), (80, 200, 120), (34, 139, 34),
                                        (53, 94, 59), (0, 163, 108), (144, 238, 144), (50, 205, 50), (71, 135, 120),
                                        (64, 224, 208), (0, 128, 128), (64, 130, 109)]

        random.shuffle(self.fractal_colors_used)

    def __get_color__(self):    # uses init_color_array and picks the next one that hasn't been used
        ans = self.fractal_colors_used[self.colors_used]
        self.colors_used += 1
        print(f"color={ans}, num={self.colors_used}")
        return ans

    def clear(self):
        self.__screen__.fill((255, 255, 255))
        self.update()

    def update(self):
        pygame.display.flip()

