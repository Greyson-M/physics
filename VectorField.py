import math
import pygame
import os
import time
import matplotlib.pyplot as plt
import numpy as np
from random import randint

def E(x):
    return 10**x

#GAME constants
FPS = 60
WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
dt = (1/FPS)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN.fill((217, 217, 217))
sysfont = pygame.font.get_default_font()
#print('system font :', sysfont)
t0 = time.time()
font = pygame.font.SysFont(None, 18)

G = 5


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

def field(particle, attractor):

    x = particle.pos[0]
    y = particle.pos[1]
    amp = 0.2
    speed = 10
    F = np.array([0,0])

    '''
    G = 1.0
    x_dist = float(attractor.pos[0] - x)
    y_dist = float(attractor.pos[1] - y)

    F[0] = float((G * particle.mass * attractor.mass)/(x_dist**2))
    F[1] = float((G * particle.mass * attractor.mass)/(y_dist**2))

    print ("top: {} \t bottom: {}  \t x_dist: {} Fx: {}".format((G * particle.mass * attractor.mass), (x_dist**2), x_dist, F[0]))
    '''
    
    F = gforce(particle, attractor)

    #cat
    F[0] = y * np.sin(y * amp) * speed
    F[1] = x * np.cos(x * amp) * speed

    #F[0] = speed * (min( np.cos(y * amp), (y - x) ))
    #F[1] = speed * pythag([x,y])

    return F


class mass1():

    def __init__(self, mass=10, pos=np.array((randint(-600.0, 600.0), randint(-320.0, 320.0))),
     vel=np.array((randint(0, 10), randint(0, 10))), accel=np.array((0, 0)),
      radius=randint(5, 50), color=(( randint(0, 255), randint(0, 255), randint(0, 255) ))):
        self.mass = mass      #kg
        self.pos = pos * np.array([1.0, 1.0])
        self.vel = vel
        self.accel = accel
        self.color = color
        self.radius = radius
        self.force = self.mass * self.accel
        self.offset = np.array((640, 360))
        self.age = 0

    def draw(self):

        self.age += 1


        pygame.draw.circle(WIN, self.color, self.pos+self.offset, self.radius)

        #display data
        veldisp = font.render("vel: " + str(np.rint(self.vel)), True, BLACK)       #np.rint(self.vel)        #round(self.scalarVel)
        acceldisp = font.render("accel: " + str(self.accel), True, BLACK)

        #WIN.blit(veldisp, self.pos - np.array((self.radius/2, 0)))
        #WIN.blit(acceldisp, self.pos - np.array((0, 10)))

    def addForce (self, F):
            self.accel[0] += F[0]/self.mass
            self.accel[1] += F[1]/self.mass


x_attractors = []
y_attractors = []
i = -640
while i < 640:
    if np.cos(i) > 1:
        x_attractors.append(i)
    i += 1
i = -320
while i < 320:
    if np.sin(i) > 1:
        y_attractors.append(i)
    i +=1

bodies = []

def create (n):
    j= 0
    while j < n:
        randPos = np.array((randint(-640, 640.0), randint(-360, 360.0)))
        #randColor = (( randint(0, 255), randint(0, 255), randint(0, 255) ))
        randColor = BLACK
        randRadius = 2
        randVel = np.array((20,0))
        randAccel = np.array((0, 0))

        bodies.append(mass1(radius=randRadius, pos=randPos, mass=100, color=randColor, vel=randVel, accel = randAccel ) )

        j+=1

create(250)

sun = mass1(radius=50, pos=np.array([0,0]), color = BLACK, mass=5500)

def main():
    clock = pygame.time.Clock()
    running = True
    t = 1/FPS
    pygame.display.flip()

    while running:
        clock.tick(FPS)
        t += (1/FPS)

        Mouse_x, Mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
#check for quit
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()


        for m in bodies:
            #m.addForce(force)

            #m.accel = m.accel + ((vf.field(m, sun))/m.mass) * dt
            #print (m.accel)
            #m.vel = m.vel + (m.accel * dt * 2.5)
            m.vel = field(m, sun) * dt * 2.5
            m.pos = m.pos + (m.vel * dt * 2.5)      #update pos
            '''
            if m.vel.all() == 0:
                bodies.remove(m)
                create(1)
                #print ("REGEN")
                '''

            m.draw()

        #sun.draw()

        countdisp = font.render("count: " + str(np.size(bodies)), True, BLACK)
        fpsdisp = font.render("fps: " + str(clock.get_fps()), True, BLACK)

        WIN.blit(countdisp, np.array([5,5]))
        WIN.blit(fpsdisp, np.array([5,15]))


        regen_rate = 0

        del bodies[0:regen_rate]
        create(regen_rate)


        pygame.display.update()     #update screen
        WIN.fill((217,217,217))     #clear prev frame


if __name__ == '__main__':
    main()




'''
x_range = y_range = np.linspace(-100, 100, 100)
x, y = np.meshgrid(x_range, y_range)
fx, fy = y, -x

#print (fx, fy)

plt.figure(figsize=(8,8))
plt.quiver(x[5::10,5::10], y[5::10,5::10], fx[5::10,5::10], fy[5::10,5::10], pivot="middle")
plt.axis("scaled")
plt.show()
'''
