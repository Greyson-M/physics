import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation



a = 6
b = -12
c = -0.38


def lorenz(x, y, z):
    x_dot = a*x - y*z
    y_dot = b*y + x*z
    z_dot = c*z + x * (y/3)
    return x_dot, y_dot, z_dot

dt = 0.001
num_steps = 50000

xs = np.empty(num_steps + 1)
ys = np.empty(num_steps + 1)
zs = np.empty(num_steps + 1)
xs[0], ys[0], zs[0] = (0.1, 0.1, 1.05)

for i in range(num_steps):
    x_dot, y_dot, z_dot = lorenz(xs[i], ys[i], zs[i])
    xs[i + 1] = xs[i] + (x_dot * dt)
    ys[i + 1] = ys[i] + (y_dot * dt)
    zs[i + 1] = zs[i] + (z_dot * dt)

    #print (str(xs[i]) + "\t\t" + str(ys[i]) + "\t\t" + str(zs[i]))


fig = plt.figure()
ax = fig.gca(projection='3d')

line, = ax.plot(xs, ys, zs, lw=0.5)
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("a = {} b = {} c = {} BASE". format(a, b, c))

plt.axis('off')
fig.patch.set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

def animate (i):
    line.set_xdata(xs[i])
    line.set_ydata(ys[i])
    line.set_zdata(zs[i])
    return line

ani = animation.FuncAnimation(
    fig, animate, interval=20, blit=True, save_count=50)

plt.show()
