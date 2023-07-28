import math
import pygame
import os
import time
import matplotlib.pyplot as plt
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

        if (self.pos[1] + self.radius) > (spring.pos[1]) and self.pos[0] > (spring.pos[0] - self.radius) and self.pos[0] < (spring.pos[0] + self.radius):
            self.vel = np.array((0,0))
            appliedForce = self.force[1]
            spring.appliedForce = self.force[1]
            self.pos[1] = spring.pos[1] - self.radius
            self.onSpring = True

        if self.onSpring == True:
            self.pos[0] = spring.pos[0]

            #print ("preForce: {} \t postForce: {} \t ballForce: {}".format(preForce, spring.force[1], self.force[1]))
            #print ("collision at {}".format(self.pos))

        if (t*60)%30 < 1:
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
        #WIN.blit(massdisp, self.pos - np.array((self.radius/2, 10)))
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
        '''
        if self.accel[0] > 0:
            self.accel[0] -= fricForce/self.mass
        if self.accel[0] < 0:
            self.accel[0] += fricForce/self.mass
            '''
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
            drag_force = 0.0 * DRAG_COEF * self.area * pythag(self.vel)**2 * (-vhat)
            #drag_force = 0

            self.force = grav_force + drag_force
            #print (self.area)
            #print ("F: {} \t A: {} \t drag_force: {} \t Gforce: {} \t vel: {}".format(self.force, self.accel, drag_force, grav_force, self.vel))
        else:
            self.force = grav_force
            #print ("F: {} \t A: {} \t drag_force: {} \t Gforce: {} \t vel: {}".format(self.force, self.accel, "drag_force", grav_force, self.vel))
            #print (self.force)


class spring():
    setpos = np.array((0,0))
    setcolor = ((100,100,100))
    def __init__(self, spring_const=10, pos=setpos, color=setcolor, width=24, height=100):
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
        self.equilibreum = 0
        self.displacement = 0
        self.y = self.pos[1]
        self.dampen = 0.7


    def draw(self, body, t):

        self.appliedForce = self.appliedForce + -self.dampen*body.vel[1]

        f = (0.5 * pi) * (np.sqrt(self.spring_const/body.mass))
        w = (2 * pi) * f
        T = 1/f
        A = self.appliedForce/self.spring_const

        self.displacement += A * math.cos(w*t) * dt

        self.pos[1] = self.y + self.displacement


        print ("displacement: {} \t amp: {} w: {}".format(self.displacement, A, w))



        '''
        print ("s: {} \t eq: {} \t appliedForce: {}".format(self.displacement, self.equilibreum, self.appliedForce))
        if self.displacement <= self.equilibreum:
            self.pos[1] = self.pos[1] + (self.appliedForce/self.spring_const)
            self.displacement = self.displacement + (self.appliedForce/self.spring_const)
            print ("down")

        if self.displacement > self.equilibreum:
            self.pos[1] = self.pos[1] + (-self.appliedForce/self.spring_const)
            self.displacement += (-self.appliedForce/self.spring_const)
            print ("up")

        '''
        self.height = bottomwall - self.pos[1]



        #print ("prepos: {}\t pos: {} Change: {}".format(prepos, self.pos[0], prepos - self.pos[0]))

        pygame.draw.rect(WIN, self.color, (self.pos[0], self.pos[1], self.width, self.height), 2)
        #Ddisp = font.render("dist: {}".format(dist), True, BLACK)

        #WIN.blit(Ddisp, self.pos - np.array((self.width/2, self.height/2)))

        if (self.pos[1] + self.height) > bottomwall:
            self.vel = np.array((0,0))

#mass object
#m1 = mass1(pos = np.array((200,200)), radius=50, mass=(50), vel = np.array((0,0)), name="m1")
#m2 = mass1(pos = np.array((110,110)), vel = np.array((0, 0)), color=((150,255,155)), radius=15, mass=(10), name="m2")
#m3 = mass1(pos = np.array((275,275)), radius=25, mass=(80), vel = np.array((0,0)), name="m1", color=(( randint(0, 255), randint(0, 255), randint(0, 255) )))

forcedata = []
randPos = np.array((450, bottomwall-100))
bodies = []
springs = [spring(pos=randPos)]

j= 0
while j < 1:
    randPos = np.array((randint(110, 720), randint(55, 380)))
    randColor = (( randint(0, 255), randint(0, 255), randint(0, 255) ))
    #randRadius = randint(2, 50)
    randRadius = 50
    randVel = np.array((0,10))

    bodies.append( mass1(radius=randRadius, name="m{}".format(j + 1), pos=randPos, mass=60, color=randColor, vel=randVel ) )

    j+=1



#main
def main():
    clock = pygame.time.Clock()
    running = True
    t = 1/FPS
    #n=bodies[1]
    prevt = 0
    #prevPos = m3.pos
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


    #collision box
        pygame.draw.rect(WIN, BLACK, pygame.Rect(leftwall, topwall, rightwall-100, bottomwall-50),  5)

        for m in bodies:
            m.linInterp()




    #collision detection with ball
        for m in bodies:
            for n in bodies:

                if n == m:
                    pass
                else:
                    #print ("m: {} \t n: {}".format(m.name, n.name))
                    dist = distance(m.pos, n.pos)

                    if dist <= (m.radius + n.radius):
                        m.interCollide(dist, n, springs[0])
                        #n.interCollide(dist, n)
                        #HeldMassObj.held = False



        MousePos = np.array((Mouse_x, Mouse_y))


    #movement
        for m in bodies:
            m.pos = m.pos + (m.vel * dt * 2.5)
            m.vel = m.vel + (m.accel * dt * 2.5)

            '''
            if m.pos[0] < 0:
                m.pos[0] = WIDTH
            if m.pos[0] > WIDTH:
                m.pos[0] = 0
            if m.pos[1] < 0:
                m.pos[1] = HEIGHT
            if m.pos[1] > HEIGHT:
                m.pos[1] = 0
            '''
    #grav

        for m in bodies:
            m.gravity()


        #m2.interGrav(m1)
        '''
        for m in bodies:
            if bodies[-1] == m:
                pass
            else:
                m.interGrav(bodies[-1])
            '''


    #stat
        tdisp = font.render("t: " + str(t), True, WHITE)


    #grab detection
        for m in bodies:
            if LeftClick:
                if (MousePos[0] < (m.pos[0] + m.radius)) and (MousePos[0] > (m.pos[0] - m.radius)):
                    if (MousePos[1] < (m.pos[1] + m.radius)) and (MousePos[1] > (m.pos[1] - m.radius)):
                        if heldMassName == 0 or heldMassName == m.name:
                            heldMassName = m.name
                            m.held = True
                            HeldMassObj = m



        for m in bodies:
            m.draw(t, dist, MousePos, springs[0])

        for s in springs:
            s.draw(bodies[0], t)



        '''
        if pythag(m1.force) < (10**50):
            forcedata.append(pythag(m1.force))

        '''

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


if __name__ == '__main__':
    main()


'''
TODO:
friction
collision between multiple

'''
