import sandbox
import pygame
import numpy as np
import time
from random import randint
import math

def E(x):
    return 10**x

#GAME constants
FPS = 60
WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
dt = (1/FPS)

topwall = 50
bottomwall = HEIGHT - 50
rightwall = WIDTH - 100
leftwall = 100

#physics constants
g = 9.80   #m/s^2
G = 5.2383524 * E(-18)
AIR_DENSITY = 1.225
DRAG_COEF = 1

pi = math.pi

#load
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN.fill((217, 217, 217))

sysfont = pygame.font.get_default_font()
t0 = time.time()
font = pygame.font.SysFont(None, 18)

#UTILIY FUNCTIONS
def pythag (vector):
    a = (vector[0]**2) + (vector[1]**2)
    return math.sqrt(a)

def distance (vec1, vec2):
    xdis = vec2[0] - vec1[0]
    ydis = vec2[1] - vec1[1]
    return pythag([xdis, ydis])

def gforce(p1,p2):
    # Calculate the gravitational force exerted on p1 by p2.
    # Calculate distance vector between p1 and p2.
    r_vec = p1.pos-p2.pos
    # Calculate magnitude of distance vector.
    r_mag = pythag(r_vec)
    if r_mag == 0:
        r_mag = 1
    # Calcualte unit vector of distance vector.
    r_hat = r_vec/r_mag
    # Calculate force magnitude.
    force_mag = G*p1.mass*p2.mass/r_mag**2
    # Calculate force vector.
    force_vec = -force_mag*r_hat
    return force_vec

def partition(arr, low, high):
    i = (low-1)         # index of smaller element
    pivot = arr[high]     # pivot

    for j in range(low, high):

        # If current element is smaller than or
        # equal to pivot
        if arr[j] <= pivot:

            # increment index of smaller element
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)
def quickSort(arr, low, high):
    if len(arr) == 1:
        return arr
    if low < high:

        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, low, high)

        # Separately sort elements before
        # partition and after partition
        quickSort(arr, low, pi-1)
        quickSort(arr, pi+1, high)

m1 = sandbox.mass1(pos = np.array((800,450)), radius=50, mass=(0.5), vel = np.array((0,0)))
m2 = sandbox.mass1(pos = np.array((175,150)), vel = np.array((0, 0)), color=((150,255,155)), radius=5, mass=(10))
anchor = sandbox.mass1(mass=0, vel=np.array((0,0)), accel=np.array((0,0)), radius=7, name="ANCHOR")

randPos = np.array((450, bottomwall-100))
bodies = [m1, m2, anchor]
springs = [sandbox.spring(pos=randPos)]
penulum = [sandbox.pendString(toppos = np.array([WIDTH/2, topwall]), length=HEIGHT/2   )]

j= 0
while j < 1:
    randPos = np.array((randint(110, 720), randint(55, 380)))
    randColor = (( randint(0, 255), randint(0, 255), randint(0, 255) ))
    #randRadius = randint(2, 50)
    randRadius = 50
    randVel = np.array((0,10))

    bodies.append( sandbox.mass1(radius=randRadius, name="m{}".format(j + 1), pos=randPos, mass=60, color=randColor, vel=randVel ) )

    j+=1


def main():
    clock = pygame.time.Clock()
    running = True
    t = 1/FPS
    n=bodies[1]
    prevt = 0
    LeftClick = False
    HeldMassObj = bodies[0]
    dist = 100
    heldMassName = 0


    pygame.display.flip()

    while running:
        clock.tick(FPS)
        prevt += (1/FPS)
        t += (1/FPS)

        Mouse_x, Mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
#check for quit
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

#pause --not complete
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print ("space")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    LeftClick = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    LeftClick = False
                    HeldMassObj.held = False
                    heldMassName = 0


        MousePos = np.array((Mouse_x, Mouse_y))

    #draw collision box
        pygame.draw.rect(WIN, BLACK, pygame.Rect(leftwall, topwall, rightwall-100, bottomwall-50),  5)

    #collision detection with ball
        for m in bodies:
            for n in bodies:

                if n == m:
                    pass
                else:

                    dist = distance(m.pos, n.pos)

                    if dist <= (m.radius + n.radius):
                        m.interCollide(dist, n, springs[0])

#MASS
        for m in bodies:
            #collision detection for box border
            m.linInterp()

            if m.name != "ANCHOR":
                m.pos = m.pos + (m.vel * dt * 2.5)      #update pos
                m.vel = m.vel + (m.accel * dt * 2.5)       #update vel

            #m.interGrav()

            #m.gravity()         #gravity


            if LeftClick:               #grab detection
                if (MousePos[0] < (m.pos[0] + m.radius)) and (MousePos[0] > (m.pos[0] - m.radius)):
                    if (MousePos[1] < (m.pos[1] + m.radius)) and (MousePos[1] > (m.pos[1] - m.radius)):
                        if heldMassName == 0 or heldMassName == m.name:
                            heldMassName = m.name
                            m.held = True
                            HeldMassObj = m

            m.draw(t, dist, MousePos, springs[0])       #draw

#       inter grav
        '''
        for m in bodies:
            try:
                m.interGrav(n)
                n.interGrav(m)
            except:
                pass
            n = m
            '''


#SPRING
        for s in springs:
            s.draw(anchor, bodies[3], t)        #draw spring


        '''
        for p in penulum:
            bodies[0].penulum(p)
            p.draw(bodies[0], t)
            '''

        pygame.display.update()     #update screen
        WIN.fill((217,217,217))     #clear prev frame


if __name__ == '__main__':
    main()
