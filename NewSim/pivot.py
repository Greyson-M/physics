import numpy as np
import pygame
from Utils import *
from settings import *

class Pivot():

    def __init__(self, environment, pos, name=None) -> None:
        self.pos = pos
        self.environment = environment
        self.name = name
        self.type = "Pivot"

    def draw(self):
        pygame.draw.circle(self.environment.WIN, BLACK, self.pos, 10, width=4)
        if self.name == "Spinner":
            pygame.draw.rect(self.environment.WIN, ((92, 122, 150)), (self.pos[0] - 10, self.pos[1] - 10, 20, 20), width=4)
        if self.name == "Generator":
            pygame.draw.rect(self.environment.WIN, ((0, 255, 0)), (self.pos[0] - 10, self.pos[1] - 10, 20, 20), width=4)

    def applyImpulse(self, impulse):
        pass