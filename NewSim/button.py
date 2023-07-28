import numpy as np
import pygame
from Utils import *
from environment import *
from settings import *

class Button:
    def __init__(self, env, text, rect) -> None:
        self.text = text
        self.rect = rect
        self.pos = np.array((self.rect.x, self.rect.y))
        self.font = env.font

        self.hoverColor = ((50, 80, 50))
        self.defaultColor = ((50, 50, 50))
        self.color = self.defaultColor

        self.width = 3

        self.environment = env

        self.clicked = False
        self.timeClicked = 0
        self.cooldown = 0.5

    def draw(self):
        self.checkClick()

                

        #print("DRAWING: {}".format(self.rect))
        pygame.draw.rect(self.environment.WIN, self.color, self.rect, width=self.width)
        text = self.font.render(self.text, True, BLACK)
        self.environment.WIN.blit(text, (self.pos[0] + 10, self.pos[1] + 5))

    def checkClick(self):
        pass