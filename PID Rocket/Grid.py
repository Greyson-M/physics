import pygame
from Settings import *
import numpy as np

class Grid():
    def __init__(self, environment, cell_width) -> None:
        self.environment = environment
        self.cell_width = cell_width
        self.line_color = ((50, 50, 50))
        self.camera = self.environment.camera

    def draw(self):
        offset = self.camera.offset

        if offset[0] > 0:
            for i in range(0, WIDTH + int(offset[0]), self.cell_width):
                adjusted_i = i - offset[0]
                pygame.draw.line(self.environment.WIN, self.line_color, (adjusted_i, 0), (adjusted_i, HEIGHT))

        
        else:
            for i in range(WIDTH - int(offset[0]), int(offset[0]), -self.cell_width):
                adjusted_i = i - offset[0] * 0.2
                pygame.draw.line(self.environment.WIN, self.line_color, (adjusted_i, 0), (adjusted_i, HEIGHT))

        if offset[1] > 0:
            for i in range(0, HEIGHT + int(offset[1]), self.cell_width):
                adjusted_i = i - offset[1]

                pygame.draw.line(self.environment.WIN, self.line_color, (0, adjusted_i), (WIDTH, adjusted_i))

        
        else:
            for i in range(HEIGHT - int(offset[1]), int(offset[1]), -self.cell_width):
                adjusted_i = i - offset[1] * 0.2
                pygame.draw.line(self.environment.WIN, self.line_color, (0, adjusted_i), (WIDTH, adjusted_i))

        


    