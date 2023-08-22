from Environment import Environment

import pygame
import numpy as np

env = Environment()


def test():
    env.addMass(env, 10, 1, np.array([env.WIDTH/2, env.HEIGHT/2]), env.RED)

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                env.addMass(env, 10, 1, np.array([pos[0], pos[1]]), env.BLACK)


        env.update()
        


if __name__ == "__main__":
    main()

