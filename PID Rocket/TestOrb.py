import pygame
import numpy as np
from Settings import *

class TestOrb():
    def __init__(self, env) -> None:
        self.env = env
        self.pos = np.array((WIDTH / 2, HEIGHT / 2))

        self.camera = self.env.camera


    def update(self):
        offset = self.camera.offset

        if pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.pos[1] -= 1
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                self.pos[1] += 1
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.pos[0] -= 1
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.pos[0] += 1

        pygame.draw.circle(self.env.WIN, BLACK, self.pos - offset, 10)