from environment import Environment
import pygame
import numpy as np

env = Environment()

def main():
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        env.update()


    pygame.quit()

if __name__ == "__main__":
    main()