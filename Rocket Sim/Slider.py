import pygame
import numpy as np
from Settings import *

class Slider:
    def __init__(self, env, pos, size, initial_val, min, max, label, prec) -> None:
        self.env = env

        self.label = label
        self.precision = prec

        self.pos = pos
        self.size = size

        self.left_pos = self.pos[0] - self.size[0] // 2
        self.right_pos = self.pos[0] + self.size[0] // 2
        self.top_pos = self.pos[1] - self.size[1] // 2

        self.initial_val = (self.right_pos - self.left_pos) * initial_val
        self.min = min
        self.max = max

        self.container_rect = pygame.Rect(self.left_pos, self.top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.left_pos + self.initial_val-6, self.top_pos, 10, self.size[1])

    def draw(self):
        pygame.draw.rect(self.env.WIN, BLACK, self.container_rect, width=3)
        pygame.draw.rect(self.env.WIN, BLACK, self.button_rect, width=3)

        labelText = self.env.font_small.render(self.label, True, BLACK)
        self.env.WIN.blit(labelText, (self.left_pos - labelText.get_width() - 10, self.top_pos + self.size[1]/2 - labelText.get_height()/2))

        text = self.env.font_small.render("{}".format(round(self.getVal(), self.precision)), True, BLACK)
        self.env.WIN.blit(text, (self.right_pos + 10, self.top_pos + self.size[1]/2 - text.get_height()/2))

        self.moveSlider()

    def moveSlider(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.container_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.button_rect.centerx = mouse_pos[0]


                if self.button_rect.x < self.left_pos:
                    self.button_rect.centerx = self.left_pos
                elif self.button_rect.x > self.right_pos:
                    self.button_rect.centerx = self.right_pos

    def getVal(self):
        val_range = self.left_pos - self.right_pos
        button_val = self.button_rect.centerx - self.left_pos

        return -(button_val / val_range) * (self.max - self.min) + self.min