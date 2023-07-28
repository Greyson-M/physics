import pygame
import numpy as np
from Utils import *
from settings import *

class Spring:
    def __init__(self, p1, p2, length, k):
        self.p1 = p1
        self.p2 = p2
        self.length = length
        self.k = k

    def update(self):
        dx = self.p1.pos[0] - self.p2.pos[0]
        dy = self.p1.pos[1] - self.p2.pos[1]
        dist = pythag((dx, dy))
        theta = math.atan2(dy, dx)
        force = self.k * abs(self.length - dist)

        theta1 = theta + math.pi/2
        theta2 = theta - math.pi/2

        forcex1 = force * math.cos(theta1)
        forcey1 = force * math.sin(theta1)

        forcex2 = force * math.cos(theta2)
        forcey2 = force * math.sin(theta2)


        force1 = np.array((forcex1, forcey1))
        force2 = np.array((forcex2, forcey2))

        print(force1, force2)

        self.p1.accelerate(-force1)
        self.p2.accelerate(-force2)

        pygame.draw.line(self.p1.environment.WIN, BLACK, self.p1.pos, self.p2.pos, 1)

