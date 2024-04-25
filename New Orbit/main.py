from environment import Environment
from settings import *

import pygame
import numpy as np

env = Environment()

def test():
    p1 = 0.306893
    p2 = 0.125507

    #sun = env.addMass(50, 33304, np.array([WIDTH/2, HEIGHT/2]), color=((255, 207, 48)), name="Sun")
    #earth = env.addMass(5, 1, np.array([WIDTH/2, HEIGHT/2 - 100]), vel=np.array([100, 0]), accel=np.array([30 , 0]), color=((0, 0, 255)), name="Earth")'
    m1 = env.addMass(5, 100000, np.array([400, 300]), vel=np.array([0, 0]))
    m2 = env.addMass(5, 100000, np.array([600, 450]), vel=np.array([0, 0]))
    m3 = env.addMass(5, 100000, np.array([500, 300]), vel=np.array([0, 0]))

def figure_eight():
    # Define the masses
    m1 = m2 = m3 = 100000

    # Define the initial positions
    pos1 = np.array([-0.97000436, 0.24308753])
    pos2 = np.array([-pos1[0], -pos1[1]])
    pos3 = np.array([0.0, 0.0])

    # Define the initial velocities
    vel1 = np.array([0.466203685, 0.43236573])
    vel2 = np.array([vel1[0], vel1[1]])
    vel3 = np.array([-2*vel1[0], -2*vel1[1]])

    # Add the masses to the environment
    m1 = env.addMass(5, m1, pos1*100 + np.array([WIDTH/2, HEIGHT/2]), vel=vel1*10)
    m2 = env.addMass(5, m2, pos2*100 + np.array([WIDTH/2, HEIGHT/2]), vel=vel2*10)
    m3 = env.addMass(5, m3, pos3*100 + np.array([WIDTH/2, HEIGHT/2]), vel=vel3*10)

figure_eight()

def main():
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            '''
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                env.addMass(5, 100, np.array(pos))
            '''
        
        env.update()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()