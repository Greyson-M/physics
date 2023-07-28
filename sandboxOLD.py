import math
import pygame
import os
import time
import matplotlib.pyplot as plt
import numpy as np
from random import randint

np.seterr(divide='ignore', invalid='ignore')

def E(x):
    return 10**x

#GAME constants
FPS = 60
WIDTH, HEIGHT = 1800, 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
dt = (1/FPS)

#physics constants
g = 9.80   #m/s^2
G = 5
#print (G)



#   starting conditions
pos = (20, 20)

pi = math.pi


#load
pygame.init()
#BALL_B_IMAGE = pygame.image.load('ball1.png')
#BALL_A_IMAGE = pygame.image.load('ball2.png')
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN.fill((217, 217, 217))

sysfont = pygame.font.get_default_font()
#print('system font :', sysfont)
t0 = time.time()
font = pygame.font.SysFont(None, 18)

def pythag (vector):
    a = (vector[0]**2) + (vector[1]**2)
    return math.sqrt(a)

def distance (vec1, vec2):
    xdis = vec2[0] - vec1[0]
    ydis = vec2[1] - vec1[1]
    return pythag([xdis, ydis])

pos0 = np.array((125, 125))
vel0 = np.array((14, 10))
accel0 = np.array((0, g))

def gforce(p1,p2):
    # Calculate the gravitational force exerted on p1 by p2.
    # Calculate distance vector between p1 and p2.
    r_vec = p1.pos-p2.pos
    # Calculate magnitude of distance vector.
    r_mag = pythag(r_vec)
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


topwall = 50
bottomwall = 900
rightwall = 1600
leftwall = 100


