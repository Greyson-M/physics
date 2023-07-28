import pygame
import numpy as np
from Utils import *
from settings import *

class Constraint():
    def __init__(self, p1, p2, length) -> None:
        #self.length = length
        self.p1 = p1
        self.p2 = p2
        self.length = pythag(self.p2.pos - self.p1.pos)

        self.environment = self.p1.environment


    def update(self):
        distVec = self.p2.pos - self.p1.pos
        distScal = pythag(distVec)

        delta_dist = self.length - distScal
        dx = (self.p1.pos[0] - self.p2.pos[0]) / distScal
        dy = (self.p1.pos[1] - self.p2.pos[1]) / distScal
        
        if self.p1.type != "Pivot":
            self.p1.pos[0] += dx * delta_dist * 0.5
            self.p1.pos[1] += dy * delta_dist * 0.5
        if self.p2.type != "Pivot":
            self.p2.pos[0] -= dx * delta_dist * 0.5
            self.p2.pos[1] -= dy * delta_dist * 0.5

        
        '''

        Beta = 0.8

        error = distScal - self.length

        force_mag = error/self.length

        diff = (distScal - self.length)/distScal

        dhat = distVec / distScal
        Force_a = distVec * (Beta * diff)
        Force_b = distVec * (-Beta * diff)

        self.p1.applyForce(Force_a)
        self.p2.applyForce(Force_b)
        '''

        if distScal > self.length:
            pygame.draw.line(self.p1.environment.WIN, ((255, 0, 0)), self.p1.pos, self.p2.pos, 3)
            self.contracting = True
            self.expanding = False
            self.stable = False
        elif distScal < self.length:
            pygame.draw.line(self.p1.environment.WIN, ((0, 255, 0)), self.p1.pos, self.p2.pos, 3)
            self.contracting = False
            self.expanding = True
            self.stable = False
        elif distScal == self.length:
            pygame.draw.line(self.p1.environment.WIN, ((0, 0, 255)), self.p1.pos, self.p2.pos, 3)
            self.contracting = False
            self.expanding = False
            self.stable = True

        else:
            pygame.draw.line(self.p1.environment.WIN, BLACK, self.p1.pos, self.p2.pos, 3)


        pygame.draw.line(self.p1.environment.WIN, BLACK, self.p1.pos, self.p2.pos, 3)