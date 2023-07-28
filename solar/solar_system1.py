from vpython import *
import math

scene.forward = vector(0,-.3,-1)

G = 0.0001
STARTING_ANGLE = 30
r = 149.6e5

x = r*(math.cos(STARTING_ANGLE))
y = r*(math.sin(STARTING_ANGLE))

print ("(x, y): " + str(x) + str(y))

star = sphere(pos=vector(0,0,0), radius=10e5, color=color.orange, mass = 1988500e25)
planet1 = sphere(pos=vector(x, 0, y), radius=5e5, color=color.green, mass = 5.9724324e24, make_trail=True)

planet1VelSQ = (G * star.mass)/r
planet1.vel = sqrt(planet1VelSQ)

momentum = planet1.vel * planet1.mass
planet1.p = vector(momentum/2, 0, momentum/2)

def gforce(p1,p2):
    # Calculate the gravitational force exerted on p1 by p2.
    # Calculate distance vector between p1 and p2.
    r_vec = p1.pos-p2.pos
    # Calculate magnitude of distance vector.
    r_mag = mag(r_vec)
    # Calcualte unit vector of distance vector.
    r_hat = r_vec/r_mag
    print (r_hat)
    # Calculate force magnitude.
    force_mag = G*p1.mass*p2.mass/r_mag**2
    # Calculate force vector.
    force_vec = -force_mag*r_hat
    return force_vec


dt = 1e-5
t=0
while True:
    rate(200)
    F = gforce(planet1, star)

    planet1.p = planet1.p + F * dt

    planet1.pos = planet1.pos + (planet1.p/planet1.mass)*dt
    pos = planet1.pos + (planet1.p/planet1.mass)*dt


    t = t + dt
