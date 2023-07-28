from random import randint
from Utils import *
from mass import Mass
import pygame
import numpy as np
from settings import *

class Puck(Mass):
    randRadius = randint(5, 50)
    randPos = np.array((randint(110, 720), randint(55, 380)))
    randVel = np.array((randint(0, 10), randint(0, 10)))
    randColor = (( randint(0, 255), randint(0, 255), randint(0, 255) ))

    def __init__(self, environment, mass=randint(1, 50), pos = randPos, vel = randVel, color=randColor, radius=randRadius, name="Puck"):
        super().__init__(environment, mass, pos, vel, color, name=name)
        self.radius = radius
        self.surface_area = self.radius
        self.name = name

        self.kineticEnergy = 0

        self.cell = np.array((0, 0))

    def update(self, mousePos, t):
        self.cell = np.array((int(self.pos[0] // self.environment.grid.step), int(self.pos[1] // self.environment.grid.step)))

        if not self.held:
            self.kineticEnergy = 0.5 * self.mass * pow(pythag(self.vel), 2)

        self.updatePos(mousePos, t)
        self.collision()

    def collision(self):
        mult = 1.8
        if self.pos[0] + self.vel[0] * dt  <= leftwall + self.radius:
            self.vel[0] = -self.vel[0] * mult
        if self.pos[0] + self.vel[0] * dt >= rightwall - self.radius:
            self.vel[0] = -self.vel[0] * mult
        if self.pos[1] + self.vel[1] * dt <= topwall + self.radius:
            self.vel[1] = -self.vel[1] * mult
        if self.pos[1] + self.vel[1] * dt >= bottomwall - self.radius:
            self.vel[1] = -self.vel[1]*mult
        
        '''
        if self.pos[1] + self.vel[1] * dt + self.radius >= self.environment.blockList[0].box.top:
            #print ("collided")
            self.pos[1] = self.environment.blockList[0].box.top - self.radius
            self.vel[1] = -self.vel[1]
            '''

        if self.pos[0] <= leftwall + self.radius:
            self.pos[0] = leftwall + self.radius
        if self.pos[0] >= rightwall - self.radius:
            self.pos[0] = rightwall - self.radius
        if self.pos[1] <= topwall + self.radius:
            self.pos[1] = topwall + self.radius
        if self.pos[1] >= bottomwall - self.radius:
            self.pos[1] = bottomwall - self.radius
                
        
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
        dvel1 = -2 * collider.mass/total_mass * np.inner(self.vel-collider.vel, self.pos-collider.pos) / np.sum( (self.pos-collider.pos)**2) * (self.pos-collider.pos)
        dvel2 = -2 * self.mass/total_mass * np.inner(collider.vel-self.vel, collider.pos-self.pos) / np.sum( (collider.pos-self.pos)**2) * (collider.pos-self.pos)
        self.vel = self.vel+dvel1
        collider.vel = collider.vel + dvel2

    def draw(self, mousePos, t):
        self.update(mousePos, t)

        pygame.draw.circle (self.environment.WIN, self.color, self.pos, self.radius)