class mass1():
    randPos = np.array((randint(110, 720), randint(55, 380)))
    #randPos[0] = randint(110, 720)
    #randPos[1] = randint(55, 380)
    randVel = np.array((randint(0, 10), randint(0, 10)))

    randColor = (( randint(0, 255), randint(0, 255), randint(0, 255) ))
    randRadius = randint(5, 50)

    def __init__(self, mass=10, pos=np.array((randint(110, 720), randint(55, 380))),
     vel=np.array((randint(0, 10), randint(0, 10))), accel=np.array((0, 0)),
      radius=randint(5, 50), color=(( randint(0, 255), randint(0, 255), randint(0, 255) ))):
        self.mass = mass      #kg
        self.pos = pos
        self.vel = vel
        self.accel = accel
        self.color = color
        self.radius = radius
        self.area = self.radius
        self.force = self.mass * self.accel



    def draw(self, t, dist):
        self.scalarVel = pythag(self.vel)
        self.p = self.scalarVel * self.mass
        self.accel = self.force / self.mass
        #print (self.p)

        pygame.draw.circle(WIN, self.color, self.pos, self.radius)
        #WIN.blit(BALL_A_IMAGE, self.pos-np.array((70,0)))

        #display data
        tdisp = font.render("t: " + str(round(t)), True, BLACK)
        posdisp = font.render("distance: " + str(dist), True, BLACK)
        veldisp = font.render("vel: " + str(np.rint(self.vel)), True, BLACK)       #np.rint(self.vel)        #round(self.scalarVel)
        acceldisp = font.render("accel: " + str(self.accel), True, BLACK)

        WIN.blit(tdisp, (20, 20))
        WIN.blit(posdisp, (20, 40))
        WIN.blit(veldisp, self.pos)
        WIN.blit(acceldisp, self.pos - np.array((0, 10)))

    def collidey(self):      #collision response
        #print ("COLLIDE")
        self.vel[1] = -self.vel[1]
        '''
        if self.accel[0] < 75:
            self.accel[1] += 7
            '''
    def collidex(self):
        #print("COLLIDE")
        self.vel[0] = -self.vel[0]

    def interCollide(self, dist, collider):
          dpos = self.pos-collider.pos
          dist = np.sqrt(np.sum(dpos**2))
          if dist < self.radius+collider.radius:
              offset = dist-(self.radius+collider.radius)
              self.pos = self.pos + (-dpos/dist)*offset/2
              collider.pos = collider.pos + (dpos/dist)*offset/2
              total_mass = self.mass+collider.mass
              dvel1 = -2*collider.mass/total_mass*np.inner(self.vel-collider.vel,self.pos-collider.pos)/np.sum((self.pos-collider.pos)**2)*(self.pos-collider.pos)
              dvel2 = -2*self.mass/total_mass*np.inner(collider.vel-self.vel,collider.pos-self.pos)/np.sum((collider.pos-self.pos)**2)*(collider.pos-self.pos)
              self.vel = self.vel+dvel1
              collider.vel = collider.vel + dvel2

    def linInterp(self):

        distfromTOPwall = self.pos[1] - topwall
        distfromBOTTOMwall = bottomwall - self.pos[1]
        distfromLEFTwall = self.pos[0] - leftwall
        distfromRIGHTwall = rightwall - self.pos[0]


        distances = np.array((distfromTOPwall, distfromBOTTOMwall, distfromLEFTwall, distfromRIGHTwall))

        currentPos = (self.vel*1) + (1/2 * (self.force/self.mass) * 1**2)
        nextpos = (self.vel*(1+dt)) + (1/2 * (self.force/self.mass) * (1+dt)**2)
        nextFramePos = nextpos - currentPos

        #print ("pos: {} \t nextFramePos: {}".format(self.pos, nextFramePos))

        if self.pos[1] >= (bottomwall - self.radius) or self.pos[1] <= (topwall + self.radius):
            self.collidey()

        if self.pos[0] >= (rightwall - self.radius) or self.pos[0] <= (leftwall + self.radius):
            self.collidex()

        else:

            if distances.argsort()[0] == 0:         #top
                if (self.pos[1] + nextFramePos[1]) < topwall:
                    if self.vel[1] < 0:
                        print ("COLLISION vel: {} \t accel: {} \t dist from topwall: {}".format(self.vel, self.force/self.mass, distfromTOPwall))
                        self.pos = np.array((self.pos[0], topwall+self.radius))
                        self.collidey()
                        self.color = BLACK

                    else:
                        #print ("pos: {} \t nextFramedistance: {} \t dist from rightwall: {}".format(self.pos, nextFramePos, distfromRIGHTwall))
                        pass
            if distances.argsort()[0] == 1:         #bottom
                if (self.pos[1] + nextFramePos[1] > bottomwall):
                    if self.vel[1] > 0:
                        print ("COLLISION pos: {} \t nextFramedistance: {} \t dist from botwall: {}".format(self.pos, nextFramePos, distfromBOTTOMwall))
                        self.pos = np.array((self.pos[0], bottomwall-self.radius))
                        self.collidey()

                else:
                    #print ("pos: {} \t nextFramedistance: {} \t dist from rightwall: {}".format(self.pos, nextFramePos, distfromRIGHTwall))
                    pass
            if distances.argsort()[0] == 2:         #left
                if (self.pos[0] + nextFramePos[0] < leftwall):
                    if self.vel[0] < 0:
                        print ("COLLISION pos: {} \t nextFramedistance: {} \t dist from lefwall: {}".format(self.pos, nextFramePos, distfromLEFTwall))
                        self.pos = np.array((leftwall+self.radius, self.pos[1]))
                        self.collidex()

                else:
                    #print ("pos: {} \t nextFramedistance: {} \t dist from rightwall: {}".format(self.pos, nextFramePos, distfromRIGHTwall))
                    pass
            if distances.argsort()[0] == 3:         #right
                if (self.pos[0] + nextFramePos[0] > rightwall):
                    if self.vel[0] > 0:
                        print ("COLLISION pos: {} \t nextFramedistance: {} \t dist from rightwall: {}".format(self.pos, nextFramePos, distfromRIGHTwall))
                        self.pos = np.array((rightwall-self.radius, self.pos[1]))
                        self.collidex()

                else:
                    #print ("pos: {} \t nextFramedistance: {} \t dist from rightwall: {}".format(self.pos, nextFramePos, distfromRIGHTwall))
                    pass
            else:
                #print ("pos: {} \t nextFramedistance: {} \t dist from rightwall: {}".format(self.pos, nextFramePos, distfromRIGHTwall))
                pass

            #print (self.pos)

    def interGrav (self, n):
        if n.color != WHITE:
            r = self.pos - n.pos        #distance vector
            top = G * self.mass * n.mass
            bottom = r**2
            #F = top/bottom
            F = gforce(self, n)
            #print(self.accel)

            self.accel = F/self.mass
        #    print("F: {}\t a:{}".format(F, self.accel) )
        else:
            pass

    def addForce (self, F):
        n=self
        a = F/n.mass
        self.accel += a


