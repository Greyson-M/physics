import numpy as np
from random import randint
import pygame
from settings import *
from environment import Environment
from Utils import *

class Mass:
    randPos = np.array((randint(110, 720), randint(55, 380)))
    randVel = np.array((randint(0, 10), randint(0, 10)))
    randColor = (( randint(0, 255), randint(0, 255), randint(0, 255) ))

    def __init__(self, environment, mass = randint(1, 50), pos = randPos, vel = randVel, color = randColor, name=None):
        self.mass = mass
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

    def gravForce(self):
        if not self.surface and not self.held:
            grav_force = np.array((0, self.environment.g * self.mass))
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


    def updatePos(self, mousePos, t):
        if self.held:
            if (t*60)%10 < 1:
                self.prevPos = self.pos

        if self.held == True:
            self.pos = mousePos
            self.vel = (self.pos - self.prevPos) * 2

        if not self.held:
            integration = "EULER"

            if integration == "EULER":
                #EULER INTEGRATION
                self.accel = self.gravForce()/self.mass
                self.vel = self.vel + self.accel * dt * SPEED
                self.pos = self.pos + self.vel * dt * SPEED
            
            

            if integration == "VERLET":
                #VERLET INTEGRATION
                self.vel = 2 * self.pos - self.prevPos
                self.prevPos = self.pos
                self.pos = self.vel + self.accel * dt**2 * SPEED
                self.vel = self.pos - self.prevPos
                self.accel = self.gravForce()/self.mass
            

            if integration == "RK4":
                #RK4 INTEGRATION
                k1 = self.vel
                k2 = self.vel + 0.5 * k1 * dt
                k3 = self.vel + 0.5 * k2 * dt
                k4 = self.vel + k3 * dt
                self.pos = self.pos + (1/6) * (k1 + 2*k2 + 2*k3 + k4) * dt * 30
            
            

            '''
            self.vel = self.vel + (self.gravForce()/self.mass) * dt * SPEED

            if not self.surface:
                self.pos = self.pos + self.vel * dt * SPEED
            else:
                self.pos[0] = self.pos[0] + self.vel[0] * dt * SPEED
                '''

    def accelerate(self, forvec):
    
        self.vel = self.vel + (forvec/self.mass) #* dt * SPEED

    def applyImpulse(self, impulse):
        self.pos = np.add(self.pos, impulse/self.mass * dt * SPEED)
        #if self.name == 'blue':
            #print ("{} force applied to {}".format(impulse, self.name))

    def applyForce(self, force):
        self.accel = np.add(self.accel, force/self.mass)

        #RK4 INTEGRATION
        k1 = force/self.mass
        k2 = force/self.mass + 0.5 * k1 * dt
        k3 = force/self.mass + 0.5 * k2 * dt
        k4 = force/self.mass + k3 * dt
        self.vel = (k1 + 2*k2 + 2*k3 + k4)/6