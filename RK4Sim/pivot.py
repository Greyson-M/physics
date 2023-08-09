import numpy as np
import pygame

from settings import *

class Pivot():
    def __init__(self, env, pos) -> None:
        self.pos = pos
        self.env = env 

    def update(self):
        pygame.draw.circle(self.env.WIN, BLACK, self.pos.tuple(), 5)