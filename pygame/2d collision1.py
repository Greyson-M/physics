#totally inelastic collision
import math
import pygame
import os
import time
import matplotlib.pyplot as plt

open('x_data.txt', 'w').close()
open('t_data.txt', 'w').close()
open('y_data.txt', 'w').close()
open('data.txt', 'w').close()

pygame.init()

pi = math.pi

A_DIST = 50.25
B_DIST = 201
ma = 5
va = 15           #7.03125
mb = 3
vb = 60           #28.125

pa = ma * va
pb = mb * vb



pfsq = (pa**2) + (pb**2)
pf = math.sqrt(pfsq)

theta = math.degrees(math.atan(pb/pa))
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
print ("theta = " + str(theta))
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

def draw_window(xa, xb, ya, yb, tdisp, posAdisp, posBdisp, mousPos):
    WIN.blit(BALL_A_IMAGE, (xa, ya))
    WIN.blit(BALL_B_IMAGE, (xb, yb))

#text
    WIN.blit(tdisp, (20, 20))
    WIN.blit(posAdisp, (20, 40))
    WIN.blit(posBdisp, (20, 60))
    WIN.blit(mousPos, (0, 0))

    pygame.display.update()
    WIN.fill(BLACK)

x_data = []
y_data = []
t_data = []

def graphx():
    plt.plot(t_data, x_data)
    plt.ylabel("X distance")
    plt.xlabel("Time")
    plt.show()

def graphy():
    plt.plot(t_data, y_data)
    plt.ylabel("y distance")
    plt.xlabel("Time")
    plt.show()

def main():
    paused = False
    clock = pygame.time.Clock()
    t = 0
    t2 = 0
    i = (1/FPS)
    r = 0

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


        t += i

        if t > 11:
            break

        if t >= (B_DIST/vb):
            t2+=i

            vely = vel * math.sin(d2r(theta))
            velx = vel * math.cos(d2r(theta))

            x = abs(velx * t2) + xpc
            y = abs(vely * t2) + ypc

            xa, ya = x, y
            xb, yb = xa, ya

            xjump = xpc - x
            yjump = ypc - y

            '''if r == 0:
                print ("time: " + str(t))
                print ("x jump: " + str(xjump))
                print("y jump: " + str(yjump))
                r = 1

            #time.sleep(5)
            '''

        else:

            x = va * t
            xa = (x) + 0

            y = vb * t
            yb = (y) + 0

            ya = A_OFFSET
            xb = B_OFFSET

            xpc = xa
            ypc = ya

        tdisp = font.render("t: " + str(t), True, WHITE)
        posAdisp = font.render("A coords: ({}, {})".format(xa, ya), True, WHITE)
        posBdisp = font.render("B coords: ({}, {})".format(xb, yb), True, WHITE)

        Pos = pygame.mouse.get_pos()
        mousPos = font.render(str(Pos), True, WHITE)

        x_data.append(round(xa, 2))
        y_data.append(round(yb, 2))
        t_data.append(round(t, 2))

        draw_window(xa, xb, ya, yb, tdisp, posAdisp, posBdisp, mousPos)

    graphx()
    graphy()

    filex = open("x_data.txt", "a")
    filet = open("t_data.txt", "a")
    filey = open("y_data.txt", "a")
    for x in x_data:
        filex.write(str(x) + "\n")
    for t in t_data:
        filet.write(str(t) + "\n")
    for t in y_data:
        filey.write(str(y) + "\n")

    file1 = open("data.txt", "a")

    for i in range(len(t_data)):
        file1.write(str(x_data[i]) + "\t\t\t\t" + str(t_data[i]) + "\t\t\t\t" + str(y_data[i]) + "\n\n")


if __name__ == "__main__":
    main()
