import pygame
import numpy as np
from Settings import *


class Camera:
    def __init__(self, env) -> None:
        self.env = env
        self.target = None

        self.offset = np.array((0, 0))

        self.center = np.array((WIDTH / 2, HEIGHT / 2))
        

    def initialize(self):
        self.grid = self.env.Grid
        
    def update(self):
        
        if self.target != None:
            self.offset = self.target.pos - self.center