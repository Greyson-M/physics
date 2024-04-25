import numpy as np

# Define a class to represent a fluid
class Fluid:
    # The constructor for the Fluid class
    def __init__(self, size, diffusion, viscosity, env) -> None:
        self.FPS = env.FPS  # Frames per second
        self.dt = env.dt  # Time step
        self.width = env.width  # Width of the simulation area
        self.height = env.height  # Height of the simulation area

        # The size of the fluid area
        self.size = size
        # The diffusion rate of the fluid
        self.diff = diffusion
        # The viscosity of the fluid
        self.visc = viscosity

        self.iter = 4  # The number of iterations for the linear solver

        # Initialize lists to hold various properties of the fluid
        self.s = np.zeros(self.size * self.size)  # Not used in the provided code
        self.density = np.zeros(self.size * self.size)  # The density of the fluid at each point

        # The velocity of the fluid in the x and y directions
        self.Vx = np.zeros(self.size * self.size)
        self.Vy = np.zeros(self.size * self.size)

        # The previous velocity of the fluid in the x and y directions
        self.Vx0 = np.zeros(self.size * self.size)
        self.Vy0 = np.zeros(self.size * self.size)

    # A method to calculate the index in the fluid grid from x and y coordinates
    def IX(self, x, y):
        return x + y * self.size

    # A method to add density to a point in the fluid
    def addDensity(self, x, y, amount):
        index = self.IX(x, y)
        self.density[index] += amount

    # A method to add velocity to a point in the fluid
    def addVelocity(self, x, y, amountX, amountY):
        index = self.IX(x, y)
        self.Vx[index] += amountX
        self.Vy[index] += amountY

    def step(self):
        self.Vx0 = self.diffuse(1, self.Vx0, self.Vx, self.visc, self.dt)
        self.Vy0 = self.diffuse(2, self.Vy0, self.Vy, self.visc, self.dt)

        self.Vx0, self.Vy0 = self.project(self.Vx0, self.Vy0, self.Vx, self.Vy)

        self.Vx = self.advect(1, self.Vx, self.Vx0, self.Vx0, self.Vy0)
        self.Vy = self.advect(2, self.Vy, self.Vy0, self.Vx0, self.Vy0)

        self.Vx, self.Vy = self.project(self.Vx, self.Vy, self.Vx0, self.Vy0)

        self.s = self.diffuse(0, self.s, self.density, self.diff, self.dt)
        self.density = self.advect(0, self.density, self.s, self.Vx, self.Vy)

        print(self.density)
        print('-' * 10)

    # A method to diffuse the fluid, spreading out its density
    def diffuse(self, b, x, x0, diff, dt):
        a = dt * diff * (self.size - 2) * (self.size - 2)
        return self.lin_solve(b, x, x0, a, 1 + 6 * a)

    # A method to solve a linear system of equations, used in the diffusion process
    def lin_solve(self, b, x, x0, a, c):
        recip_c = 1.0 / c
        for k in range(self.iter):
            for i in range(1, self.size - 1):
                for j in range(1, self.size - 1):
                    #print (i, j)
                    x[self.IX(i, j)] = (x0[self.IX(i, j)] + a * (x[self.IX(i + 1, j)] + x[self.IX(i - 1, j)] + x[self.IX(i, j + 1)] + x[self.IX(i, j - 1)])) * recip_c

            x = self.set_bnd(b, x)

        return x

    # A method to set the boundaries of the fluid
    def set_bnd(self, b, x):
        for i in range(1, self.size - 1):
            x[self.IX(i, 0)] = -x[self.IX(i, 1)] if b == 2 else x[self.IX(i, 1)]
            x[self.IX(i, self.size - 1)] = -x[self.IX(i, self.size - 2)] if b == 2 else x[self.IX(i, self.size - 2)]
        
        for j in range(1, self.size - 1):
            x[self.IX(0, j)] = -x[self.IX(1, j)] if b == 1 else x[self.IX(1, j)]
            x[self.IX(self.size - 1, j)] = -x[self.IX(self.size - 2, j)] if b == 1 else x[self.IX(self.size - 2, j)]

        x[self.IX(0, 0)]  = 0.5 * (x[self.IX(1, 0)] + x[self.IX(0, 1)])
        x[self.IX(0, self.size - 1)] = 0.5 * (x[self.IX(1, self.size - 1)] + x[self.IX(0, self.size - 2)])
        x[self.IX(self.size - 1, 0)] = 0.5 * (x[self.IX(self.size - 2, 0)] + x[self.IX(self.size - 1, 1)])
        x[self.IX(self.size - 1, self.size - 1)] = 0.5 * (x[self.IX(self.size - 2, self.size - 1)] + x[self.IX(self.size - 1, self.size - 2)])

        return x

    def project(self, velocX, velocY, p, div):
        for j in range(1, self.size - 1):
            for i in range(1, self.size - 1):
                div[self.IX(i, j)] = -0.5 * (velocX[self.IX(i + 1, j)] - velocX[self.IX(i - 1, j)] + velocY[self.IX(i, j + 1)] - velocY[self.IX(i, j - 1)]) / self.size
                p[self.IX(i, j)] = 0

        div = self.set_bnd(0, div)
        p = self.set_bnd(0, p)
        p = self.lin_solve(0, p, div, 1, 6)

        for j in range(1, self.size - 1):
            for i in range(1, self.size - 1):
                velocX[self.IX(i, j)] -= 0.5 * (p[self.IX(i + 1, j)] - p[self.IX(i - 1, j)]) * self.size
                velocY[self.IX(i, j)] -= 0.5 * (p[self.IX(i, j + 1)] - p[self.IX(i, j - 1)]) * self.size

        velocX = self.set_bnd(1, velocX)
        velocY = self.set_bnd(2, velocY)

        return velocX, velocY

    def advect(self, b, d, d0, velocX, velocY):
        i0, i1, j0, j1 = 0, 0, 0, 0
        dtx = self.dt * (self.size - 2)
        dty = self.dt * (self.size - 2)

        s0, s1, t0, t1 = 0, 0, 0, 0
        tmp1, tmp2, x, y = 0, 0, 0, 0

        i, j = 0, 0

        for j in range(1, self.size - 1):
            for i in range(i, self.size - 1):
                tmp1 = dtx * velocX[self.IX(i, j)]
                tmp2 = dty * velocY[self.IX(i, j)]
                x = i - tmp1
                y = j - tmp2

                if x < 0.5: x = 0.5
                if x > (self.size-2) + 0.5: x = (self.size-2) + 0.5
                i0 = np.floor(x)
                i1 = i0 + 1

                if y < 0.5: y = 0.5
                if y > (self.size-2) + 0.5: y = (self.size-2) + 0.5
                j0 = np.floor(y)
                j1 = j0 + 1

                s1 = x - i0
                s0 = 1 - s1
                t1 = y - j0
                t0 = 1 - t1

                i0i = int(i0)
                i1i = int(i1)
                j0i = int(j0)
                j1i = int(j1)

                d[self.IX(i, j)] = (s0 * (t0 * d0[self.IX(i0i, j0i)] + t1 * d0[self.IX(i0i, j1i)]) +
                                    s1 * (t0 * d0[self.IX(i1i, j0i)] + t1 * d0[self.IX(i1i, j1i)]))
                
                #print (f"d change: {d[self.IX(i, j)] - d0[self.IX(i, j)]}")
                
        d = self.set_bnd(b, d)
        
        return d