class mouse:
    randPos = np.array((randint(110, 720), randint(55, 380)))
    #randPos[0] = randint(110, 720)
    #randPos[1] = randint(55, 380)
    randVel = np.array((randint(0, 10), randint(0, 10)))

    randColor = (( randint(0, 255), randint(0, 255), randint(0, 255) ))
    randRadius = randint(5, 50)

    def __init__(self, mass=10, pos=np.array((randint(110, 720), randint(55, 380))),
     vel=np.array((randint(0, 10), randint(0, 10))), accel=np.array((0, 0)),
      radius=randint(5, 50), color=(( randint(0, 255), randint(0, 255), randint(0, 255) ))):
        self.mass = mass      #kg
        self.pos = pos
        self.accel = accel
        self.color = color
        self.radius = radius
        self.vel = np.array((dt, dt))


    def draw(self, t, dist, prevPos):
        a = (self.pos - prevPos)
        self.vel = a * 2
        #print("Vel: {} \t a: {} \t prevPos: {} \t POS: {}".format(self.vel, a, prevPos, self.pos))

        #print (self.p)

        pygame.draw.circle(WIN, self.color, self.pos, self.radius)
        #WIN.blit(BALL_A_IMAGE, self.pos-np.array((70,0)))

        #display data
        tdisp = font.render("t: " + str(round(t)), True, BLACK)
        posdisp = font.render("position: " + str(np.rint(self.pos)), True, BLACK)
        veldisp = font.render("vel: " + str(np.rint(self.vel)), True, BLACK)       #np.rint(self.vel)        #round(self.scalarVel)
        acceldisp = font.render("accel: " + str(self.accel), True, BLACK)

    #    WIN.blit(tdisp, (20, 20))
        WIN.blit(posdisp, self.pos - np.array((0, 10)))
        WIN.blit(veldisp, self.pos)
        #WIN.blit(acceldisp, self.pos - np.array((0, 10)))

    def collidey(self):      #collision response
        #print ("COLLIDE")
        self.vel[1] = -self.vel[1]

    def collidex(self):
        #print("COLLIDE")
        self.vel[0] = -self.vel[0]

    def interCollide(self, dist, collider):
          dpos = self.pos-collider.pos
          dist = np.sqrt(np.sum(dpos**2))
          if dist < self.radius+collider.radius:
              offset = dist-(self.radius+collider.radius)
              self.pos = self.pos + (-dpos/dist)*offset/2
              collider.pos = collider.pos + (dpos/dist)*offset/2
              total_mass = self.mass+collider.mass
              dvel1 = -2*collider.mass/total_mass*np.inner(self.vel-collider.vel,self.pos-collider.pos)/np.sum((self.pos-collider.pos)**2)*(self.pos-collider.pos)
              dvel2 = -2*self.mass/total_mass*np.inner(collider.vel-self.vel,collider.pos-self.pos)/np.sum((collider.pos-self.pos)**2)*(collider.pos-self.pos)
              self.vel = self.vel+dvel1
              collider.vel = collider.vel + dvel2


