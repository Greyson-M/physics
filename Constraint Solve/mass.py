import numpy as np
import pygame

class Mass:
    def __init__(self, env, pos, mass=1):
        self.env = env
        self.pos = np.array(pos, dtype=float)
        self.vel = np.zeros(2, dtype=float)
        self.g = 9.81
        self.acc = np.array([0, self.g], dtype=float)
        self.mass = mass

    def apply_force(self, force):
        self.acc += force / self.mass

    def update(self):
        self.vel = self.vel + (self.acc * self.env.dt) * self.env.speed
        self.pos = self.pos + (self.vel * self.env.dt) * self.env.speed
        self.acc = np.array([0, self.g], dtype=float)

        #boundary
        if self.pos[0] < 0:
            self.vel[0] *= -1
            self.pos[0] = 0
        if self.pos[0] > self.env.WIDTH:
            self.vel[0] *= -1
            self.pos[0] = self.env.WIDTH
        if self.pos[1] < 0:
            self.vel[1] *= -1
            self.pos[1] = 0
        if self.pos[1] > self.env.HEIGHT:
            self.vel[1] *= -1
            self.pos[1] = self.env.HEIGHT

    def draw(self):
        pygame.draw.circle(self.env.WIN, (255, 255, 255), self.pos.astype(int), 5)
        pygame.draw.circle(self.env.WIN, (0, 0, 0), self.pos.astype(int), 5, 1)