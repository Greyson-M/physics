import pygame
import numpy as np
from Utils import *
from Settings import *

class Constraint():
    def __init__(self, p1, p2, length) -> None:
        #self.length = length
        self.p1 = p1
        self.p2 = p2
        self.length = pythag(self.p2.pos - self.p1.pos)

        self.environment = self.p1.environment

        self.color = BLACK

        self.mass = p1.mass + p2.mass
        self.angle = 0
        
        self.camera = self.environment.camera

    def applyForce(self, force):
        #self.p1.applyForce(force/2)
        self.p2.applyForce(force/2)

    def applyControl(self, force):
        self.p1.applyForce(force)

    def findAngle(self):
        dx = self.p2.pos[0] - self.p1.pos[0]
        dy = self.p2.pos[1] - self.p1.pos[1]

        angle = np.arctan2(dy, dx)

        return angle


    def update(self):
        distVec = self.p2.pos - self.p1.pos
        distScal = pythag(distVec)

        self.angle = self.findAngle()
        self.p1.angle = self.angle
        self.p2.angle = self.angle

        delta_dist = self.length - distScal
        dx = (self.p1.pos[0] - self.p2.pos[0]) / distScal
        dy = (self.p1.pos[1] - self.p2.pos[1]) / distScal

        dhat = distVec / distScal
        #print (dhat)

        if dx < 0:
            self.color = ((255, 0, 0))
        elif dx > 0:
            self.color = ((0, 255, 0))
        
        
        
        self.p1.pos[0] += dx * delta_dist * 0.5
        self.p1.pos[1] += dy * delta_dist * 0.5
        
        self.p2.pos[0] -= dx * delta_dist * 0.5
        self.p2.pos[1] -= dy * delta_dist * 0.5

        offset = self.camera.offset

        if distScal > self.length:
            pygame.draw.line(self.p1.environment.WIN, ((255, 0, 0)), self.p1.pos - offset, self.p2.pos - offset, 3)
            self.contracting = True
            self.expanding = False
            self.stable = False
        elif distScal < self.length:
            pygame.draw.line(self.p1.environment.WIN, ((0, 255, 0)), self.p1.pos - offset, self.p2.pos - offset, 3)
            self.contracting = False
            self.expanding = True
            self.stable = False
        elif distScal == self.length:
            pygame.draw.line(self.p1.environment.WIN, ((0, 0, 255)), self.p1.pos - offset, self.p2.pos - offset, 3)
            self.contracting = False
            self.expanding = False
            self.stable = True

        else:
            pygame.draw.line(self.p1.environment.WIN, BLACK, self.p1.pos - offset, self.p2.pos - offset, 3)


        pygame.draw.line(self.p1.environment.WIN, self.color, self.p1.pos - offset, self.p2.pos - offset, 3)