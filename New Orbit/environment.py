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

        self.computations_per_frame = 10

    def update(self):
        self.WIN.fill((217, 217, 217))
        self.clock.tick(FPS)

        visited = []

        '''     collision
        for m in self.massList:
            for n in self.massList:
                if m != n :
                    dist = distance(m.pos, n.pos)
                    if dist < m.radius + n.radius:
                        m.vel = -m.vel
                        n.vel = -n.vel
        '''

        


        for i in range(self.computations_per_frame):
            self.threeBody(self.massList[0], self.massList[1], self.massList[2])
            for m in self.massList:
                m.update()

        #display fps
        pygame.display.set_caption("Orbit Simulation | FPS: {}".format(round(self.clock.get_fps())))

    def addMass(self, radius, mass, pos, vel=np.array([0,0]), accel=np.array([0, 0]), color=BLACK, name="Mass"):
        m = self.massList.append(Mass(self, radius, mass, pos, vel, accel, color, name))
        return m
    '''
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
    '''

    def threeBody(self, b1, b2, b3):
        G = 3

        pos1 = b1.pos
        pos2 = b2.pos
        pos3 = b3.pos

        m1 = b1.mass
        m2 = b2.mass
        m3 = b3.mass

        r12 = np.linalg.norm(pos1 - pos2)
        r13 = np.linalg.norm(pos1 - pos3)

        r23 = np.linalg.norm(pos2 - pos3)
        r21 = np.linalg.norm(pos2 - pos1)

        r31 = np.linalg.norm(pos3 - pos1)
        r32 = np.linalg.norm(pos3 - pos2)

        thresh = 3.5

        if (r12 > thresh and r13 > thresh):
            accel1 = (-G * m2 * (pos1 - pos1) / pow(r12, 3)) - (G * m3 * (pos1 - pos3) / pow(r13, 3))
        else: accel1 = np.array([0, 0])

        if (r23 > thresh and r21 > thresh):
            accel2 = (-G * m3 * (pos2 - pos3) / pow(r23, 3)) - (G * m1 * (pos2 - pos1) / pow(r21, 3))
        else: accel2 = np.array([0, 0])

        if (r31 > thresh and r32 > thresh):
            accel3 = (-G * m1 * (pos3 - pos1) / pow(r31, 3)) - (G * m2 * (pos3 - pos2) / pow(r32, 3))
        else: accel3 = np.array([0, 0])

        b1.accel = accel1
        b2.accel = accel2
        b3.accel = accel3