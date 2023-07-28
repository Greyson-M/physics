from constraint import Constraint
from pivot import Pivot
import numpy as np
from settings import *
import math

class Spinner():
    def __init__(self, radius, speed, output) -> None:
        self.output = output
        self.speed = speed
        self.radius = radius
        self.environment = output.environment
        self.pivPos = output.pos - np.array((radius, 0))

        self.pivot = Pivot(self.environment, self.pivPos, "Spinner")
        self.constraint = Constraint(self.pivot, output, radius)

        self.angularVelocity = 0

    def update(self):
        increment = math.pi/1440
        self.pivot.draw()
        self.constraint.update()

        currentAngle = math.atan2(self.output.pos[1] - self.pivPos[1], self.output.pos[0] - self.pivPos[0])
        newAngle = currentAngle + (self.speed * increment)

        dx = self.radius * np.cos(newAngle) * dt
        dy = self.radius * np.sin(newAngle) * dt

        self.angularVelocity = (newAngle - currentAngle) / dt

        self.output.pos =  self.output.pos + np.array((dx, dy))


        angularVelDisp = self.environment.font.render("Angular Velocity: " + str(self.angularVelocity), True, BLACK)
        self.environment.WIN.blit(angularVelDisp, (10, 150))

        