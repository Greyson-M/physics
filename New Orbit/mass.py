import pygame
import numpy as np

from settings import *
from utils import *

class Mass():
    def __init__(self, env, radius, mass, pos, vel, accel, color=BLACK, name="Mass") -> None:
        self.env = env
        self.radius = radius
        self.mass = mass
        self.color = color
        self.pos = pos
        self.vel = vel
        self.accel = accel

        self.name = name

        self.prevPos = self.pos

    def update(self):
        self.eulerMethod()
        
        self.draw()

    def eulerMethod(self):
        self.vel = self.vel + self.accel * dt/self.env.computations_per_frame
        self.pos = self.pos + self.vel * dt/self.env.computations_per_frame

    def verletMethod(self):
        self.vel = 2 * self.pos - self.prevPos
        self.prevPos = self.pos
        self.pos = self.vel + self.accel * dt**2 
        self.vel = self.pos - self.prevPos

    def draw(self):
        pygame.draw.circle(self.env.WIN, self.color, self.pos, self.radius)

        velText = self.env.font.render("Velocity: ({}, {})".format(round(self.vel[0]), round(self.vel[1])), True, BLACK)
        #self.env.WIN.blit(velText, (self.pos[0] - 50, self.pos[1] - 50))

    def addForce(self, forvec):
    
        self.accel = self.accel + (forvec/self.mass)

        
    
