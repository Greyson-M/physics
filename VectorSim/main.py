import pygame
import numpy as np

from Environment import Environment
from VectorArrow import VectorArrow
from mass import Mass
from utils import *

env = Environment()

#env.add_vector(VectorArrow(env, np.array([env.WIDTH//2, env.HEIGHT//2])))
#env.add_mass(Mass(env, 1000000, 10, np.array([env.WIDTH//2, env.HEIGHT//2]), (0, 0, 0)))
#env.add_mass(Mass(env, 4000000, 10, np.array([env.WIDTH//2 + 100, env.HEIGHT//2]), (0, 0, 0)))

def main():
    run = True
    while run:
        env.update()
        

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pos = np.array([mouse_pos[0], mouse_pos[1]])
                for mass in env.mass_list:
                    if dist(mass.pos, mouse_pos) < mass.radius:
                        mass.held = True
                        env.heldMass = mass

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if env.heldMass != None:
                    env.heldMass.held = False
                    env.heldMass = None

            if event.type == pygame.QUIT:
                run = False

if __name__ == "__main__":
    main()