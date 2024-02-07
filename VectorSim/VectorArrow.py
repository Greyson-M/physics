import pygame
import numpy as np

from utils import *

class VectorArrow():
    def __init__(self, env, pos) -> None:
        self.env = env
        self.pos = pos
        self.vel = np.array([0, 0])
        self.acc = np.array([0, 0])

        self.color = (0, 0, 0)
        self.size = 10

        self.mass = 1000
        self.charge = 5000

        print (self.pos)

    def update(self):
        #self.vel = self.vel + self.acc * self.env.dt
        #self.vel = self.rotate(self.vel, np.pi/400)
        pass
        
        
    def rotate(self, vec, angle):
        rot_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                               [np.sin(angle), np.cos(angle)]])
        return np.matmul(rot_matrix, vec)

    def scale (self, vec, factor):
        return vec * factor
        
        

    def draw(self):
        factor = 0.1
        buffer = 5

        

        closest_mass_dist = 10000


        for m in self.env.mass_list:
            closest_mass_dist = min(dist(self.pos, m.pos), closest_mass_dist)


        mag = np.linalg.norm(self.vel)
        if mag != 0:
            unit_vec = self.vel/mag
        else:
            unit_vec = self.vel

        if len(self.env.mass_list) > 0:
            if mag > closest_mass_dist - self.env.mass_list[0].radius:
                mag = closest_mass_dist - self.env.mass_list[0].radius - buffer        

        if mag > 50:
            mag = 50
        disp_len = mag
        disp_vec = unit_vec * disp_len

        

        #if self.pos[1] < 200 and self.pos[0] > 400:
        #    print (unit_vec, self.pos, self.vel)

        pygame.draw.line(self.env.WIN, self.color, self.pos, self.pos + disp_vec, self.size//3)
        endpoint = self.pos + disp_vec

        #arrow head
        arrow_angle = np.pi/4       #45 degrees
        
        head_vec1 = self.rotate(-unit_vec, arrow_angle) * disp_len*factor
        head_vec2 = self.rotate(-unit_vec, -arrow_angle) * disp_len*factor

        pygame.draw.line(self.env.WIN, self.color, endpoint, endpoint + head_vec1, self.size//3)
        pygame.draw.line(self.env.WIN, self.color, endpoint, endpoint + head_vec2, self.size//3)
        pygame.draw.circle(self.env.WIN, self.color, self.pos, self.size//2)

        self.vel = np.array([0, 0])
