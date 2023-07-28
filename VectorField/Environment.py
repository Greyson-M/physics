from settings import *
import pygame
from Field import Field

class Environment():
    def __init__(self) -> None:
        #load
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.WIN.fill((217, 217, 217))

        self.sysfont = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(None, 18)

        self.totalEnergy = 0

        self.field = Field(self, 10)

        self.t = 0

        self.massList = []

    def update(self):
        #self.WIN.fill((217, 217, 217))
        #print(self.t)
        self.field.update()

        for m in self.massList:
            m.update()

        
        

    def clear(self):
        self.WIN.fill((217, 217, 217))
        self.massList = []