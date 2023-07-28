import pygame
import numpy as np
import math
import time

FPS = 30
WIDTH, HEIGHT = 600, 600
CENTER = np.array([WIDTH/2, HEIGHT/2])

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
dt = (1/FPS)

pi = math.pi

#load
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN.fill((217, 217, 217))
clock = pygame.time.Clock()

sysfont = pygame.font.get_default_font()
font = pygame.font.SysFont(None, 18)

g = -9.81

size = 32
overrelaxation = 1.8

class cell():
    def __init__(self, x, y, density=0, u=0, v=0, s=1):
        self.x = x
        self.y = y
        self.u = v
        self.v = u
        self.density = density

        self.s = s

        self.divergence = 0

        self.pressure = 0

    def calcGravity(self):
        self.v += g*dt

    def calcDivergence(self, nextCell_i, nextCell_j, prevCell_i, prevCell_j):
        divergence = (nextCell_i.u - self.u + nextCell_j.v - self.v)*overrelaxation
        totalS = nextCell_i.s + nextCell_j.s + prevCell_i.s + prevCell_j.s

        if divergence > 0:
            self.u += divergence/4 * (prevCell_i.s/totalS)
            nextCell_i.u -= divergence/4 * (nextCell_i.s/totalS)
            self.v += divergence/4 * (prevCell_j.s/totalS)
            nextCell_j.v -= divergence/4 * (nextCell_j.s/totalS)

    def calcPressure(self):
        self.pressure = self.density * self.s

    


class grid():
    def __init__(self):
        self.cells = [[cell(x, y) for x in range(HEIGHT)] for y in range(WIDTH)]



class Fluid():
    def __init__(self):
        self.numX = WIDTH//size + 2
        self.numY = HEIGHT//size + 2
        self.numCells = self.numX * self.numY
        
        self.vel = np.zeros((self.numX, self.numY, 2))
        self.newU = []
        self.newV = []

        self.density = np.zeros((self.numX, self.numY))

        self.s = []

        self.divergence = np.zeros((self.numX, self.numY))

        self.cells = [[cell(x*size, y*size) for x in range(self.numX)] for y in range(self.numY)]
        self.cells[5][5].density = 200

    def draw(self):
        #self.setBound()
        self.calcGrav()
        self.calcDivergence()
        

        for i in range(self.numX):
            for j in range(self.numY):
                cell = self.cells[i][j]
                x = i * size
                y = j * size

                '''
                dx = self.u[i, j]
                dy = self.v[i, j]
                pygame.draw.line(WIN, BLACK, (x, y), (x+dx, y+dy), 1)
                '''

                pygame.draw.rect(WIN, ((255, 255, 255)), (x, y, size, size), 1)
                pygame.draw.rect(WIN, ((255-cell.density, 255-cell.density, 255-cell.density)), (x, y, size, size))


    def setBound(self):
        self.u[:, 0] = self.u[:, 1]  # Bottom boundary
        self.u[:, -1] = self.u[:, -2]  # Top boundary
        self.u[0, :] = self.u[1, :]  # Left boundary
        self.u[-1, :] = self.u[-2, :]  # Right boundary

        self.v[:, 0] = self.v[:, 1]  # Bottom boundary

    def calcGrav(self):
        for i in range(self.numX):
            for j in range(self.numY):
                self.cells[i][j].calcGravity()

    def calcDivergence(self):
        for i in range(1, self.numX-1):
            for j in range(1, self.numY-1):
                cell = self.cells[i][j]
                self.divergence[i, j] = (self.cells[i+1][j].u - cell.u + self.cells[i][j+1].v - cell.v)*overrelaxation

    def udpateVel(self):
        for i in range(1, self.numX-1):
            for j in range(1, self.numY-1):
                cell = self.cells[i][j]
                up = self.cells[i][j-1]
                down = self.cells[i][j+1]
                left = self.cells[i-1][j]
                right = self.cells[i+1][j]

                

                


def main():
    fluid = Fluid()

    running = True
    while running:
        WIN.fill((217, 217, 217))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting...")
                running = False

        fluid.draw()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()