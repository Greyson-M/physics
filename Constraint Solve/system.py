import pygame
import numpy as np

from mass import Mass
from constraint import Constraint

class System():
    def __init__(self, points, constraints) -> None:
        self.points = points
        self.constraints = constraints

    def update(self):
        for point in self.points:
            point.update()

        for constraint in self.constraints:
            constraint.solve()

    def draw(self):
        for point in self.points:
            point.draw()

        for constraint in self.constraints:
            constraint.draw()

    def move(self, pos):

        for constraint in self.constraints:
            constraint.p1.pos += pos
            constraint.p2.pos += pos