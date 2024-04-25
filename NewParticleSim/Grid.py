import pygame
import numpy as np
from numba import njit

cell_size = 20

def checkBounds(pos):
    return pos[0] > 0 and pos[0] < 1280 and pos[1] > 0 and pos[1] < 720
    #return np.all(pos > np.array([0,0])) and np.all(pos < np.array([1280, 720]))
    
@njit(fastmath=True)
def fastNorm(v):
    return np.sqrt(v[0]*v[0] + v[1]*v[1])
@njit(fastmath=True)
def fastSQ(v1, v2=None):
    if v2 is None:
        return v1 * v1
    
    disp = v1 - v2
    return disp[0]*disp[0] + disp[1]*disp[1]

class Grid():
    
    class Cell:
        def __init__(self, env, x, y, grid, OOB=False) -> None:
            self.grid = grid
            self.OOB = OOB
            self.env = env
            self.x = x
            self.y = y
            self.color = self.env.BLACK
            self.rect = pygame.Rect(self.x, self.y, self.env.cell_size, self.env.cell_size)

            self.highlight = False

            self.particles = []
            self.directions = np.array([[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]])


        def getIndex(self):
            return (self.x/self.env.cell_size, self.y/ self.env.cell_size)

        def update(self):
            
            '''leftover = []
            for p in self.particles:
                if self.rect.collidepoint(p.pos):
                    leftover.append(p)

            self.particles = leftover'''
            if self.OOB:
                self.particles = []
            if not self.OOB:
                if len(self.particles) == 1:
                    self.color = self.env.BLUE
                elif len(self.particles) > 1:

                    #print (self.particles)
                    self.color = self.env.RED
                    for p in self.particles:
                        for p2 in self.particles:
                            if p != p2:
                                distsq = pow(p.pos[0] - p2.pos[0], 2) + pow(p.pos[1] - p2.pos[1], 2)
                                minDist = p.radius + p2.radius
                                self.env.collisionResponse(p, p2)
                                if distsq > minDist*minDist:
                                    self.particles.remove(p)
                                    self.particles.remove(p2)

                else:
                    self.color = self.env.BLACK

                if len(self.particles) > 0:
                    self.checkCollision(self.particles)

                self.particles = []

        def checkCollision(self, particles):
            for i, particle in enumerate(particles):
                #print (i)
                eps = 0.0001

                for dir in self.directions:
                    adjacent_cell = self.grid.getCell(particle.pos + dir * self.env.cell_size)
                    if len(adjacent_cell.particles) > 0:
                        for p in adjacent_cell.particles:
                            if p != particle:
                                disp = particle.pos - p.pos
                                #distsq = fastSQ(disp[0]) + fastSQ(disp[1])
                                distsq = disp[0]*disp[0] + disp[1]*disp[1]
                                minDist = particle.radius + p.radius
                                if distsq < minDist*minDist and distsq > eps:
                                    self.env.collisionResponse(particle, p)
                                    
            

    def __init__(self, env) -> None:
        self.env = env

        self.cells = [[self.Cell(self.env, x, y, self) for x in range(0, self.env.WIDTH, self.env.cell_size)] for y in range(0, self.env.HEIGHT, self.env.cell_size)]
        self.empty_cell = self.Cell(self.env, -1, -1, self, OOB=True)

        self.max_x = len(self.cells[0]) - 1
        self.max_y = len(self.cells) - 1

    def draw(self):
        for row in self.cells:
            for cell in row:
                #print (str(cell.getIndex()) + ": " + str(len(cell.particles)) + " particles")
                if cell.highlight:
                    pygame.draw.rect(self.env.WIN, self.env.GREEN, cell.rect)
                '''else:
                    pygame.draw.rect(self.env.WIN, cell.color, cell.rect, 1)'''


                cell.update()


    def getCell(self, pos):
        if checkBounds(pos):
            return self.cells[int(pos[1] // cell_size)][int(pos[0] // cell_size)]
        else:
            return self.empty_cell

