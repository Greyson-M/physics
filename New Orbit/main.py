from environment import Environment
from settings import *

import pygame
import numpy as np

env = Environment()

def test():
    #sun = env.addMass(50, 33304, np.array([WIDTH/2, HEIGHT/2]), color=((255, 207, 48)), name="Sun")
    earth = env.addMass(5, 1, np.array([WIDTH/2, HEIGHT/2 - 100]), vel=np.array([100, 0]), accel=np.array([30 , 0]), color=((0, 0, 255)), name="Earth")

test()

def main():
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                env.addMass(5, 100, np.array(pos))
        
        env.update()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()