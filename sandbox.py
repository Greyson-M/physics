import math
import pygame
import os
import time
import numpy as np
from random import randint

#np.seterr(divide='ignore', invalid='ignore')

def E(x):
    return 10**x

#GAME constants
FPS = 60
WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
dt = (1/FPS)

#physics constants
g = 9.80   #m/s^2
G = 5.2383524 * E(-18)
AIR_DENSITY = 1.225
DRAG_COEF = 1
print (G)



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


topwall = 50
bottomwall = HEIGHT - 50
rightwall = WIDTH - 100
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
      radius=randint(5, 50), color=(( randint(0, 255), randint(0, 255), randint(0, 255) )), name="" ):
        self.mass = mass      #kg
        self.pos = pos
        self.vel = vel
        self.accel = accel
        self.color = color
        self.radius = radius
        self.area = self.radius
        self.force = self.mass * self.accel
        self.kinEnergy = (0.5*self.mass) * (self.vel**2)
        self.name = name
        self.held = False
        self.prevPos = self.pos
        self.F = 0
        self.onSpring = False
        #print ("mass: {} \t vel: {} \t kin: {}".format(self.mass, self.vel, self.kinEnergy))

    def draw(self, t, dist, MousePos, spring):
        #print ("mass: {} \t vel: {} \t kin: {}".format(self.mass, self.vel, self.kinEnergy))
        self.scalarVel = pythag(self.vel)
        self.p = self.vel * self.mass
        self.accel = self.force / self.mass
        self.force = self.mass * self.accel
        self.normalForce = self.mass * g

        '''
        if (self.pos[1] + self.radius) > (spring.pos[1]) and self.pos[0] > (spring.pos[0] - self.radius) and self.pos[0] < (spring.pos[0] + self.radius):
            self.vel = np.array((0,0))
            appliedForce = self.force[1]
            spring.appliedForce = self.force[1]
            self.pos[1] = spring.pos[1] - self.radius
            self.onSpring = True

        if self.onSpring == True:
            self.pos[0] = spring.pos[0]
        '''

            #print ("preForce: {} \t postForce: {} \t ballForce: {}".format(preForce, spring.force[1], self.force[1]))
            #print ("collision at {}".format(self.pos))

        if (t*60)%10 < 1:
            if self.held:
                self.prevPos = self.pos

        if self.held == True:
            self.pos = MousePos

            self.vel = (self.pos - self.prevPos) * 2

        self.terminalVel = np.sqrt((2*self.mass*g)/(AIR_DENSITY * self.area * DRAG_COEF))

        #self.vel = self.p/self.mass

        #print (self.p)

        pygame.draw.circle(WIN, self.color, self.pos, self.radius)
        #WIN.blit(BALL_A_IMAGE, self.pos-np.array((70,0)))

        #display data
        tdisp = font.render("t: " + str(round(t)), True, BLACK)
        #posdisp = font.render("distance: " + str(dist), True, BLACK)
        veldisp = font.render("vel: " + str(np.rint(self.vel)), True, BLACK)       #np.rint(self.vel)        #round(self.scalarVel)
        acceldisp = font.render("accel: " + str(self.accel), True, BLACK)
        namedisp = font.render(self.name, True, BLACK)
        massdisp = font.render("{}kg".format(self.mass), True, BLACK)

        #WIN.blit(tdisp, (20, 20))
        #WIN.blit(posdisp, (20, 40))
        WIN.blit(veldisp, self.pos - np.array((self.radius/2, 0)))
        #WIN.blit(namedisp, self.pos - np.array((self.radius/2, 0)))
        WIN.blit(massdisp, self.pos - np.array((self.radius/2, 10)))
        WIN.blit(acceldisp, self.pos - np.array((0, 10)))

    def addForce (self, F):
            self.accel += F/self.mass

    def collidey(self, side):      #collision response
        #print ("COLLIDE")
        self.vel[1] = -self.vel[1]

        if self.vel[1] == 0:
            self.vel[1] = 0
            self.accel[1] = 0
        elif side == "bottom" and self.vel[1] != 0:
            self.vel[1] = self.vel[1] + 20
        elif side == "top" and self.vel[1] != 0:
            self.vel[1] = self.vel[1] - 20
        if self.vel[1] < 0.01 and self.vel[1] > -0.01 and side != "top":
            self.vel[1] = 0
            self.accel[1] = 0

        #FRICTION
        fricCoef = 0.25
        fricForce = fricCoef * self.normalForce
        vhat = self.vel / pythag(self.vel)

        self.accel[0] += fricForce/self.mass * (-vhat[0])


    def collidex(self, side):
        #print("COLLIDE")
        self.vel[0] = -self.vel[0]

        if self.vel[0] == 0:
            self.vel[0] = 0
        elif side == "right" and self.vel[0] != 0:
            self.vel[0] = self.vel[0] + 20
        elif side == "left" and self.vel[0] != 0:
            self.vel[0] = self.vel[0] - 20

    def interCollide(self, dist, collider, spring):
      #  self.held = False
        dpos = self.pos-collider.pos

        if dist == 0:
            dist = 1

        offset = dist-(self.radius+collider.radius)
        self.pos = self.pos + (-dpos/dist)*offset/2
        collider.pos = collider.pos + (dpos/dist)*offset/2
        total_mass = self.mass+collider.mass
        #print ( np.sum( (self.pos-collider.pos) **2) * (self.pos-collider.pos) )

        if dpos[0] == 0 and dpos[1] == 0:
            #print ("self pos: {} \t colliderpos: {}".format(self.pos, collider.pos))
            self.pos += np.array((self.radius + 5, self.radius + 5))
            collider.pos -= np.array((self.radius + 8, self.radius + 8))
            #print ("adjusted")
            #print ("self pos: {} \t colliderpos: {}".format(self.pos, collider.pos))
            dpos = self.pos-collider.pos

            #print (dpos)
        dvel1 = -2 * collider.mass/total_mass * np.inner(self.vel-collider.vel, self.pos-collider.pos) / np.sum( (self.pos-collider.pos)**2) * (self.pos-collider.pos)
        dvel2 = -2 * self.mass/total_mass * np.inner(collider.vel-self.vel, collider.pos-self.pos) / np.sum( (collider.pos-self.pos)**2) * (collider.pos-self.pos)
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
        '''
        if self.pos[1] >= (bottomwall - self.radius) or self.pos[1] <= (topwall + self.radius):
            self.collidey()

        if self.pos[0] >= (rightwall - self.radius) or self.pos[0] <= (leftwall + self.radius):
            self.collidex()
        '''
        if 0 != 0:
            pass
        else:

            if distances.argsort()[0] == 0:         #top
                if (self.pos[1] + nextFramePos[1] - self.radius) < topwall:
                    if self.vel[1] < 0:
                        #print ("COLLISION vel: {} \t accel: {} \t dist from topwall: {}".format(self.vel, self.force/self.mass, distfromTOPwall))
                        self.pos = np.array((self.pos[0], topwall+self.radius))
                        self.collidey("top")

                    else:
                        #print ("pos: {} \t nextFramedistance: {} \t dist from rightwall: {}".format(self.pos, nextFramePos, distfromRIGHTwall))
                        pass
            if distances.argsort()[0] == 1:         #bottom
                if (self.pos[1] + nextFramePos[1] + self.radius) > bottomwall:
                    if self.vel[1] > 0:
                        #print ("COLLISION pos: {} \t nextFramedistance: {} \t dist from botwall: {}".format(self.pos, nextFramePos, distfromBOTTOMwall))
                        self.pos = np.array((self.pos[0], bottomwall-self.radius))
                        self.collidey("bottom")

                else:
                    #print ("pos: {} \t nextFramedistance: {} \t dist from rightwall: {}".format(self.pos, nextFramePos, distfromRIGHTwall))
                    pass
            if distances.argsort()[0] == 2:         #left
                if (self.pos[0] + nextFramePos[0] - self.radius < leftwall):
                    if self.vel[0] < 0:
                       # print ("COLLISION pos: {} \t nextFramedistance: {} \t dist from lefwall: {}".format(self.pos, nextFramePos, distfromLEFTwall))
                        self.pos = np.array((leftwall+self.radius, self.pos[1]))
                        self.collidex("left")

                else:
                    #print ("pos: {} \t nextFramedistance: {} \t dist from rightwall: {}".format(self.pos, nextFramePos, distfromRIGHTwall))
                    pass
            if distances.argsort()[0] == 3:         #right
                if (self.pos[0] + nextFramePos[0] + self.radius > rightwall):
                    if self.vel[0] > 0:
                        #print ("COLLISION pos: {} \t nextFramedistance: {} \t dist from rightwall: {}".format(self.pos, nextFramePos, distfromRIGHTwall))
                        self.pos = np.array((rightwall-self.radius, self.pos[1]))
                        self.collidex("right")

                else:
                    #print ("pos: {} \t nextFramedistance: {} \t dist from rightwall: {}".format(self.pos, nextFramePos, distfromRIGHTwall))
                    pass
            else:
                #print ("pos: {} \t nextFramedistance: {} \t dist from rightwall: {}".format(self.pos, nextFramePos, distfromRIGHTwall))
                pass

            #print (self.pos)

    def interGrav (self, n):
            r = self.pos - n.pos        #distance vector
            top = G * self.mass * n.mass
            bottom = r**2
            #F = top/bottom
            self.F = gforce(self, n)
            #print(self.accel)



            self.accel = self.F/self.mass
            print ("{} \t F:{} a:{}".format(self.name, self.F, self.accel))

        #    print("F: {}\t a:{}".format(F, self.accel) )

    def gravity(self):
        grav_force = np.array((0, g * self.mass))
        if pythag(self.vel) != 0:
            vhat = self.vel / pythag(self.vel)
            #print (vhat)
            drag_force = 0.0005 * DRAG_COEF * self.radius * pythag(self.vel)**2 * (-vhat)
            #drag_force = 0

            self.force = grav_force + drag_force
            #print (self.area)
            #print ("F: {} \t A: {} \t drag_force: {} \t Gforce: {} \t vel: {}".format(self.force, self.accel, drag_force, grav_force, self.vel))
        else:
            self.force = grav_force
            #print ("F: {} \t A: {} \t drag_force: {} \t Gforce: {} \t vel: {}".format(self.force, self.accel, "drag_force", grav_force, self.vel))
            #print (self.force)

    def penulum(self, pend):
        self.pos = pend.botpos

