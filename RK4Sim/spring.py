import pygame
import numpy as np

from settings import *
from pivot import Pivot
from Vector import Vector

class Spring ():
    def __init__(self, p1, p2, k) -> None:
        self.p1 = p1
        self.p2 = p2
        self.k = k
        self.length = self.p1.pos.distance(self.p2.pos)

        self.env = self.p1.env

    def funcx(self, particle, s, theta):
        return -self.k/particle.mass * (s * np.cos(theta) - self.length)
    def funcy(self, particle, s, theta):
        return -self.k/particle.mass * (s * np.sin(theta) - self.length)

    def update(self):
        diff = self.p2.pos - self.p1.pos
        dist = diff.magnitude()
        dhat = diff.normal()

        displacement = dist - self.length

        Fx = self.k * (dist - self.length) * dhat.x
        Fy = self.k * (dist - self.length) * dhat.y

        F = Vector(Fx, Fy)


        if not isinstance(self.p1, Pivot):
            #RK4
            h1x = self.env.dt * self.funcx(self.p1, displacement, self.p1.pos.angle(self.p2.pos))
            h2x = self.env.dt * self.funcx(self.p1, displacement + h1x/2, self.p1.pos.angle(self.p2.pos))
            h3x = self.env.dt * self.funcx(self.p1, displacement + h2x/2, self.p1.pos.angle(self.p2.pos))
            h4x = self.env.dt * self.funcx(self.p1, displacement + h3x, self.p1.pos.angle(self.p2.pos))
            self.p1.pos.x += (h1x + 2*h2x + 2*h3x + h4x) / 6

            h1y = self.env.dt * self.funcy(self.p1, displacement, self.p1.pos.angle(self.p2.pos))
            h2y = self.env.dt * self.funcy(self.p1, displacement + h1y/2, self.p1.pos.angle(self.p2.pos))
            h3y = self.env.dt * self.funcy(self.p1, displacement + h2y/2, self.p1.pos.angle(self.p2.pos))
            h4y = self.env.dt * self.funcy(self.p1, displacement + h3y, self.p1.pos.angle(self.p2.pos))


            #self.p1.pos.x += (Fx / self.p1.mass) * self.env.dt
            #self.p1.pos.y += (Fy / self.p1.mass) * self.env.dt
        if not isinstance(self.p2, Pivot):
            h1x = self.env.dt * self.funcx(self.p2, displacement, self.p2.pos.angle(self.p1.pos))
            h2x = self.env.dt * self.funcx(self.p2, displacement + h1x/2, self.p2.pos.angle(self.p1.pos))
            h3x = self.env.dt * self.funcx(self.p2, displacement + h2x/2, self.p2.pos.angle(self.p1.pos))
            h4x = self.env.dt * self.funcx(self.p2, displacement + h3x, self.p2.pos.angle(self.p1.pos))
            self.p2.pos.x += -(h1x + 2*h2x + 2*h3x + h4x) / 6

            h1y = self.env.dt * self.funcy(self.p2, displacement, self.p2.pos.angle(self.p1.pos))
            h2y = self.env.dt * self.funcy(self.p2, displacement + h1y/2, self.p2.pos.angle(self.p1.pos))
            h3y = self.env.dt * self.funcy(self.p2, displacement + h2y/2, self.p2.pos.angle(self.p1.pos))
            h4y = self.env.dt * self.funcy(self.p2, displacement + h3y, self.p2.pos.angle(self.p1.pos))
            self.p2.pos.y += -(h1y + 2*h2y + 2*h3y + h4y) / 6

            #self.p2.pos.x += (-Fx / self.p2.mass) * self.env.dt
            #self.p2.pos.y += (-Fy / self.p2.mass) * self.env.dt

        self.draw()

    def draw(self):
        pygame.draw.line(self.env.WIN, BLACK, ((int(self.p1.pos.x), int(self.p1.pos.y))), ((int(self.p2.pos.x), int(self.p2.pos.y))), 3)