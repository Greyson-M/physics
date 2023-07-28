import matplotlib.pyplot as plt
import math
pi = math.pi

def d2r (d):
    r = d * (pi/180)
    return r

acc = -2.54
veli = 1.5843781233797656
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


def ForceNet ():
    forcenet = (appliedForceX) - (fricForce)

    return forcenet

def getVel (d):
    #return (veli ** 2.0) + (2.0 * acc)(d)
    velisq = veli**2
    ac = 2 * acc
    ad = ac * d
    return velisq + ad

print (getVel(6.0))

def getDistance (t):
    pass


print ("VEL: {}".format(getVel()))

def getTime (d, v):
    try:
        return d/v
    except:
        return 0

def getFricAcc ():
    return (-1 * friction_coeff * grav)

#print ("(6m) Velocity: {}".format(getVel(6)))
#print ("(6m) Force Net: {}".format(ForceNet(6)))

def velTime (max_time, increment):
    time = []
    vel = []

    t = 0
    while t < max_time:

        v = getVel()


        t += increment


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

x = velTime(30, 1)[0]
y = velTime(30, 1)[1]
plt.plot(x, y)
plt.ylabel("Velocty")
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
