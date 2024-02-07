import pygame
from Settings import *
import numpy as np
from Utils import *

class ControlThruster():
    def __init__(self, constraint, size) -> None:
        self.constraint = constraint
        self.pos = constraint.p2.pos

        self.environment = constraint.env
        self.color = BLACK

        self.size = size

        self.point1 = np.array([self.pos[0]+self.size, self.pos[1] - self.size])
        self.point2 = np.array([self.pos[0]+self.size, self.pos[1] + self.size])
        self.point3 = np.array([self.pos[0]-self.size, self.pos[1] - self.size])
        self.point4 = np.array([self.pos[0]-self.size, self.pos[1] + self.size])

        self.angle = 0

    def rotate(self, angle):
        self.angle += angle
        angle = self.angle

        dp1 = self.point1 - self.pos
        dp1hat = (dp1 / pythag(dp1))
        dp1mag = pythag(dp1)
        dp2 = self.point2 - self.pos
        dp2hat = (dp2 / pythag(dp2))
        dp2mag = pythag(dp2)

        d1rothat = np.array((dp1[0] * np.sin(angle) - dp1[1] * np.cos(angle), dp1[0] * np.cos(angle) + dp1[1] * np.sin(angle)))
        d2rothat = np.array((dp2[0] * np.sin(angle) - dp2[1] * np.cos(angle), dp2[0] * np.cos(angle) + dp2[1] * np.sin(angle)))

        self.point1 = self.pos + d1rothat
        self.point2 = self.pos + d2rothat


        dp3 = self.point3 - self.pos
        dp3hat = (dp3 / pythag(dp3))
        dp3mag = pythag(dp3)
        dp4 = self.point4 - self.pos
        dp4hat = (dp4 / pythag(dp4))
        dp4mag = pythag(dp4)

        d3rothat = np.array((dp3[0] * np.sin(angle) - dp3[1] * np.cos(angle), dp3[0] * np.cos(angle) + dp3[1] * np.sin(angle)))
        d4rothat = np.array((dp4[0] * np.sin(angle) - dp4[1] * np.cos(angle), dp4[0] * np.cos(angle) + dp4[1] * np.sin(angle)))

        self.point3 = self.pos + d3rothat# * dp3mag
        self.point4 = self.pos + d4rothat# * dp4mag

        return d3rothat, d4rothat

    def draw(self):
        
        
        offset = self.environment.camera.offset

        self.point1 = np.array([self.pos[0]+self.size, self.pos[1] - self.size])
        self.point2 = np.array([self.pos[0]+self.size, self.pos[1] + self.size])
        self.point3 = np.array([self.pos[0]-self.size, self.pos[1] - self.size])
        self.point4 = np.array([self.pos[0]-self.size, self.pos[1] + self.size])


        self.rotate((self.constraint.get_angle()) - self.angle)
        #print (self.angle)
        
        pygame.draw.polygon(self.environment.WIN, self.color, (self.pos - offset, self.point1 - offset, self.point2 - offset), 2)
        pygame.draw.polygon(self.environment.WIN, self.color, (self.pos - offset, self.point3 - offset, self.point4 - offset), 2)

    def displayStats(self, force):
        offset = self.environment.camera.offset

        font = pygame.font.SysFont("Arial", 12)
        text = font.render("Force: " + str(force), True, BLACK)
        self.environment.WIN.blit(text, (self.pos[0] - offset[0], self.pos[1] + 20 - offset[1]))

    def update(self):
        self.pos = self.constraint.p1.pos

        self.applyThrust()

        self.draw()


    def applyThrust(self):
        force = np.array((0, 0))
        if pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                f = np.array((-200, 0))
                force = np.array((f[0] * np.sin(self.angle) - f[1] * np.cos(self.angle), f[0] * np.cos(self.angle) + f[1] * np.sin(self.angle)))
                
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                f = np.array((200, 0))
                force = np.array((f[0] * np.sin(self.angle) - f[1] * np.cos(self.angle), f[0] * np.cos(self.angle) + f[1] * np.sin(self.angle)))
                
        self.displayStats(force)

        self.constraint.applyControl(force)
