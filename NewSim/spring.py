import pygame
import numpy as np
from Utils import *
from settings import *

class Spring:
    def __init__(self, p1, p2, length, k, name='spring', block=False, offset=0):
        self.p1 = p1
        self.p2 = p2
        if length == None:
            self.length = pythag(self.p1.pos - self.p2.pos)
        else:
            self.length = length
        self.k = k

        self.name = name
        self.block = block
        self.offset = offset

        self.stable = False
        self.contracting = False
        self.expanding = False

        self.environment = self.p1.environment

    def __del__(self):
        print("Spring BROKE")

    def update(self):
        self.k = self.environment.stiffness

        if self.block:
            dist = np.array((self.p2.pos[0] - self.p1.pos[0] + self.offset, self.p2.pos[1] - self.p1.pos[1]))

        else:
            dist = self.p2.pos - self.p1.pos

        #print ("{} : {}".format(self.name, pythag(dist)))
        if self.environment.breakable:
            if self.k > 0:
                if pythag(dist) >= self.length*4/self.k:
                    self.environment.springList.remove(self)

        dhat = dist / pythag(dist)
        F = 0.8 * self.k * (pythag(dist) - self.length) * dhat

        self.p1.applyImpulse(F)
        self.p2.applyImpulse(-F)

        

        if self.block:
            if pythag(dist) > self.length:
                pygame.draw.line(self.p1.environment.WIN, ((255, 0, 0)), self.p1.pos, np.array((self.p2.pos[0] + self.offset, self.p2.pos[1])), 3)
                self.contracting = True
                self.expanding = False
                self.stable = False
            if pythag(dist) < self.length:
                pygame.draw.line(self.p1.environment.WIN, ((0, 255, 0)), self.p1.pos, np.array((self.p2.pos[0] + self.offset, self.p2.pos[1])), 3)
                self.contracting = False
                self.expanding = True
                self.stable = False
            if pythag(dist) == self.length:
                pygame.draw.line(self.p1.environment.WIN, ((0, 0, 255)), self.p1.pos, np.array((self.p2.pos[0] + self.offset, self.p2.pos[1])), 3)
                self.contracting = False
                self.expanding = False
                self.stable = True

        else:
            if pythag(dist) > self.length:
                pygame.draw.line(self.p1.environment.WIN, ((255, 0, 0)), self.p1.pos, self.p2.pos, 3)
                self.contracting = True
                self.expanding = False
                self.stable = False
            if pythag(dist) < self.length:
                pygame.draw.line(self.p1.environment.WIN, ((0, 255, 0)), self.p1.pos, self.p2.pos, 3)
                self.contracting = False
                self.expanding = True
                self.stable = False
            if pythag(dist) == self.length:
                pygame.draw.line(self.p1.environment.WIN, ((0, 0, 255)), self.p1.pos, self.p2.pos, 3)
                self.contracting = False
                self.expanding = False
                self.stable = True
        

