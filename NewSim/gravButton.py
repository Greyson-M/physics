import numpy as np
import pygame
from button import Button
from environment import Environment
from settings import *
from Utils import *


class GravButton(Button):
    def __init__(self, env, text, rect) -> None:
        super().__init__(env, text, rect)

        self.gravSwitch = False

        self.clicked = False
        self.timeClicked = 0

    def checkClick(self):
        if self.environment.t - self.timeClicked > self.cooldown:
            self.clicked = False

        mouse_pos = np.array(pygame.mouse.get_pos())
        self.color = self.defaultColor
        self.width = 3

        if self.rect.collidepoint(mouse_pos):
            self.color = self.hoverColor
            self.width = 0
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.timeClicked = self.environment.t
                print("GRAV BUTTON CLICKED")
                
                self.gravSwitch = not self.gravSwitch
                if self.gravSwitch:
                    self.environment.g = 0
                else:
                    self.environment.g = 9.81