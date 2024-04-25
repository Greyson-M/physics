import pygame
import numpy as np
from gon import Gon
from collision import Collision

class Environment:
    def __init__(self) -> None:
        self.WIDTH = 1440
        self.HEIGHT = 720
        self.fps = 120
        self.freq = 20
        self.dt = 1 / (self.fps* self.freq)
        pygame.init()
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True

        self.bg = ((217, 217, 217))
        self.WIN.fill(self.bg)

        self.font = pygame.font.Font(None, 14)
        

        p1 = Gon(self, np.array([self.WIDTH//2, self.HEIGHT//2]))
        p2 = Gon(self, np.array([self.WIDTH//2 + 100, self.HEIGHT//2 + 100]))
        self.gons = [p1, p2]

        self.click = False
        self.Collision = Collision(self)

    # def line_line(self, p1, p2, p3, p4):
    #     x1, y1 = p1
    #     x2, y2 = p2
    #     x3, y3 = p3
    #     x4, y4 = p4

    #     den = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    #     if den == 0:
    #         return

    #     ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / den
    #     ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den

    #     if ua >= 0 and ua <= 1 and ub >= 0 and ub <= 1:
    #         x = x1 + ua * (x2 - x1)
    #         y = y1 + ua * (y2 - y1)
    #         return (x, y)

    # def poly_line(self, points, p1, p2):
    #     for i in range(len(points) - 1):
    #         next = (i + 1) % len(points)
    #         pc = points[i]
    #         pn = points[next]

    #         collision_point = self.line_line(pc, pn, p1, p2)
    #         if collision_point:
    #             return collision_point

    # def collision_check(self, p1, p2):
    #     for i in range(len(p1.points) - 1):
    #         next = (i + 1) % len(p1.points)
    #         pc = p1.points[i]
    #         pn = p1.points[next]

    #         collision_point = self.poly_line(p2.points, pc, pn)
    #         if collision_point:
    #             return collision_point
        
    

    def update(self):
        self.WIN.fill(self.bg)
        self.clock.tick(self.fps)

        for gon in self.gons:
            for _ in range(self.freq):
                gon.update()

            gon.draw()

        # if not self.click:
        #     for gon in self.gons:
        #         self.Collision.collision_update(gon)

        for gon in self.gons:
            self.Collision.collision_update(gon)

        pygame.display.update()


