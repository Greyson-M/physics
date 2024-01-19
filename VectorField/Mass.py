import numpy as np
import pygame
from settings import *
import math
from random import randint
from utils import *


class Mass:
    def __init__(self, env, pos = np.array([WIDTH/2, HEIGHT/2]), vel = np.array([0, 0]), mass = 1, radius = 1, color = BLACK):
        self.env = env
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.radius = radius
        self.color = color
        
        self.cell = np.array([0,0])

        self.kineticEnergy = 0

    def __del__(self):
        print ("mass destroyed")

    def update(self):
        if self.pos[0] > 0 and self.pos[0] < WIDTH and self.pos[1] > 0 and self.pos[1] < HEIGHT:
            x = self.pos[0]
            y = self.pos[1]
            self.cell = np.array([int(self.pos[0]//self.env.field.step), int(self.pos[1]//self.env.field.step)])
            #print(self.cell)

            #self.vel = self.env.field.cells[self.cell[1]][self.cell[0]].velocity
            #print (self.vel)
            self.vel[0] = y/(2*math.sqrt(x*y))
            self.vel[1] = x/(2*math.sqrt(x*y))
            self.pos = self.pos + self.vel * dt * SPEED
            
            self.kineticEnergy = 0.5 * self.mass * self.vel**2

            red = int((pythag(self.vel)/1000) * 255)

            if red < 255: self.color = (red, 0, 0)
            else: self.color = (0, 0, 255)
            print (self.color)

        else:
            self.env.massList.remove(self)
            self.env.massList.append(Mass(self.env, np.array([randint(0, WIDTH), randint(0, HEIGHT)]), np.array([0, 0]), self.mass, self.radius, self.color))

        self.draw()

    def draw(self):
        pygame.draw.circle(self.env.WIN, self.color, self.pos, self.radius)

    