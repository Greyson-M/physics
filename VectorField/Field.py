import pygame
from settings import *
import math
import numpy as np
from utils import *

class Field:
    class Cell:
        def __init__(self, x, y, size):
            self.x = x
            self.y = y
            self.size = size
            self.rect = pygame.Rect(x, y, size, size)
            self.density = 0
            self.velocity = np.array([0,0])
            self.index = 0

    def __init__(self, env, step):
        self.step = step
        self.env = env
        self.cells = [[self.Cell(x, y, self.step) for x in range(0, WIDTH, self.step)] for y in range(0, HEIGHT, self.step)]
        print ("created field: {} x {}".format(len(self.cells[0]), len(self.cells)))

    def draw(self):
        for row in self.cells:
            for cell in row:
                pygame.draw.rect(self.env.WIN, (255, 255, 255), cell.rect, 1)

    def update(self):
        self.cells = [[self.Cell(x, y, self.step) for x in range(0, WIDTH, self.step)] for y in range(0, HEIGHT, self.step)]

        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                if i is not 0 and j is not 0:
                    cell.velocity[0] = j/(2*math.sqrt(i*j))
                    cell.velocity[1] = i/(2*math.sqrt(i*j))


        if DRAW_GRID: self.draw()