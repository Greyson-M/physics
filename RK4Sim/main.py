from environment import Environment
from settings import *
from Vector import Vector
from mass import Mass


import pygame

env = Environment()

def test():
    piv = env.addPivot(Vector(400, 300))
    m1 = env.addMass(Mass(env, 1, 10, Vector(400, 400), RED))
    m2 = env.addMass(Mass(env, 1, 10, Vector(400, 500), BLUE))
    #const = env.addConstraint(m1, m2)
    const2 = env.addConstraint(m1, piv)
    #spring = env.addSpring(piv, m1, 0.8)

test()

def main():
    run = True
    while run:
        env.update()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for mass in env.massList:
                    if mass.pos.distance(pygame.mouse.get_pos()) < mass.radius:
                        mass.held = True
                        env.heldMass = mass

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if env.heldMass != None:
                    env.heldMass.held = False
                    env.heldMass = None

if __name__ == "__main__":
    main()