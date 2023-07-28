import matplotlib.pyplot as plt
import math
pi = math.pi

def d2r (d):
    r = d * (pi/180)
    return r

grav = 9.8
mass = 20
massN = mass * grav
friction_coeff = 0.25

appliedForceM = 100.0              #N
appliedForceA = -30.0              #degree

#velocity calc
#F = m(v/t)

appliedForceY = appliedForceM * math.sin(d2r(appliedForceA))
appliedForceX = appliedForceM * math.cos(d2r(appliedForceA))

normalForce = massN - appliedForceY
fricForce = friction_coeff * normalForce

print ("normal force: {}".format(normalForce))
print ("applied force x: {}".format(appliedForceX))
print ("Frictional Force: {}".format(fricForce))
print ("-------------------------------")


def ForceNet (d):
    forcenet = (appliedForceX) - (fricForce)

    return forcenet

def getVel (d):
    force = ForceNet(d)
    vsq = (2 * force)/mass
    print (vsq)
    try:
        v = math.sqrt(vsq)
    except:
        v = 0
    return v

def getTime (d, v):
    try:
        return d/v
    except:
        return 0

def getAcc (F, m):
    try:
        return F/m
    except:
        return 0

#print ("(6m) Velocity: {}".format(getVel(6)))
#print ("(6m) Force Net: {}".format(ForceNet(6)))

def forceTime (max_distance, increment):

    time = []
    force = []

    d = 1
    while d < max_distance:

        f = ForceNet(d)
        v = getVel(d)
        t = getTime(d, v)

        time.append(t)
        force.append(f)

        d+=increment

    return [time, force]

#print (forceTime(30, 1))

x = forceTime(30, 1)[0]
y = forceTime(30, 1)[1]
plt.plot(x, y)
plt.ylabel("Force")
plt.xlabel("Time")
plt.show()

#########
#FIX FRICTION
#impulse
#momentum




def velCalc (time) :
    #Fnet = 20(v/time)
    v = (ForceNet * time) / mass
    return v

#ForceNet(d) = 1/2mv^2
def timeDistance (time):
    vel = velCalc(time)
    return vel

def forceTime (max_time, increment):
    i = 0
    while i < max_time:
        distance = timeDistance(i)
        i+=increment
        print (distance)

#forceTime(100, 10)
