from matplotlib import pyplot as plt
import pygame
import threading

from Environment import Environment
from Mass import Mass
from Constraint import Constraint
from Thruster import Thruster
from ControlTruster import ControlThruster
from Settings import *
import numpy as np
from Utils import *
from System import System
from Rocket import Rocket

from TestOrb import TestOrb

env = Environment()

def test_rocket():
    env.addMass(Mass(env, 1, 13, np.array((600, 100)), np.array((0, 0)), (255, 0, 0), name="Control"))
    env.addMass(Mass(env, 10, 13, np.array((600, 200)), np.array((0, 0)), (0, 255, 0), name="Base"))
    env.addConstraint(Constraint(env.massList[0], env.massList[1], 100))
    env.addSystem(System(env, env.massList, env.constraintList))
    env.addThruster(Thruster(env.systemList[0], 17))
    env.addThruster(ControlThruster(env.systemList[0], 7))

    



def main():

    #env.addMass(TestOrb(env))
    #test_rocket()
    env.addMass(Rocket(env, 50, 50))

    run = True
    while run:
        mouse_pos = pygame.mouse.get_pos()
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


