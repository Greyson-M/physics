import math
import pygame
from breakButton import BreakButton
from gravButton import GravButton
from button import Button
from settings import *
from environment import Environment
from puck import Puck
from block import Block
from spinner import Spinner
from cylinder import Cylinder
from generator import Generator
from tube import Tube
import numpy as np
from pivot import Pivot
from pytmx.util_pygame import load_pygame
from gravSlider import GravSlider
from stiffSlider import StiffSlider
import random
from constraint import Constraint




environment = Environment()

m1 = Puck(environment)

def pyramid():
    for i in range(1, 2):
        for j in range(-i, i):
            environment.blockList.append(Block(environment, 20, np.array(( 350 + j*25, 75 + i*25)), 50, 25, color=BLACK, vel=np.array((0, -10)), name=i+j))

#pyramid()

def square(k=0):
    puck0 = environment.addPuck(Puck(environment, 10, np.array(( 350, 75)), radius=10, color=((255, 0, 0)), name='red'))
    puck1 = environment.addPuck(Puck(environment, 10, np.array(( 350, 110)), radius=10, color=((0, 255, 0)), name='green'))
    puck2 = environment.addPuck(Puck(environment, 10, np.array(( 385, 75)), radius=10, color=((0, 0, 255)), name='blue'))
    puck3 = environment.addPuck(Puck(environment, 10, np.array(( 385, 110)), radius=10, color=((255, 255, 0)), name='yellow'))

    environment.addSpring(puck0, puck1, None, k)
    environment.addSpring(puck0, puck2, None, k)
    environment.addSpring(puck1, puck3, None, k)
    environment.addSpring(puck2, puck3, None, k)
    environment.addSpring(puck0, puck3, None, k)
    environment.addSpring(puck1, puck2, None, k)

def triangle():
    puck1 = environment.addPuck(Puck(environment, 1 , np.array(( 400, 130)), radius=10, color=((255, 0, 0)), name='red'))
    puck2 = environment.addPuck(Puck(environment, 1, np.array(( 350, 130)), radius=10, color=((0, 255, 0)), name='green'))
    puck3 = environment.addPuck(Puck(environment, 1, np.array(( 375, 75)), radius=10, color=((0, 0, 255)), name='blue'))

    environment.addSpring(puck1, puck2, None, 0.8)
    environment.addSpring(puck1, puck3, None, 0.8)
    environment.addSpring(puck2, puck3, None, 0.8)

def pendulum(stiff):
    pivot = environment.addPivot(Pivot(environment, np.array(( 800, 200))))
    puck1 = environment.addPuck(Puck(environment, 1, np.array(( 800, 250)), radius=10, color=((255, 0, 0)), name='red'))
    puck2 = environment.addPuck(Puck(environment, 2, np.array(( 800, 300)), radius=10, color=((0, 255, 0)), name='green'))
    puck3 = environment.addPuck(Puck(environment, 10, np.array(( 800, 350)), radius=10, color=((0, 0, 255)), name='blue'))

    environment.addSpring(pivot, puck1, None, stiff)
    environment.addSpring(puck1, puck2, None, stiff)
    environment.addSpring(puck2, puck3, None, stiff)

