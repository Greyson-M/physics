import pygame
from settings import *
import numpy as np

class Tube():
    def __init__(self, rect, p1, p2, vertical=False):
        self.environment = p1.environment
        self.rect = rect
        self.p1 = p1
        self.p2 = p2
        self.vertical = vertical

        self.pressureArea = rect.width * rect.height
        self.n = self.pressureArea / 10
        self.R = GAS_CONSTANT
        self.T = 400
        self.pressure = (self.n*self.R*self.T)/self.pressureArea

        if not vertical:
            self.top = pygame.draw.line(self.environment.WIN, BLACK, self.rect.topleft, self.rect.topright, width=4)
            self.bottom = pygame.draw.line(self.environment.WIN, BLACK, self.rect.bottomleft, self.rect.bottomright, width=4)
        else:
            self.left = pygame.draw.line(self.environment.WIN, BLACK, self.rect.topleft, self.rect.bottomleft, width=4)
            self.right = pygame.draw.line(self.environment.WIN, BLACK, self.rect.topright, self.rect.bottomright, width=4)

    def draw(self):
        if self.vertical:
            self.left = pygame.draw.line(self.environment.WIN, BLACK, self.rect.topleft, self.rect.bottomleft, width=4)
            self.right = pygame.draw.line(self.environment.WIN, BLACK, self.rect.topright, self.rect.bottomright, width=4)
        else:
            self.top = pygame.draw.line(self.environment.WIN, BLACK, self.rect.topleft, self.rect.topright, width=4)
            self.bottom = pygame.draw.line(self.environment.WIN, BLACK, self.rect.bottomleft, self.rect.bottomright, width=4)

        self.update()

        pressureDisp = self.environment.font.render("Pressure: " + str(round(self.pressure)), True, BLACK)
        self.environment.WIN.blit(pressureDisp, (self.rect.x, self.rect.y - 20))

        areaDisp = self.environment.font.render("VOLUME: " + str(round(self.pressureArea)), True, BLACK)
        self.environment.WIN.blit(areaDisp, (self.rect.x, self.rect.y - 40))


    def update(self):
        if (self.rect.collidepoint(self.p1.pos + np.array((self.p1.radius, self.p1.radius))) and self.rect.collidepoint(self.p2.pos + np.array((self.p2.radius, self.p2.radius))) 
            or self.rect.collidepoint(self.p1.pos - np.array((self.p1.radius, self.p1.radius))) and self.rect.collidepoint(self.p2.pos - np.array((self.p1.radius, self.p1.radius)))):
        #if self.rect.collidepoint(self.p1.pos) and self.rect.collidepoint(self.p2.pos):
            if not self.vertical:
                self.p1.pos[1]= self.rect.centery
                self.p2.pos[1]= self.rect.centery

                self.pressureArea = self.rect.height * abs((self.p2.pos[0]) - (self.p1.pos[0]))
                self.pressure = (self.n*self.R*self.T)/self.pressureArea

                SA = self.rect.height
                F = self.pressure * SA
                self.p1.applyForce(np.array((F, 0)))
                self.p2.applyForce(np.array((-F, 0)))

    