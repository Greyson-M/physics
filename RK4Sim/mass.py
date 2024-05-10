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
            self.vel = (self.pos - self.lastPos) *self.env.dt #* (self.env.dt * 10)
            self.accel = (self.vel - self.lastVel)*self.env.dt #* (self.env.dt * 10)

            self.lastVel = self.vel
            self.lastPos = self.pos
            self.prevPos = self.pos 

        else:
            self.collideWall()

            #self.eulerIntegration()
            self.verlet()
            # self.RK4()

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

    
    def eulerIntegration(self):
        self.vel += self.accel * self.env.dt
        self.pos += self.vel * self.env.dt
    
    def interCollide(self, dist, collider):
      #  self.held = False
        dpos = self.pos-collider.pos

        if dist == 0:
            dist = 1

        offset = dist-(self.radius+collider.radius)
        self.pos = self.pos + (-dpos/dist)*offset/2
        collider.pos = collider.pos + (dpos/dist)*offset/2
        total_mass = self.mass+collider.mass
        #print ( np.sum( (self.pos-collider.pos) **2) * (self.pos-collider.pos) )

        if dpos[0] == 0 and dpos[1] == 0:
            #print ("self pos: {} \t colliderpos: {}".format(self.pos, collider.pos))
            self.pos += np.array((self.radius + 5, self.radius + 5))
            collider.pos -= np.array((self.radius + 8, self.radius + 8))
            #print ("adjusted")
            #print ("self pos: {} \t colliderpos: {}".format(self.pos, collider.pos))
            dpos = self.pos-collider.pos

            #print (dpos)

        self_vel = np.array((self.vel.x, self.vel.y))
        collider_vel = np.array((collider.vel.x, collider.vel.y))
        self_pos = np.array((self.pos.x, self.pos.y))
        collider_pos = np.array((collider.pos.x, collider.pos.y))

        dvel1 = -2 * collider.mass/total_mass * np.inner(self_vel-collider_vel, self_pos-collider_pos) / np.sum( (self_pos-collider_pos)**2) * (self_pos-collider_pos)
        dvel2 = -2 * self.mass/total_mass * np.inner(collider_vel-self_vel, collider_pos-self_pos) / np.sum( (collider_pos-self_pos)**2) * (collider_pos-self_pos)
        newselfvel = self_vel+dvel1
        newcollidervel = collider_vel + dvel2
        self.vel = Vector(newselfvel[0], newselfvel[1])
        collider.vel = Vector(newcollidervel[0], newcollidervel[1])
    

