from environment import Environment
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
                if event.key == pygame.K_LEFT:
                    env.system.move(np.array([-10, 0]))
                if event.key == pygame.K_RIGHT:
                    env.system.move(np.array([10, 0]))
                if event.key == pygame.K_UP:
                    env.system.move(np.array([0, -10]))
                if event.key == pygame.K_DOWN:
                    env.system.move(np.array([0, 10]))

if __name__ == "__main__":
    main()