#mass object
m1 = mass1(pos = np.array((800,450)), radius=50, mass=(0.5), vel = np.array((0,0)))
m2 = mass1(pos = np.array((175,150)), vel = np.array((0, 0)), color=((150,255,155)), radius=5, mass=(10))
m3 = mouse(color=WHITE, radius=50, mass=30)

forcedata = []

bodies = [m1, m3]


def minYDist(point, rect):
    pass

#main
def main():
    clock = pygame.time.Clock()
    running = True
    t = 1/FPS
    n=bodies[1]
    prevt = 0
    prevPos = m3.pos


    pygame.display.flip()

    while running:
        clock.tick(FPS)
        prevt += (1/FPS)
        t += (1/FPS)

        m1x = m1.pos[0]
        m1y = m1.pos[1]

        m2x = m2.pos[0]
        m2y = m2.pos[1]

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



    #collision box
        pygame.draw.rect(WIN, BLACK, pygame.Rect(leftwall, topwall, rightwall-100, bottomwall-50),  5)
        '''
    #collision detection with box
        for m in bodies:
            mx = m.pos[0]
            my = m.pos[1]



            if my >= (bottomwall - m.radius) or my <= (topwall + m.radius):
                m.collidey()

            if mx >= (rightwall - m.radius) or mx <= (leftwall + m.radius):
                m.collidex()
                '''

        for m in bodies:
            if m.color != WHITE:
                m.linInterp()

    #collision detection with ball
        for m in bodies:
            dist = distance(m.pos, n.pos)

            if dist <= (m.radius * 2):
                m.interCollide(dist, n)
                #n.interCollide(dist, n)

            n=m

    #movement
        for m in bodies:
            #for velocity calc of mouse mass
            if (t*60)%30 < 1:
                prevPos = m3.pos
                #print(prevPos)
                #print ((t*60)%30)

            try:
                m.pos = m.pos + (m.vel * dt * 2.5)
                m.vel = m.vel + (m.accel * dt * 2.5)
            except:
                pass

            m3.pos = np.array((Mouse_x, Mouse_y))



            #air resistance




    #grav

        for m in bodies:
            if m.color != WHITE:
                drag_coef = 1
                grav_force = np.array((0, g * m.mass))
                if pythag(m.vel) != 0:
                    vhat = m.vel / pythag(m.vel)
                    print (vhat)
                    drag_force = 0.005 * drag_coef * m.area * pythag(m.vel)**2 * (-vhat)

                    m.force = grav_force + drag_force
                    #print (m.area)
                    #print ("F: {} \t A: {} \t drag_force: {} \t Gforce: {} \t vel: {}".format(m.force, m.accel, drag_force, grav_force, m.vel))
                else:
                    m.force = grav_force
                    #print ("F: {} \t A: {} \t drag_force: {} \t Gforce: {} \t vel: {}".format(m.force, m.accel, "drag_force", grav_force, m.vel))
                #print (m.force)



                #print ("F: {} \t A: {} \t drag_force: {} \t Gforce: {}".format(m.force, m.accel, drag_force, grav_force))


        #m2.interGrav(m1)
        '''
        for m in bodies:
            try:
                m.interGrav(n)
                n.interGrav(m)
            except:
                pass
            n = m
            '''

    #stat
        tdisp = font.render("t: " + str(t), True, WHITE)


        for m in bodies:
            try:
                m.draw(t, dist)
            except:
                m3.draw(t, dist, prevPos)


        if pythag(m1.force) < (10**50):
            forcedata.append(pythag(m1.force))



        #print ("prevPos: {} \t POS: {}".format(prevPos, m3.pos))

        pygame.display.update()
        WIN.fill((217,217,217))
        '''
        if t > 10:
            break
            '''

    plt.plot(forcedata)
    plt.ylabel('Force (N)')
    plt.show()



main()
