import math
from VectorArrow import VectorArrow

import numpy as np
import pygame

def GravFunction(mass1, mass2):
    grav_const = 0.001
    dist = np.linalg.norm(mass1.pos - mass2.pos)
    if dist > 0:
        F = grav_const * (mass1.mass * mass2.mass) / (dist**2)
        unit_vec = (mass2.pos - mass1.pos) / dist
        F = -unit_vec * F

        return F
    
def ElectricFunction(charge1, charge2):
    elec_const = 0.001
    dist = np.linalg.norm(charge1.pos - charge2.pos)
    if dist > 0:
        F = elec_const * (charge1.charge * charge2.charge) / (dist**2)
        unit_vec = (charge2.pos - charge1.pos) / dist
        F = -unit_vec * F

        return F


class Field():
    def __init__(self, env, step) -> None:
        self.env = env
        self.step = step
        self.vectors = [[VectorArrow(env, np.array([x, y])) for y in range(0, 720, self.step)] for x in range(0, 1280, self.step)]

        self.grav_const = 0.001

        self.max_mag = 0

    def update(self):
        for row in self.vectors:
            for vector in row:

                self.max_mag = max(self.max_mag, np.linalg.norm(vector.vel))

                #grav force field
                vec_mass = 1000
                x = vector.pos[0]
                y = vector.pos[1]
                
                if x != 0 and y != 0:
                    vector.vel[0] = x*x - y*y
                    vector.vel[1] = 2*x*y
                


                vector.update()

    def draw(self):
        for row in self.vectors:
            for vector in row:
                vector.draw()

        if self.env.drawGrid:
            self.draw_grid()

    def draw_grid(self):
        grid_color = (50, 50, 50)
        for x in range(0, 1280, self.step):
            pygame.draw.line(self.env.WIN, grid_color, (x, 0), (x, 720), 1)

        for y in range(0, 720, self.step):
            pygame.draw.line(self.env.WIN, grid_color, (0, y), (1280, y), 1)
