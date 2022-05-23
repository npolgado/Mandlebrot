import pygame, time, random, os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class Painter:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Fractals Babyy')

        self.pixels = 1000
        self.screen = pygame.display.set_mode((self.pixels, self.pixels))

        self.clear()

        self.draw_skeleton()

        self.update()

    def draw_skeleton(self):
        pygame.draw.line(self.screen, (0,0,0), (self.pixels/2, 10), (self.pixels /2, self.pixels - 10))   # vertical line
        pygame.draw.line(self.screen, (0, 0, 0), (10, self.pixels/2), (self.pixels - 10, self.pixels/2))  # horizontal line


    def draw_pixel(self, x, y):
        color = (0, 0, 255)
        # print(x, y)
        self.screen.fill(color, ((x,y), (3, 3)))

        self.update()

    def clear(self):
        self.screen.fill((255, 255, 255))
        self.update()

    def update(self):
        pygame.display.flip()