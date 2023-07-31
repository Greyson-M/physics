import pygame
from settings import *
import numpy as np
from pivot import Pivot
from puck import Puck
from constraint import Constraint
import math
from Utils import *

class Generator:
    def __init__(self, env, pos, radius, mass, start='L') -> None:
        self.env = env
        self.piv = Pivot(env, pos, "Generator")
        if start == 'L':
            self.puck = Puck(env, mass, pos + np.array((radius + 4, 0)), np.array((0,0)), BLACK, 4)
        if start == 'R':
            self.puck = Puck(env, mass, pos - np.array((radius + 4, 0)), np.array((0,0)), BLACK, 4)
        self.constraint = Constraint(self.piv, self.puck, radius)

        self.radius = radius

        self.power = 0
        self.averagePower = 0
        self.t = 0

        self.powerData = []

    def __del__(self):
        #print ("AVG POWER: " + str(round(sum(self.powerData) / len(self.powerData))))
        pass

    def draw(self, mouse_pos, t):
        self.t = t
        self.piv.draw()
        self.puck.draw(mouse_pos, t)
        self.constraint.update()

        self.update()

        powerDisp = self.env.font.render("Power: " + str(round(self.averagePower)), True, BLACK)
        self.env.WIN.blit(powerDisp, (self.piv.pos[0] - 50, self.piv.pos[1] - 50))

    def update(self):
        currAngle = math.atan2(self.puck.pos[1] - self.piv.pos[1], self.puck.pos[0] - self.piv.pos[0])
        prevAngle = math.atan2(self.puck.prevPos[1] - self.piv.pos[1], self.puck.prevPos[0] - self.piv.pos[0])
        dTheta = abs(currAngle - prevAngle) * dt * SPEED

        s = self.radius * dTheta
        work = self.puck.mass * pythag(self.puck.accel) * s
        self.power = work / dt

        if pygame.time.get_ticks() % 100 == 0:
            self.powerData.append(self.power)

        if len(self.powerData) > 10:
            self.averagePower = sum(self.powerData[-10:-1]) / len(self.powerData[-10:-1])


    