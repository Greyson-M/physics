import pygame
import numpy as np
from settings import *

from constraint import Constraint
from pivot import Pivot
from spring import Spring

class Environment():
    def __init__(self):
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.WIN.fill((217, 217, 217))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Physics Simulation")

        self.sysfont = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(None, 18)

        self.dt = (1/FPS)

        self.massList = []
        self.constraintList = []
        self.pivotList = []
        self.springList = []

        self.drawList = [self.massList, self.constraintList, self.pivotList, self.springList]

        self.totalE = []
        self.energyAvg = 0

        self.heldMass = None

    def update(self):
        self.WIN.fill((217, 217, 217))
        self.clock.tick(FPS)

        if self.clock.get_fps() != 0:
            self.dt = 1/self.clock.get_fps() * SPEED

        pygame.draw.rect(self.WIN, BLACK, pygame.Rect(leftwall, topwall, rightwall-100, bottomwall-50),  5)

        currTotalE = 0
        
        for l in self.drawList:
            for obj in l:
                obj.update()
                if hasattr(obj, "energy"):
                    currTotalE += obj.energy

        if self.clock.get_rawtime() % 100 == 0:
            if len(self.totalE) > 20:
                self.totalE.pop(0)
            self.totalE.append(currTotalE)

        if self.clock.get_rawtime() % 500 == 0:
            self.energyAvg = np.mean(self.totalE)
            

        fpsDisplay = self.font.render("FPS: {}".format(round(self.clock.get_fps())), True, BLACK)
        self.WIN.blit(fpsDisplay, (120, 10))

        energyDisplay = self.font.render("Energy: {}".format(round(self.energyAvg)), True, BLACK)
        self.WIN.blit(energyDisplay, (120, 30))
        
        pygame.display.flip()

    def addMass(self, mass):
        self.massList.append(mass)
        return mass

    def addConstraint(self, p1, p2):
        const = Constraint(p1, p2)
        self.constraintList.append(const)
        return const
    
    def addPivot(self, pos):
        piv = Pivot(self, pos)
        self.pivotList.append(piv)
        return piv
    
    def addSpring(self, p1, p2, k):
        spring = Spring(p1, p2, k)
        self.springList.append(spring)
        return spring
