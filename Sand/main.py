import pygame
from Environment import Environment
import numpy as np


def main():
    E = Environment()
    run = True
 
    while run:
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = np.array([int(mouse_pos[0]), int(mouse_pos[1])])

            if mouse_pos[0] < E.WIDTH and mouse_pos[1] < E.HEIGHT:
                E.grid.add_sand(*mouse_pos)

        E.update()

    pygame.quit()

if __name__ == "__main__":
    main()