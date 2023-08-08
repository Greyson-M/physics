from environment import Environment
from settings import *
from Vector import Vector
from mass import Mass


import pygame

env = Environment()

def test():
    pivleft = env.addPivot(Vector(400, 300))
    pivright = env.addPivot(Vector(800, 300))
    bot1 = env.addMass(Mass(env, 3, 3, Vector(500, 300), BLACK))
    bot2 = env.addMass(Mass(env, 3, 3, Vector(600, 300), BLACK))
    bot3 = env.addMass(Mass(env, 3, 3, Vector(700, 300), BLACK))
    botconst1 = env.addConstraint(bot1, pivleft)
    botconst2 = env.addConstraint(bot2, bot1)
    botconst3 = env.addConstraint(bot3, bot2)
    botconst4 = env.addConstraint(bot3, pivright)

    top1 = env.addMass(Mass(env, 3, 3, Vector(500, 200), BLACK))
    top2 = env.addMass(Mass(env, 3, 3, Vector(600, 200), BLACK))
    top3 = env.addMass(Mass(env, 3, 3, Vector(700, 200), BLACK))
    topconst1 = env.addConstraint(top1, pivleft)
    topconst2 = env.addConstraint(top1, bot1)
    topconst3 = env.addConstraint(top1, bot2)
    topconst4 = env.addConstraint(top1, top2)
    topconst5 = env.addConstraint(top2, bot2)
    topconst6 = env.addConstraint(top2, top3)
    topconst7 = env.addConstraint(top3, bot2)
    topconst8 = env.addConstraint(top3, pivright)
    topconst9 = env.addConstraint(top3, bot3)

    ball_mass = 100

    pend1 = env.addMass(Mass(env, ball_mass, 50, Vector(400, 600), BLACK))
    pend2 = env.addMass(Mass(env, ball_mass, 50, Vector(500, 600), BLACK))
    pend3 = env.addMass(Mass(env, ball_mass, 50, Vector(600, 600), BLACK))
    pend4 = env.addMass(Mass(env, ball_mass, 50, Vector(700, 600), BLACK))
    pend5 = env.addMass(Mass(env, ball_mass, 50, Vector(800, 600), BLACK))
    
    pendconst1 = env.addConstraint(pend1, pivleft)
    pendconst2 = env.addConstraint(pend2, bot1)
    pendconst3 = env.addConstraint(pend3, bot2)
    pendconst4 = env.addConstraint(pend4, bot3)
    pendconst5 = env.addConstraint(pend5, pivright)

    mass = env.addMass(Mass(env, 10, 10, Vector(500, 500), BLACK))

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