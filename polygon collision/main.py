from environment import Environment
from gon import Gon
import pygame
import numpy as np

env = Environment()
def main():
    while env.running:
        env.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                env.running = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    env.running = False
                    pygame.quit()
                    quit()
                if event.key == pygame.K_LEFT:
                    for p in env.gons[0].points:
                        p[0] += -5
                if event.key == pygame.K_RIGHT:
                    for p in env.gons[0].points:
                        p[0] += 5
                if event.key == pygame.K_UP:
                    for p in env.gons[0].points:
                        p[1] += -5
                if event.key == pygame.K_DOWN:
                    for p in env.gons[0].points:
                        p[1] += 5

            if event.type == pygame.MOUSEBUTTONDOWN:
                env.click = True
            if event.type == pygame.MOUSEBUTTONUP:
                env.click = False

if __name__ == "__main__":
    main()