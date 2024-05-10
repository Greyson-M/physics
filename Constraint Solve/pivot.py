import numpy as np
import pygame

from constraint import Constraint

class Pivot():
    def __init__(self, env, pos, m1) -> None:
        self.env = env
        self.pos0 = np.array(pos, dtype=float)
        self.pos = np.array(pos, dtype=float)
        self.m1 = m1

        self.constraint = Constraint(env, m1, self)

    def update(self):
        self.constraint.solve()
        self.pos = self.pos0

    def draw(self):
        self.pos = self.pos0
        pygame.draw.circle(self.env.WIN, (255, 255, 255), self.pos.astype(int), 5)
        pygame.draw.circle(self.env.WIN, (0, 0, 0), self.pos.astype(int), 5, 1)
        self.constraint.draw()




