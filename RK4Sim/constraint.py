import pygame
import numpy as np

from settings import *
from Vector import Vector
from utils import *
from pivot import Pivot

class Constraint():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

        self.restLength = self.p1.pos.distance(self.p2.pos)

        self.color = BLACK

    def update(self):
        dist = self.p2.pos.distance(self.p1.pos)

        error = self.restLength - dist
        direction = (self.p2.pos - self.p1.pos).normal()

        dirx = (self.p1.pos.x - self.p2.pos.x) / dist
        diry = (self.p1.pos.y - self.p2.pos.y) / dist

        if not isinstance(self.p1, Pivot):
            if not self.p1.held:
                self.p1.pos.x += dirx * error / 2
                self.p1.pos.y += diry * error / 2
        if not isinstance(self.p2, Pivot):
            if not self.p2.held:
                self.p2.pos.x -= dirx * error / 2
                self.p2.pos.y -= diry * error / 2 

        pygame.draw.line(self.p1.env.WIN, self.color, ((int(self.p1.pos.x), int(self.p1.pos.y))), ((int(self.p2.pos.x), int(self.p2.pos.y))), 3)
