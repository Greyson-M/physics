import pygame
import numpy as np
import math

from settings import *
from mass import Mass
from utils import *

class Environment():
    def __init__(self):
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.WIN.fill((217, 217, 217))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Orbit Simulation")

        self.sysfont = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(None, 18)

        self.massList = []

        self.drawList = [self.massList]

    def update(self):
        self.WIN.fill((217, 217, 217))
        self.clock.tick(FPS)

        visited = []

        for m in self.massList:
            for n in self.massList:
                if m != n :
                    dist = distance(m.pos, n.pos)
                    if dist < m.radius + n.radius:
                        m.vel = -m.vel
                        n.vel = -n.vel



                    self.calcGravVerlet(m, n)


        for m in self.massList:
            m.update()

    def addMass(self, radius, mass, pos, vel=np.array([0,0]), accel=np.array([0, 0]), color=BLACK, name="Mass"):
        m = self.massList.append(Mass(self, radius, mass, pos, vel, accel, color, name))
        return m

    def calcGrav(self, b1, b2):
        force = b1.mass * b2.mass / distance(b1.pos, b2.pos) ** 2
        angle = math.atan2(b2.pos[1] - b1.pos[1], b2.pos[0] - b1.pos[0])

        accerlation1 = force / b1.mass
        accx1 = accerlation1 * math.cos(angle)
        accy1 = accerlation1 * math.sin(angle)

        accerlation2 = force / b2.mass
        accx2 = accerlation2 * math.cos(angle)
        accy2 = accerlation2 * math.sin(angle)

        #print ("{}: ({}, {})".format(b2.name, accx2, accy2))

        b1.vel[0] += accx1
        b1.vel[1] += accy1
        b2.vel[0] -= accx2
        b2.vel[1] -= accy2

    def calcGravVerlet(self, b1, b2):
        if distance(b1.pos, b2.pos) < b1.radius + b2.radius:
            maxMass = max(b1.mass, b2.mass)
            if maxMass == b1.mass:
                b1.mass += b2.mass
                self.massList.remove(b2)
            else:
                b2.mass += b1.mass
                self.massList.remove(b1)

        force = b1.mass * b2.mass / (distance(b1.pos, b2.pos) ** 2 + DAMPENING)
        angle = math.atan2(b2.pos[1] - b1.pos[1], b2.pos[0] - b1.pos[0])

        Fx = force * math.cos(angle)
        Fy = force * math.sin(angle)

        b1.addForce(np.array([Fx, Fy]))
        b2.addForce(np.array([-Fx, -Fy]))