import pygame
from settings import *

class Slider:
    def __init__(self, env, pos, size, initial_val, min, max) -> None:
        self.environment = env

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
        pygame.draw.rect(self.environment.WIN, BLACK, self.container_rect, width=3)
        pygame.draw.rect(self.environment.WIN, BLACK, self.button_rect, width=3)
        self.moveSlider()

    def moveSlider(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.container_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.button_rect.centerx = mouse_pos[0]

                self.action(self.getVal())

                if self.button_rect.x < self.left_pos:
                    self.button_rect.centerx = self.left_pos
                elif self.button_rect.x > self.right_pos:
                    self.button_rect.centerx = self.right_pos

    def getVal(self):
        val_range = self.left_pos - self.right_pos
        button_val = self.button_rect.centerx - self.left_pos

        return -(button_val / val_range) * (self.max - self.min) + self.min
    
    def action(self, val):
        pass