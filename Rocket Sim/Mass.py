import numpy as np
from random import randint
import pygame
from Settings import *
from Environment import Environment
from Utils import *

class Mass:
    randPos = np.array((randint(110, 720), randint(55, 380)))
    randVel = np.array((randint(0, 10), randint(0, 10)))
    randColor = (( randint(0, 255), randint(0, 255), randint(0, 255) ))

    def __init__(self, environment, mass = randint(1, 50), radius = randint(1, 50), pos = randPos, vel = randVel, color = randColor, name=None):
        self.mass = mass
        self.radius = radius
        self.pos = pos
        self.prevPos = self.pos
        self.vel = vel
        self.accel = np.array((0, 0))
        self.color = color
        self.environment = environment
        self.surface_area = 0

        self.held = False

        self.surface = False
        self.name = name
        self.type = "Mass"

        self.force = 0

        self.angle = 0

        self.camera = self.environment.camera

    def update(self):
        self.updatePos()
        self.draw()

    def draw(self):
        offset = self.camera.offset
        #print (offset, self.pos)
        pygame.draw.circle(self.environment.WIN, self.color, self.pos - offset, self.radius)


    def gravForce(self):
        if not self.surface and not self.held:
            grav_force = np.array((0, g * self.mass))
            if pythag(self.vel) != 0:
                vhat = self.vel / pythag(self.vel)

                drag_force = 0.0005 * DRAG_COEF * self.surface_area * pythag(self.vel)**2 * (-vhat)
                drag_force = 0

                force = grav_force + drag_force

            else:
                force = grav_force

            return force
        
        else:
            return np.array((0, 0))

    def checkBounds(self):
        if self.pos[1] >= bottomwall - self.radius - self.vel[1] * dt * SPEED:
            #self.pos[1] = bottomwall - self.radius
            self.vel[1] = -self.vel[1] * 0.5

    def updatePos(self):
        
        self.checkBounds()


        self.accel = np.array((0, g)) + self.force/self.mass
        self.vel = self.vel + self.accel * dt * SPEED
        self.pos = self.pos + self.vel * dt * SPEED
            
            
            

    def accelerate(self, forvec):
    
        self.vel = self.vel + (forvec/self.mass) #* dt * SPEED

    def applyImpulse(self, impulse):
        self.pos = np.add(self.pos, impulse/self.mass * dt * SPEED)
        #if self.name == 'blue':
            #print ("{} force applied to {}".format(impulse, self.name))

    def applyForce(self, force):
        self.force = force