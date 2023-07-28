#graph euler method spring motion
import numpy as np
import matplotlib.pyplot as plt
import math

spring_const = 50
mass = 60
appliedForce = 570
dt = 1/60
displacement = 0
frame = 0
t = 0
pi = math.pi

data = []

while t < 10:

    if t >= 2:
        appliedForce = 570
    else:
        appliedForce = 0

    f = (0.5 * pi) * (np.sqrt(spring_const/mass))
    w = (2 * pi) * f
    T = 1/f
    A = appliedForce/spring_const

    displacement += A * math.cos(w*t) * dt
    data.append(displacement)

    frame+=1
    t = frame/60

    print ("frame: {} \t Time: {} \t Distance: {}".format(frame, t, displacement))

plt.plot(data)
plt.ylabel('Displacement (m)')
plt.xlabel('Time')
plt.show()
