import pygame
from settings import *

class Grid:
    class Cell:
        def __init__(self, x, y, size) -> None:
            self.x = x
            self.y = y
            self.size = size
            self.color = BLACK
            
            self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
            self.particles = []
            

    def __init__(self, env, step) -> None:
        self.environment = env
        self.step = step

        self.cells = [[self.Cell(x, y, self.step) for x in range(0, WIDTH, self.step)] for y in range(0, HEIGHT, self.step)]

       # print ("Creating Grid: {} cells wide, {} cells tall".format(len(self.cells[0]), len(self.cells)))

    def update(self):
        for p in self.environment.puckList:
            #print ("p.cell: " + str(p.cell))
            if p not in self.cells[p.cell[1]][p.cell[0]].particles:
                self.cells[p.cell[1]][p.cell[0]].particles.append(p)

                

    def draw(self):
        self.cells = [[self.Cell(x, y, self.step) for x in range(0, WIDTH, self.step)] for y in range(0, HEIGHT, self.step)]
        self.update()
        #print ("2, 4 particles: " + str(self.cells[2][4].particles))
        for row in self.cells:
            for cell in row:
                #pygame.draw.rect(self.environment.WIN, cell.color, cell.rect, width=1)
                pass