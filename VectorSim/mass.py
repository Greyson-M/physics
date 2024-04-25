from typing import Any
import pygame
import numpy as np

class Mass():
    def __init__(self, env, mass, radius, pos, color) -> None:
        self.env = env
        self.mass = mass
        self.radius = radius
        self.pos = pos
        self.color = color

        self.held = False
        self.charge = 100000

    def update(self):
        if self.held:
            mouse_pos = pygame.mouse.get_pos()
            self.pos = np.array([mouse_pos[0], mouse_pos[1]])

    def draw(self):
        pygame.draw.circle(self.env.WIN, self.color, self.pos, self.radius)