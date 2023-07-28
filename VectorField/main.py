import pygame
from settings import *
import math
from Field import Field
from Environment import Environment
import numpy as np
from Mass import Mass
from random import randint

env = Environment()

for i in range(100):
    pos = np.array([randint(0, WIDTH), randint(0, HEIGHT)])
    env.massList.append(Mass(env, pos))

def main():
    clock = pygame.time.Clock()
    running = True
    t = 1/FPS
    prevt = 0

    pygame.display.flip()

    while running:
        clock.tick(FPS)
        
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        mouse_pos = np.array((Mouse_x, Mouse_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                env.massList.append(Mass(env, mouse_pos))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_g:
                    DRAW_GRID = not DRAW_GRID
                if event.key == pygame.K_r:
                    env.clear()

        env.update()


        pygame.display.flip()

        t += (1/FPS)
        env.t = t

if __name__ == "__main__":
    main()