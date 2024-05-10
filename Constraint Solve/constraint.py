import numpy as np
import pygame

from mass import Mass

class Constraint:
    def __init__(self, env, p1, p2):
        self.env = env
        self.p1 = p1
        self.p2 = p2
        self.length = np.linalg.norm(p1.pos - p2.pos)

    def solve(self):
        if (type(self.p1) == type(self.p2) == Mass):
            delta = self.p2.pos - self.p1.pos
            dist = np.linalg.norm(delta)
            error = 0.5 * (dist - self.length) / dist
            self.p1.pos += error * delta
            self.p2.pos -= error * delta
        if (type(self.p1) == Mass and type(self.p2) == Constraint):
            delta = self.p2.p1.pos - self.p1.pos
            dist = np.linalg.norm(delta)
            error = 1 * (dist - self.length) / dist
            self.p1.pos += error * delta
            #self.p2.p1.pos -= error * delta
        if (type(self.p1) == Constraint and type(self.p2) == Mass):
            delta = self.p2.pos - self.p1.p1.pos
            dist = np.linalg.norm(delta)
            error = 1 * (dist - self.length) / dist
            #self.p1.p1.pos += error * delta
            self.p2.pos -= error * delta

    def draw(self):
        pygame.draw.line(self.env.WIN, (255, 255, 255), self.p1.pos.astype(int), self.p2.pos.astype(int), 1)