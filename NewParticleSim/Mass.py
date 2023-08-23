import pygame
import numpy as np
from numba import njit

@njit(fastmath=True)
def fastNorm(v):
    return np.sqrt(v[0]*v[0] + v[1]*v[1])


class Mass():
    def __init__(self, env, radius, mass, pos, color=(0, 0, 0)) -> None:
        self.env = env
        self.grid = self.env.grid
        self.radius = radius
        self.mass = mass
        self.pos = pos
        self.acc = np.array([0, 0])
        self.color = color

        self.kinetic_energy = 0

        self.prevPos = self.pos

        self.prev_dhat = np.array([0, 0])
        self.dhat = np.array([0, 0])

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.radius*2, self.radius*2)

        self.cell = None


    def draw(self):
        pygame.draw.circle(self.env.WIN, self.color, self.pos, self.radius)
        pygame.draw.circle(self.env.WIN, self.env.BLACK, self.pos, self.radius, 1)
        #pygame.draw.rect(self.env.WIN, self.env.BLACK, self.rect, 1)

    def update(self):
        self.kinetic_energy = abs((self.mass * fastNorm(self.getVelocity())**2) / 2)
        self.cell = self.grid.getCell(self.pos)
        self.cell.particles.append(self)
        #self.cell.color = self.color

        self.prev_dhat = self.dhat
        self.verletIntegration()
        
        self.draw()
        self.rect = pygame.Rect(self.pos[0] - self.radius*2, self.pos[1] - self.radius*2, self.radius*4, self.radius*4)

    def verletIntegration(self):
        self.dhat = (self.pos - self.prevPos) / fastNorm(self.pos - self.prevPos)
        displacement = self.pos - self.prevPos
        self.prevPos = self.pos
        self.pos = self.pos + displacement + self.acc * (self.env.dt*self.env.dt)
        self.acc = np.array([0, 0])

    def accelerate(self, a):
        self.acc = self.acc + a
    
    def setVelocity(self, v):
        self.prevPos = self.pos - (v * self.env.dt)

    def addVelocity(self, v):
        self.prevPos = self.prevPos - v * self.env.dt

    def getVelocity(self):
        return (self.pos - self.prevPos) / self.env.dt
        