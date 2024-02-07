import pygame
import numpy as np

class Cell():
        def __init__(self, x, y) -> None:
            self.x = x
            self.y = y
            self.state = 0

class Grid():
    
    def __init__(self, env, grain_size, draw_lines=True) -> None:
        self.draw_lines = draw_lines
        self.env = env
        self.grain_size = grain_size

        #self.SAND_COLOR = ((227, 178, 93))
        self.SAND_COLOR = ((0,0,0))

        #self.cells = [[Cell(x, y) for x in range(self.env.WIDTH//self.grain_size)] for y in range(self.env.HEIGHT//self.grain_size)]
        self.cells = []
        for y in range(0, self.env.HEIGHT, self.grain_size):
            self.cells.append([])
            for x in range(0, self.env.WIDTH, self.grain_size):
                self.cells[y//self.grain_size].append(Cell(x, y))

        
    
    def get_index(self, x, y):
        return x//self.grain_size, y//self.grain_size
    
    def get_cell(self, x, y):
        return self.cells[self.get_index(x, y)[1]][self.get_index(x, y)[0]]
    
    def add_sand(self, x, y):
        self.get_cell(x, y).state = 1


    def update(self):
        
        check = False
        if self.env.frame_count % 5 == 0:
            check = True

        visited = []

        for j in range(len(self.cells)):
            for i in range(len(self.cells[0])):
                if self.cells[j][i].state == 1 and self.cells[j][i] not in visited and check:

                    if j < len(self.cells)-1:
                        if self.cells[j+1][i].state == 0:
                            self.cells[j][i].state = 0
                            self.cells[j+1][i].state = 1
                            visited.append(self.cells[j+1][i])


    def draw(self):
        for col in self.cells:
            for cell in col:
                if cell.state == 1:
                    pygame.draw.rect(self.env.WIN, self.SAND_COLOR, (cell.x, cell.y, self.grain_size, self.grain_size))
                if self.draw_lines:
                    pygame.draw.rect(self.env.WIN, (0, 0, 0), (cell.x, cell.y, self.grain_size, self.grain_size), 1)