def bridge(stiff):
    Pivot1 = environment.addPivot(Pivot(environment, np.array(( 200, 200))))
    Pivot2 = environment.addPivot(Pivot(environment, np.array(( 950, 200))))

    Pivot3 = environment.addPivot(Pivot(environment, np.array(( 200, 275))))
    Pivot4 = environment.addPivot(Pivot(environment, np.array(( 950, 275))))

    puck1 = environment.addPuck(Puck(environment, 1, np.array(( 350, 200)), radius=10, color=((255, 0, 0)), name='red'))
    puck2 = environment.addPuck(Puck(environment, 1, np.array(( 500, 200)), radius=10, color=((0, 255, 0)), name='green'))
    puck3 = environment.addPuck(Puck(environment, 1, np.array(( 650, 200)), radius=10, color=((0, 0, 255)), name='blue'))
    puck4 = environment.addPuck(Puck(environment, 1, np.array(( 800, 200)), radius=10, color=((255, 255, 0)), name='yellow'))

    puck5 = environment.addPuck(Puck(environment, 1, np.array(( 275, 275)), radius=10, color=((255, 0, 0)), name='red'))
    puck6 = environment.addPuck(Puck(environment, 1, np.array(( 425, 275)), radius=10, color=((0, 255, 0)), name='green'))
    puck7 = environment.addPuck(Puck(environment, 1, np.array(( 575, 275)), radius=10, color=((0, 0, 255)), name='blue'))
    puck8 = environment.addPuck(Puck(environment, 1, np.array(( 725, 275)), radius=10, color=((255, 255, 0)), name='yellow'))
    puck9 = environment.addPuck(Puck(environment, 1, np.array(( 875, 275)), radius=10, color=((255, 255, 0)), name='yellow'))

    tightness = 1

    short = 75/tightness
    shortmed = 100/tightness
    med = 150/tightness
    lon = 235/tightness

    short, shortmed, med, lon = None, None, None, None

    environment.addSpring(Pivot1, puck1, med, stiff, name='1')
    environment.addSpring(puck1, puck2, med, stiff, name='2')
    environment.addSpring(puck2, puck3, med, stiff, name='3')
    environment.addSpring(puck3, puck4, med, stiff, name='4')
    environment.addSpring(puck4, Pivot2, med, stiff, name='5')

    environment.addSpring(Pivot3, puck5, short, stiff, name='6')
    environment.addSpring(puck5, puck6, med, stiff, name='7')
    environment.addSpring(puck6, puck7, med, stiff, name='8')
    environment.addSpring(puck7, puck8, med, stiff, name='9')
    environment.addSpring(puck8, puck9, med, stiff, name='10')
    environment.addSpring(puck9, Pivot4, short, stiff, name='11')

    environment.addSpring(Pivot3, puck1, med, stiff, name='12')
    environment.addSpring(Pivot1, puck5, shortmed, stiff, name='13')
    environment.addSpring(puck1, puck5, shortmed, stiff, name='14')
    environment.addSpring(puck1, puck6, shortmed, stiff, name='15')
    environment.addSpring(puck2, puck5, lon, stiff, name='16')
    environment.addSpring(puck2, puck6, shortmed, stiff, name='17')
    environment.addSpring(puck2, puck7, shortmed, stiff, name='18')
    environment.addSpring(puck3, puck6, lon, stiff, name='19')
    environment.addSpring(puck3, puck7, shortmed, stiff, name='20')
    environment.addSpring(puck3, puck8, shortmed, stiff, name='21')
    environment.addSpring(puck4, puck7, lon, stiff, name='22')
    environment.addSpring(puck4, puck8, shortmed, stiff, name='23')
    environment.addSpring(puck4, puck9, shortmed, stiff, name='24')
    environment.addSpring(Pivot4, puck4, med, stiff, name='25')
    environment.addSpring(Pivot2, puck9, shortmed, stiff, name='26')

def loadMap(map):
        pucks = []
        pivots = []
        springs = []

        for obj in map.objects:
            if obj.type == "puck":
                environment.addPuck(Puck(environment, 1, np.array((obj.x, obj.y)), radius=10, name=obj.name))

            if obj.type == "pivot":
                environment.addPivot(Pivot(environment, np.array((obj.x, obj.y)), name=obj.name))

            if obj.type == "block":
                print ("block added")
                #environment.addBlock(Block(environment, 25, np.array((obj.x, obj.y)), obj.width, obj.height, name=obj.name))
                environment.blockList.append(Block(environment, 25, np.array((obj.x, obj.y)), obj.width, obj.height, name=obj.name))

            if obj.type == "spring":
                p1 = obj.properties["p1"] - 1
                p2 = obj.properties["p2"] - 1
                length = obj.properties["length"]
                k = obj.properties["k"]

                print (p1, p2, length, k)

                if length < 1:
                    length = None

                if obj.properties['pivot']:
                    environment.addSpring(environment.puckList[p1], environment.pivotList[p2], length, k, name=obj.name)

                elif obj.properties['block']:
                    print (environment.blockList, p2)
                    environment.addSpring(environment.puckList[p1], environment.blockList[p2], length, k, name=obj.name, block=True, offset = obj.properties['offset'])
                else:
                    environment.addSpring(environment.puckList[p1], environment.puckList[p2], length, k, name=obj.name)

