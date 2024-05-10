import pygame
import numpy as np

from system import System
from mass import Mass
from constraint import Constraint
from pivot import Pivot

class Environment():
    def __init__(self) -> None:
        self.WIDTH = 1440
        self.HEIGHT = 720
        self.fps = 120
        self.freq = 20
        self.dt = 1 / (self.fps)
        self.speed = 10
        pygame.init()
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True

        self.bg = ((4, 22, 46))
        self.WIN.fill(self.bg)

        self.font = pygame.font.Font(None, 14)

        m1 = Mass(self, np.array([100, 100]))
        m2 = Mass(self, np.array([200, 100]))
        m3 = Mass(self, np.array([150, 200]))
        
        points = [m1, m2, m3]
        constraints = [Constraint(self, points[0], points[1]), Constraint(self, points[1], points[2]), Constraint(self, points[2], points[0])]
        self.system = System(points, constraints)

        self.pivot = Pivot(self, np.array([150, 0]), m1)
        

    def update(self):
        self.clock.tick(self.fps)
        self.WIN.fill(self.bg)

        self.system.update()
        self.system.draw()

        self.pivot.update()
        self.pivot.draw()

        pygame.display.update()