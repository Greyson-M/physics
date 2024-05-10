import pygame
import numpy as np
import math
from random import randint

from Solver import Solver
from camera import Camera

WIDTH, HEIGHT = 800, 800
FPS = 144

class Environment():
    def __init__(self):
        self.dt = 0.1
        self.freq = 20

        self.CENTER = np.array([WIDTH//2, HEIGHT//2])
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.BG = ((17, 7, 30))
        self.WIN.fill(self.BG)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("3-Body Problem Simulation")

        self.sysfont = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(None, 18)

        # pos = [[-100, 0], [100, 0], [0, 0]]
        # pos = [p + self.CENTER for p in pos]
        # v = ((0.347113,0.532727), (0.347113,0.532727), (-0.694226,-1.065454))
        # m = np.ones(3)*100
        # self.solver = Solver(self, np.array(pos), v, m)

        self.solver = self.gen_random_bodies(25, 150)
        # self.solver = self.gen_grid_bodies(25)

        self.Cam = Camera(self, self.solver)

    def dist(self, pos1, pos2):
        v = pos1 - pos2
        d_sq = v[0] * v[0] + v[1] * v[1]
        return math.sqrt(d_sq)

    def dist_from_center(self, pos):
        return self.dist(pos, self.CENTER)

    def gen_grid_bodies(self, n):
        l = round(np.sqrt(n))
        pos = []
        v = []
        m = np.ones(n)*1

        spaceing = 40

        for i in range(l):
            for j in range(l):
                pos.append((self.CENTER - np.array([l//2, l//2])) + np.array([i*spaceing, j*spaceing]))
                v.append([0, 0])
                # v.append([randint(-1, 1), randint(-1, 1)])

        return Solver(self, np.array(pos), v, m)

    
    def gen_random_bodies(self, n, radius):
        pos = np.array([])
        v = np.zeros((n, 2))
        m = np.ones(n)*1


        #gen random points within a circle
        alpha = 2 * math.pi * np.random.rand(n)
        r = radius * np.sqrt(np.random.rand(n))
        pos = [self.CENTER 
    + np.array([r[i] * math.cos(alpha[i]), r[i] * math.sin(alpha[i])]) for i in range(n)]

        return Solver(self, np.array(pos), v, m)
    
    def draw_spawn_circle(self, radius):
        pygame.draw.circle(self.WIN, (255, 255, 255), self.CENTER, radius, 1)

    def update(self):
        
        self.WIN.fill(self.BG)
        self.clock.tick(FPS)


        #display fps in window title
        pygame.display.set_caption("3-Body Problem Simulation | FPS: " + str(int(self.clock.get_fps())))

        # self.draw_spawn_circle(150)

        for _ in range(self.freq):
            self.solver.solve_next()

        self.Cam.update()
        
        # self.solver.draw()
        # self.solver.draw_center_of_mass()

        # self.solver.draw_tracer()

        pygame.display.update()