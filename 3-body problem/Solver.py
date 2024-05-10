import numpy as np
import pygame

class Solver():
    def __init__(self, env, positions, m1, m2, m3) -> None:
        self.G = 1 #6.67408e-11
        self.env = env

        self.pos1 = self.env.CENTER + np.array(positions[0]*10)
        self.pos2 = self.env.CENTER + np.array(positions[1]*10)
        self.pos3 = self.env.CENTER + np.array(positions[2]*10)

        self.m1 = m1
        self.m2 = m2
        self.m3 = m3

        self.t = 0

        # self.vel1 = np.array([0,0])
        # self.vel2 = np.array([0,0])
        # self.vel3 = np.array([0,0])

        self.vel1 = np.array([-1,0])
        self.vel2 = np.array([0,-1])
        self.vel3 = np.array([1,0])

    def solve_next(self):
        r12 = np.linalg.norm(self.pos1 - self.pos2)
        r13 = np.linalg.norm(self.pos1 - self.pos3)

        r23 = np.linalg.norm(self.pos2 - self.pos3)
        r21 = np.linalg.norm(self.pos2 - self.pos1)

        r31 = np.linalg.norm(self.pos3 - self.pos1)
        r32 = np.linalg.norm(self.pos3 - self.pos2)

        accel1 = (-self.G * self.m2 * (self.pos1 - self.pos2) / pow(r12, 3)) - (self.G * self.m3 * (self.pos1 - self.pos3) / pow(r13, 3))
        accel2 = (-self.G * self.m3 * (self.pos2 - self.pos3) / pow(r23, 3)) - (self.G * self.m1 * (self.pos2 - self.pos1) / pow(r21, 3))
        accel3 = (-self.G * self.m1 * (self.pos3 - self.pos1) / pow(r31, 3)) - (self.G * self.m2 * (self.pos3 - self.pos2) / pow(r32, 3))

        self.vel1 = self.vel1 + accel1*self.env.dt
        self.vel2 = self.vel2 + accel2*self.env.dt
        self.vel3 = self.vel3 + accel3*self.env.dt

        self.pos1 = self.pos1 + self.vel1*self.env.dt
        self.pos2 = self.pos2 + self.vel2*self.env.dt
        self.pos3 = self.pos3 + self.vel3*self.env.dt

        self.t += self.env.dt

        print (self.pos1, self.pos2, self.pos3)

    def draw(self):
        pygame.draw.circle(self.env.WIN, (255, 0, 0), self.pos1, 3)
        pygame.draw.circle(self.env.WIN, (0, 255, 0), self.pos2, 3)
        pygame.draw.circle(self.env.WIN, (0, 0, 255), self.pos3, 3)