from vpython import *
import math

scene.forward = vector(0,-.3,-1)

x0 = 1.0
y0 = 0.225
z0 = 0.69

a = 2.1

def Map_x (x, y):
    return math.sin (x) -math.sin (a * y)

def Map_y (x, y):
    return x


#print ("(x, y): " + str(x) + str(y))

point1 = sphere(pos=vector(x0, y0, z0), radius=0.1, color=color.orange, make_trail=True)
point2 = sphere(pos=vector(x0+0.001, y0+0.001, z0+0.001), radius=0.1, color=color.blue, make_trail=True)

dt = 1e-5
t=0

prevx1 = x0
prevy1 = y0
prevx2 = x0+0.001
prevy2 = y0+0.001

while True:
    rate(200)

    xpos1 = Map_x(prevx1, prevy1)
    ypos1 = Map_y(prevx1, prevy1)

    point1.pos = vector(xpos1, ypos1, z0)

    prevx1 = xpos1
    prevy1 = ypos1

    xpos2 = Map_x(prevx2, prevy2)
    ypos2 = Map_y(prevx2, prevy2)

    point2.pos = vector(xpos2, ypos2, z0)

    prevx2 = xpos2
    prevy2 = ypos2

    t = t + dt