def cloth(num, m, stiff, step):
    nodes = []

    for i in range(num):
        nodes.append([])
        for j in range(num):
            nodes[i].append(environment.addPuck(Puck(environment, m, np.array(( 300 + j*step, 150 + i*step)), radius=60/num, color=((0, 0, 0)), name='red')))

    for i in range(num):
        p = environment.addPivot(Pivot(environment, np.array(( 300 + i*step, 100)), name='red'))
        environment.addSpring(environment.puckList[i], p, None, stiff, name='1')

    for i in range(num):
        for j in range(1, num):
            environment.addSpring(nodes[i][j-1], nodes[i][j], step, stiff, name='1')

    for i in range(num):
        for j in range(1, num):
            environment.addSpring(nodes[j-1][i], nodes[j][i], step, stiff, name='1')

def addParticles(n, size, mass):
    for i in range(n):
        randpos = np.array((random.randint(leftwall, rightwall), random.randint(topwall, bottomwall)))
        environment.addPuck(Puck(environment, mass, randpos, radius=size, color=((0, 0, 0)), name='red'))

def constraintTest():
    pivot1 = environment.addPivot(Pivot(environment, np.array(( 800, 550))))
    pivot2 = environment.addPivot(Pivot(environment, np.array(( 700, bottomwall))))
    p1 = environment.addPuck(Puck(environment, 10, np.array(( 700, 555)), radius=10, color=((0, 0, 0)), name='red'))
    #p2 = environment.addPuck(Puck(environment, 20, np.array(( 700, 550)), radius=10, color=((0, 0, 0)), name='red'))
    #environment.addConstraint(Constraint(p1, p2, 283))
    environment.addConstraint(Constraint(p1, pivot1, 283))
    environment.addSpring(p1, pivot2, None, 0.5, name='1')


    #p3 = environment.addPuck(Puck(environment, 10, np.array(( 700, 500)), radius=10, color=((0, 0, 0)), name='red'))
    #piv3 = environment.addPivot(Pivot(environment, np.array(( 743, 575))))
    #p4 = environment.addPuck(Puck(environment, 10, np.array(( 743, 525)), radius=10, color=((0, 0, 0)), name='red'))
    #p5 = environment.addPuck(Puck(environment, 10, np.array(( 693, 525)), radius=10, color=((0, 0, 0)), name='red'))

    #environment.addConstraint(Constraint(piv3, p4, 50))
    #environment.addConstraint(Constraint(p4, p5, 50))
    #environment.addConstraint(Constraint(p5, piv3, 50))

def spinnerTest():
    
    p1 = environment.addPuck(Puck(environment, 5, np.array(( 740, 515)), radius=3, color=((0, 0, 0)), name='red'))
    p2 = environment.addPuck(Puck(environment, 10, np.array(( 640, 515)), radius=15, color=((0, 0, 0))))
    p3 = environment.addPuck(Puck(environment, 20, np.array(( 880, 500)), radius=15, color=((0, 0, 0))))
    #cylinder = environment.addCylinder(Cylinder(environment, pygame.Rect(550, 500, 100, 30), "right", p2))
    tube = environment.addTube(Tube(pygame.Rect(500, 500, 150, 30), p3, p2))
    spin = environment.addSpinner(Spinner(20, 4, p1))
    #piv = environment.addPivot(Pivot(environment, np.array(( 600, bottomwall))))
    #spring = environment.addSpring(p1, piv, None, 0.5, name='1')
    constraint = environment.addConstraint(Constraint(p1, p2, 40))
    #const2 = environment.addConstraint(Constraint(p2, p3, 40))


