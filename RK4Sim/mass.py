from Vector import Vector
from utils import *
from settings import *


import pygame
import numpy as np

class Mass():
    def __init__(self, env, mass, radius, pos, color) -> None:
        self.env = env
        self.mass = mass
        self.pos = pos
        self.prevPos = pos
        self.color = color
        self.radius = radius

        self.vel = Vector(0, 0)
        self.accel = Vector(0, 0)

        self.lastPos = self.pos
        self.lastVel = self.vel

        self.energy = 0

        self.held = False

        self.force_queue = []

    def update(self):
        self.force_queue = []
        self.accel = Vector(0, g)
        

        if self.held:
            self.pos = Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            self.vel = (self.pos - self.lastPos) *self.env.dt #/ (self.env.dt * 10)
            self.accel = (self.vel - self.lastVel)*self.env.dt  #/ (self.env.dt * 10)

            self.lastVel = self.vel
            self.lastPos = self.pos    

        else:
            self.collideWall()

            self.verlet()

        self.draw()

        self.energy = (1/2) * self.mass * self.vel.magnitude()**2

    def collideWall(self):
        bounce_loss = -1
        if self.pos.x - self.radius < leftwall:
            self.pos.x = leftwall + self.radius
            self.vel.x *= bounce_loss
        if self.pos.x + self.radius > rightwall:
            self.pos.x = rightwall - self.radius
            self.vel.x *= bounce_loss
        if self.pos.y - self.radius < topwall:
            self.pos.y = topwall + self.radius
            self.vel.y *= bounce_loss
        if self.pos.y + self.radius > bottomwall:
            self.pos.y = bottomwall - self.radius
            self.vel.y *= bounce_loss

    def draw(self):
        pygame.draw.circle(self.env.WIN, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        #print ("drawn at", self.pos.x, self.pos.y)

    def verlet(self):
        self.vel = (self.pos * 2) - self.prevPos
        self.prevPos = self.pos
        self.pos = self.vel + self.accel * self.env.dt**2
        self.vel = self.pos - self.prevPos
        self.accel = Vector(0, g)


    def applyForce(self, force):
        self.force_queue.append(force)

    def RK4(self):
        for f in self.force_queue:
            self.updateAccel(f)
        self.updateVel()
        self.updatePos()

    def updateAccel(self, force):
        self.accel += force / self.mass


    def updateVel(self):
        #RK4
        k1 = self.accel
        k2 = self.accel + k1 * (1/2)
        k3 = self.accel + k2 * (1/2)
        k4 = self.accel + k3

        self.vel += (k1 + k2 * 2 + k3 * 2 + k4) * (1/6) * self.env.dt

    def updatePos(self):
        #RK4
        k1 = self.vel
        k2 = self.vel + k1 * (1/2)
        k3 = self.vel + k2 * (1/2)
        k4 = self.vel + k3 

        self.pos += (k1 + k2*2 + k3*2 + k4) * (1/6) * self.env.dt

