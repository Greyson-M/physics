#totally inelastic collision
import math
import pygame
import os
import time
import matplotlib.pyplot as plt

pygame.init()

pi = math.pi

A_DIST = 50.25
B_DIST = 201
ma = 5
va = 2          #7.03125
mb = 3
vb = 0           #28.125
g = -9.8

pa = ma * va
pb = mb * vb



pfsq = (pa**2) + (pb**2)
pf = math.sqrt(pfsq)


vel  = pf/(ma+mb)

paf = ma * vel
pbf = mb * vel
print ([paf, pbf])

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


FPS = 30

BALL_B_IMAGE = pygame.image.load('ball1.png')
BALL_A_IMAGE = pygame.image.load('ball2.png')

print ("finals")
print ("v = " + str(vel))
print ("Pf = " + str(pf))

def d2r (d):
    r = d * (pi/180)
    return r


def getImpulse ():
    Jya = pf - pa
    Jxb = pf - pb


    return [Jya, Jxb]


#print (getImpulse())

sysfont = pygame.font.get_default_font()
#print('system font :', sysfont)
t0 = time.time()
font = pygame.font.SysFont(None, 18)
#
print('time needed for Font creation :', time.time()-t0)

B_OFFSET = A_DIST
A_OFFSET = B_DIST

def ball ():
    velx = 0
    vely = 0


def draw_window(xa, xb, ya, yb, tdisp, posAdisp, posBdisp, mousPos):
    WIN.blit(BALL_A_IMAGE, (xa, ya))
    #WIN.blit(BALL_B_IMAGE, (xb, yb))

#text
    WIN.blit(tdisp, (20, 20))
    WIN.blit(posAdisp, (20, 40))
    WIN.blit(posBdisp, (20, 60))
    WIN.blit(mousPos, (0, 0))

    pygame.display.update()
    WIN.fill(BLACK)

def main():
    paused = False
    clock = pygame.time.Clock()
    t = 0
    t2 = 0
    dt = (1/FPS)
    r = 0
    xpc = 0
    ypc = 0
    x = 15
    y = 10

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
#check for quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

#keypresses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print ("space")
                    paused = True

            while paused == True:

                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        print ("C")
                        paused = False


        t += dt

        if t > 100:
            break


        floor = 436

        vely = 0
        velx = 0

        accelperframe = g/60

        if y < floor:
            vely = vely - (g/1)

        elif y >= floor:
            vely =0

        x = x + (velx/1)
        y = y + (vely/1)


        xa = x
        ya = y

        xb = 0
        yb = 0




        tdisp = font.render("t: " + str(t), True, WHITE)
        posAdisp = font.render("A coords: ({}, {})".format(xa, ya), True, WHITE)
        posBdisp = font.render("B coords: ({}, {})".format(xb, yb), True, WHITE)

        Pos = pygame.mouse.get_pos()
        mousPos = font.render(str(Pos), True, WHITE)

        draw_window(xa, xb, ya, yb, tdisp, posAdisp, posBdisp, mousPos)



if __name__ == "__main__":
    main()