def cylinderTest():
    #pSpin = environment.addPuck(Puck(environment, 1, np.array(( 800, 517)), radius=4, color=((0, 0, 0)), name='red'))
    #spin = environment.addSpinner(Spinner(40, 1, pSpin))
    #piv = environment.addPivot(Pivot(environment, np.array(( 760, 517))))
    #const2 = environment.addConstraint(Constraint(pSpin, piv, 40))

    gen = environment.addGenerator(Generator(environment, np.array((760, 517)), 35, 20))
    
    #piv = environment.addPivot(Pivot(environment, np.array(( 670, 517))))
    p2 = environment.addPuck(Puck(environment, 10, np.array(( 670, 513)), radius=15, color=((75, 175, 200)), name='red'))
    cylinder = environment.addCylinder(Cylinder(environment, pygame.Rect(570, 500, 115, 30), "right", p2))

    const = environment.addConstraint(Constraint(p2, gen.puck, 40))
    #spring = environment.addSpring(p2, gen.puck, None, 0.5, name='1')

def newConstriantTest():
    piv = environment.addPivot(Pivot(environment, np.array(( 640, bottomwall))))
    piv1 = environment.addPivot(Pivot(environment, np.array(( 700, bottomwall))))
    piv2 = environment.addPivot(Pivot(environment, np.array(( 580, bottomwall))))
    p1 = environment.addPuck(Puck(environment, 10, np.array(( 640, 550)), radius=10, color=((0, 0, 0)), name='red'))
    const = environment.addConstraint(Constraint(p1, piv, 50))
    spring1 = environment.addSpring(p1, piv1, None, 0.5, name='1')
    spring2 = environment.addSpring(p1, piv2, None, 0.5, name='2')

def structure():
    pivleft = environment.addPivot(Pivot(environment, np.array(( 300, 600))))
    pivright = environment.addPivot(Pivot(environment, np.array(( 900, 600))))
    bot1 = environment.addPuck(Puck(environment, 10, np.array(( 450, 600)), radius=3, color=((0, 0, 0)), name='red'))
    bot2 = environment.addPuck(Puck(environment, 10, np.array(( 600, 600)), radius=3, color=((0, 0, 0)), name='red'))
    bot3 = environment.addPuck(Puck(environment, 10, np.array(( 750, 600)), radius=3, color=((0, 0, 0)), name='red'))
    botconst1 = environment.addConstraint(Constraint(bot1, pivleft, 150))
    botconst2 = environment.addConstraint(Constraint(bot2, bot1, 150))
    botconst3 = environment.addConstraint(Constraint(bot3, bot2, 150))
    botconst4 = environment.addConstraint(Constraint(bot3, pivright, 150))

    mid1 = environment.addPuck(Puck(environment, 10, np.array(( 450, 450)), radius=3, color=((0, 0, 0)), name='red'))
    mid2 = environment.addPuck(Puck(environment, 10, np.array(( 750, 450)), radius=3, color=((0, 0, 0)), name='red'))
    midconst1 = environment.addConstraint(Constraint(mid1, pivleft, 150))
    midconst2 = environment.addConstraint(Constraint(mid1, bot1, 150))
    midconst3 = environment.addConstraint(Constraint(mid1, bot2, 150))
    midconst4 = environment.addConstraint(Constraint(mid2, pivright, 150))
    midconst5 = environment.addConstraint(Constraint(mid2, bot2, 150))
    midconst6 = environment.addConstraint(Constraint(mid2, bot3, 150))

    top1 = environment.addPuck(Puck(environment, 10, np.array(( 600, 300)), radius=3, color=((0, 0, 0)), name='red'))
    topconst1 = environment.addConstraint(Constraint(top1, mid1, 150))
    topconst2 = environment.addConstraint(Constraint(top1, bot2, 150))
    topconst3 = environment.addConstraint(Constraint(top1, mid2, 150))


#cloth(10, 1, 0, 20)
#loadMap(environment.map)
#square()
#triangle()
#pendulum(1)
#bridge(0)

structure()

