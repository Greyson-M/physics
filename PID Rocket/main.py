from matplotlib import pyplot as plt
import pygame
import numpy as np

from Environment import Environment
from Utils import *
from Rocket import Rocket
from TestOrb import TestOrb
from Settings import *
from Rocket2 import Rocket2


env = Environment()

def main():
    #env.addMass(Rocket(env, 50, 50))
    env.addMass(Rocket2(env, 50, 50))

    run = True
    while run:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False
        


        env.update()

        

if __name__ == "__main__":

    main()

    plt.plot(env.pdata_ang[2:-1], label = "Propotional Error", color = "red")
    plt.plot(env.idata_ang[2:-1], label = "Integral", color = "orange")
    plt.plot(env.ddata_ang[2:-1], label = "Derivative", color = "green")
    plt.plot(env.correctiondata_ang[2:-1], label = "correction", color="blue")
    plt.title("PID - Angle")
    plt.legend()
    plt.show()

    plt.plot(env.pdata_pos[2:-1], label = "Propotional Error", color = "red")
    plt.plot(env.idata_pos[2:-1], label = "Integral", color = "orange")
    plt.plot(env.ddata_pos[2:-1], label = "Derivative", color = "green")
    plt.plot(env.correctiondata_pos[2:-1], label = "correction", color="blue")
    plt.title("PID - Position")
    plt.legend()
    plt.show()


