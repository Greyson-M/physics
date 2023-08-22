import pygame
import numpy as np

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

    def checkDirectionChange(self):
        inertia_constant = 0.2
        self.dhat = (self.pos - self.prevPos) / np.linalg.norm(self.pos - self.prevPos)
        #print ("current direction: " + str(self.dhat) + " previous direction: " + str(self.prev_dhat))

        

        if np.dot(self.dhat, self.prev_dhat) < 0:
            print ("Direction Change")
            self.setVelocity(self.getVelocity() * inertia_constant)

    def draw(self):
        pygame.draw.circle(self.env.WIN, self.color, self.pos, self.radius)
        pygame.draw.circle(self.env.WIN, self.env.BLACK, self.pos, self.radius, 1)
        #pygame.draw.rect(self.env.WIN, self.env.BLACK, self.rect, 1)

    def update(self):
        self.kinetic_energy = abs((self.mass * np.linalg.norm(self.getVelocity())**2) / 2)
        self.cell = self.grid.getCell(self.pos)
        self.cell.particles.append(self)
        #self.cell.color = self.color

        self.prev_dhat = self.dhat
        self.verletIntegration()
        #self.checkDirectionChange()
        
        self.draw()
        self.rect = pygame.Rect(self.pos[0] - self.radius*2, self.pos[1] - self.radius*2, self.radius*4, self.radius*4)

    def verletIntegration(self):
        self.dhat = (self.pos - self.prevPos) / np.linalg.norm(self.pos - self.prevPos)
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
        