#piv = environment.addPivot(Pivot(environment, np.array(( 350, 250))))
#m1 = environment.addPuck(Puck(environment, 1, np.array(( 350, 75)), vel = np.array((5, 2)), radius=10, color=((255, 0, 0)), name='red'))
#m2 = environment.addPuck(Puck(environment, 1, np.array(( 350, 110)), radius=10, color=((0, 255, 0)), name='green'))
#const = environment.addConstraint(Constraint(m1, m2, 50))
#const2 = environment.addConstraint(Constraint(m2, piv, 50))

#NEWTON BALL SIM
#.....
#.....
#>>....

#constraintTest()
#spinnerTest()
#cylinderTest()
#newConstriantTest()
#cannonTest()

#loadMap(environment.map)

#environment.addPuck(Puck(environment, 10, np.array(( 100, 100)), radius=10, color=((0, 0, 0)), name='red'))
#environment.addPuck(Puck(environment, 20, np.array(( 600, 600)), radius=10, color=((0, 0, 0)), name='red'))
#environment.addPuck(Puck(environment, 100, np.array(( 800, 500)), radius=10, color=((255, 0, 0)), name='red'))

#addParticles(3, 4, 2)

#environment.blockList.append(Block(environment, 1, np.array(( 350, 75)), 50, 25, color=((200, 24, 75)), vel=np.array((0, -10)), name="top"))
#environment.blockList.append(Block(environment, 1, np.array(( 350, 110)), 50, 25, color=BLACK, vel=np.array((0, -5)), name="bottom"))

#environment.addButton(GravButton(environment, "grav", pygame.Rect(100, 680, 60, 20)))
#environment.sliderList.append(GravSlider(environment, (200, 690), (80, 20), 0, -20, 100))
environment.sliderList.append(StiffSlider(environment, (600, 690), (80, 20), 0.25, -0.5, 3))
environment.addButton(BreakButton(environment, "break", pygame.Rect(100, 680, 60, 20)))




for b in environment.blockList:
    environment.rectList.append(b.box)

def main():
    clock = pygame.time.Clock()
    running = True
    t = 1/FPS
    prevt = 0

    pygame.display.flip()

    while running:
        clock.tick(FPS)

        i=0
        for b in environment.blockList:
            environment.rectList[i] = b.box
            i+=1
        
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        mouse_pos = np.array((Mouse_x, Mouse_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for b in environment.blockList:
                    if b.box.collidepoint(Mouse_x, Mouse_y):
                        b.held = True
                        environment.heldBlock = b

                if len(environment.puckList) < 1:
                    environment.addPuck(Puck(environment, 20, mouse_pos, radius=10))
                    environment.heldPuck = None

                for p in environment.puckList:
                    if (mouse_pos[0] < (p.pos[0] + p.radius)) and (mouse_pos[0] > (p.pos[0] - p.radius)):
                        if (mouse_pos[1] < (p.pos[1] + p.radius)) and (mouse_pos[1] > (p.pos[1] - p.radius)):
                            p.held = True
                            environment.heldPuck = p

                if environment.heldPuck == None:
                    environment.addPuck(Puck(environment, 20, mouse_pos, radius=10))

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if environment.heldBlock != None:
                    environment.heldBlock.held = False
                    environment.heldBlock = None

                if environment.heldPuck != None:
                    environment.heldPuck.held = False
                    environment.heldPuck = None


        environment.update(clock)
        environment.grid.draw()

        for p in environment.puckList:
            p.draw(mouse_pos, t)
        
        for b in environment.blockList:
            b.draw(mouse_pos, t)


        for s in environment.springList:
            s.update()

        for p in environment.pivotList:
            p.draw()

        for b in environment.buttonList:
            b.draw()

        for s in environment.sliderList:
            s.draw()

        for c in environment.constraintList:
            c.update()
        for s in environment.spinnerList:
            s.update()
        for c in environment.cylinderList:
            c.draw()

        for g in environment.generatorList:
            g.draw(mouse_pos, t)

        for tube in environment.tubeList:
            tube.draw()


        pygame.display.flip()

        t += (1/FPS)
        environment.t = t



if __name__ == "__main__":
    main()
    pygame.quit()