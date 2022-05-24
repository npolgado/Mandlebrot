import pygame, time, random, os

class Painter:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Fractals Babyy')

        self.__pixels__ = 1000
        self.__screen__ = pygame.display.set_mode((self.pixels, self.pixels))

        self.__pixel_dict__ = {}

        self.clear()
        self.draw_skeleton()
        self.update()

    def get_pixels(self):
        return self.__pixels__

    def draw_skeleton(self):
        pygame.draw.line(self.screen, (0,0,0), (self.pixels/2, 0), (self.pixels/2, self.pixels))   # vertical line
        pygame.draw.line(self.screen, (0,0,0), (0, self.pixels/2), (self.pixels, self.pixels/2))  # horizontal line

    def draw_pixel(self, x, y, id):
        print(f"id={id}  ({x}, {y})")

        if id in self.__pixel_dict__.keys():
            color = self.__pixel_dict__[id]

        else:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.__pixel_dict__[id] = color

        self.screen.fill(color, ((x,y), (1, 1)))

        self.update()

    def clear(self):
        self.screen.fill((255, 255, 255))
        self.update()

    def update(self):
        pygame.display.flip()

# TODO:
#  - change "roots" pixels -> get_pixels