class pendString ():
    setpos = np.array((0,0))
    def __init__(self, toppos=setpos, length=500):
        self.toppos = toppos
        self.length = length
        self.color = ((0, 0, 0,))
        self.botpos = np.array((0,0))
        self.theta = 30
        self.dir = 0


    def draw(self, body, t):
        if self.theta == 30:
            self.dir = -1
        elif self.theta == -30:
            self.dir = 1

        self.theta = self.theta + (1 * self.dir)

        print ("theta: {} \t dir: {}".format(self.theta, self.dir))

        self.botpos[0] = self.toppos[0] + (self.length * np.sin(math.radians(self.theta)))
        self.botpos[1] = self.toppos[1] + (self.length * np.cos(math.radians(self.theta)))
        pygame.draw.line(WIN, self.color, self.toppos, self.botpos, width=5)


class spring():
    setpos = np.array((0,0))
    setcolor = ((100,100,100))
    def __init__(self, spring_const=50, pos=setpos, color=setcolor, width=10, height=100):
        self.spring_const = spring_const
        self.pos = pos
        self.color = color
        self.width = width
        self.height = height
        self.vel = np.array((0,0))
        self.accel = np.array((0,0))
        self.mass = 50
        self.force = 0
        self.area = self.width
        self.appliedForce = 0
        self.equilibreum = self.height
        self.displacement = 0
        self.y = self.pos[1]
        self.dampen = 0.7
        #self.anchorBody = mass1(mass=0, vel=np.array((0,0)), accel=np.array((0,0)), radius=7, name="ANCHOR")


    def draw(self, anchor, body, t):
        self.pos[0] = anchor.pos[0]
        self.pos[1] = anchor.pos[1] - self.height

        body.pos = self.pos





        self.displacement = self.height - self.equilibreum
        self.origin = np.array((self.pos[0], self.pos[1] - self.displacement))
        F = -self.spring_const * self.displacement





        '''
        self.pos = pos

        self.appliedForce = self.appliedForce + -self.dampen*body.vel[1]

        f = (0.5 * pi) * (np.sqrt(self.spring_const/body.mass))
        w = (2 * pi) * f
        T = 1/f
        A = self.appliedForce/self.spring_const

        self.displacement += A * math.cos(w*t) * dt

        self.pos[1] += self.displacement

        self.origin = np.array((self.pos[0], self.pos[1] - self.displacement))


        print ("displacement: {} \t amp: {} w: {}".format(self.displacement, A, w))

        self.height = bottomwall - self.pos[1]
        '''


        pygame.draw.rect(WIN, self.color, (self.pos[0], self.pos[1], self.width, self.height), 2)
        #pygame.draw.circle(WIN, self.color, self.origin, 2)


        '''
        if (self.pos[1] + self.height) > bottomwall:
            self.vel = np.array((0,0))
            '''



'''
TODO:
friction
collision between multiple

'''
