import pygame
from settings import *
import numpy as np


class Cylinder():
    def __init__(self, env, rect, head, drive):
        self.environment = env
        self.rect = rect
        self.head = head
        self.drive = drive

        self.combustionArea = rect.width * rect.height
        self.n = self.combustionArea / 40
        self.R = GAS_CONSTANT
        self.T = 400
        self.pressure = (self.n*self.R*self.T)/self.combustionArea


        if self.head != "top":
            self.top = pygame.draw.line(self.environment.WIN, BLACK, self.rect.topleft, self.rect.topright, width=4)
        if self.head != "left":
            self.left = pygame.draw.line(self.environment.WIN, BLACK, self.rect.topleft, self.rect.bottomleft, width=4)
        if self.head != "right":
            self.right = pygame.draw.line(self.environment.WIN, BLACK, self.rect.topright, self.rect.bottomright, width=4)
        else:
            self.right = pygame.Rect(100000, 10000, 1, 1)
        if self.head != "bottom":
            self.bottom = pygame.draw.line(self.environment.WIN, BLACK, self.rect.bottomleft, self.rect.bottomright, width=4)

        
        
    def draw(self):
        if self.head != "top":
            self.top = pygame.draw.line(self.environment.WIN, BLACK, self.rect.topleft, self.rect.topright, width=4)
        if self.head != "left":
            self.left = pygame.draw.line(self.environment.WIN, BLACK, self.rect.topleft, self.rect.bottomleft, width=4)
        if self.head != "right":
            self.right = pygame.draw.line(self.environment.WIN, BLACK, self.rect.topright, self.rect.bottomright, width=4)
        if self.head != "bottom":
            self.bottom = pygame.draw.line(self.environment.WIN, BLACK, self.rect.bottomleft, self.rect.bottomright, width=4)


        self.update()

        pressureDisp = self.environment.font.render("Pressure: " + str(round(self.pressure)), True, BLACK)
        self.environment.WIN.blit(pressureDisp, (self.rect.x, self.rect.y - 20))

    def update(self):

        if self.rect.collidepoint(self.drive.pos):
            threshold = 2.2
            if self.drive.pos[0] <= self.rect.left + self.drive.radius * threshold:
                #print("BOOM!")
                self.T *= 1.5
                self.drive.color = ((255, 0, 0))
            else:
                self.T = 300
                self.drive.color = ((75, 175, 200))

            self.drive.pos[1]= self.rect.centery
            self.pressure = (self.n*self.R*self.T)/self.combustionArea

            SA = self.rect.height
            F = self.pressure * SA
            self.drive.applyForce(np.array((F, 0)))

            self.drive.pos[1]= self.rect.centery

        else:
            self.pressure = 0