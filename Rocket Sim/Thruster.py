import pygame
from Settings import *
import numpy as np

class Thruster():
    def __init__(self, constraint, size) -> None:
        self.constraint = constraint
        self.pos = constraint.p2.pos

        self.environment = constraint.env
        self.color = BLACK

        self.size = size

        self.camera = self.environment.camera

    def draw(self):
        offset = self.camera.offset
        point1 = np.array([self.pos[0]+self.size, self.pos[1] + self.size])
        point2 = np.array([self.pos[0]-self.size, self.pos[1] + self.size])
        pygame.draw.polygon(self.environment.WIN, self.color, (self.pos - offset, point1 - offset, point2 - offset), 2)

    def displayStats(self, force):
        offset = self.camera.offset
        font = pygame.font.SysFont("Arial", 12)
        text = font.render("Force: " + str(force), True, BLACK)
        self.environment.WIN.blit(text, (self.pos[0] - offset[0], self.pos[1] + 20 - offset[1]))

    def update(self):
        self.pos = self.constraint.p2.pos

        self.applyThrust()

        self.draw()


    def applyThrust(self):
        #force = np.array((0, -20 * self.environment.t))
        force = np.array((0, 0))

        if pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_UP]:
                force = np.array((0, -600))

        self.displayStats(force)



        self.constraint.applyForce(force)
