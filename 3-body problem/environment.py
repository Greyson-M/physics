import pygame
import numpy as np
import math

from Solver import Solver

WIDTH, HEIGHT = 800, 800
FPS = 144

class Environment():
    def __init__(self):
        self.dt = 0.01
        self.freq = 10

        self.CENTER = (WIDTH//2, HEIGHT//2)
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.BG = ((17, 7, 30))
        self.WIN.fill(self.BG)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("3-Body Problem Simulation")

        self.sysfont = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(None, 18)

        self.solver = Solver(self, np.array([[-10, 0], [0, -10], [10, 0]]), 100, 100, 100)

    def update(self):
        self.WIN.fill(self.BG)
        self.clock.tick(FPS)

        for _ in range(self.freq):
            self.solver.solve_next()
            self.solver.draw()

        pygame.display.update()