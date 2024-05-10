import numpy as np
import pygame

class Solver():
    def __init__(self, env, positions, vels, masses) -> None:
        self.G = 1 #6.67408e-11
        self.n = len(positions)
        print (self.n)
        self.env = env

        self.positions = positions
        self.vels = [np.array(vel) for vel in vels]
        self.masses = masses

        self.tracer_length = 100

        self.pos_hist = [[] for _ in positions]
        self.start_center_of_mass = self.get_center_of_mass()

        self.t = 0
        self.radius = 5

    def solve_next(self):
        accelerations = [np.array([0, 0]) for _ in self.positions]

        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    r = np.linalg.norm(self.positions[i] - self.positions[j])

                    #update accelerations
                    accelerations[i] = ( accelerations[i] +
                                       (-self.G * self.masses[j] * (self.positions[i] - self.positions[j]) / pow(r, 3)))

            # #update positions and velocities
            # self.vels[i] = self.vels[i] + accelerations[i]*self.env.dt
            # self.positions[i] = self.positions[i] + self.vels[i]*self.env.dt
            

            # #tracer code
            # if round(self.t / (self.env.dt*self.env.freq)) % 4 == 0:
            #     #print ("appending", self.t)
            #     self.pos_hist[i].append(self.positions[i])

            # if len(self.pos_hist[i]) > self.tracer_length:
            #     # pass
            #     self.pos_hist[i].pop(0)

        for i in range(self.n):
            self.vels[i] = self.vels[i] + accelerations[i]*self.env.dt
            self.positions[i] = self.positions[i] + self.vels[i]*self.env.dt
            

            #tracer code
            if round(self.t / (self.env.dt*self.env.freq)) % 4 == 0:
                #print ("appending", self.t)
                self.pos_hist[i].append(self.positions[i])

            if len(self.pos_hist[i]) > self.tracer_length:
                #pass
                self.pos_hist[i].pop(0)


        self.t += self.env.dt

        #print (self.pos1, self.pos2, self.pos3)

    def draw(self):
        for i in range(self.n):
            pygame.draw.circle(self.env.WIN, (255, 255, 255), self.positions[i], self.radius)

    # def is_out_of_bounds(self, pos):
    #     return pos[0] > self.env.WIDTH or pos[0] < 0 or pos[1] > self.env.HEIGHT or pos[1] < 0
    
    def get_center_of_mass(self):
        return np.sum([self.positions[i] * self.masses[i] for i in range(self.n)], axis=0) / np.sum(self.masses)
        

    def draw_center_of_mass(self):
        com = self.get_center_of_mass()
        pygame.draw.circle(self.env.WIN, (255, 0, 0), com, 5)
        pygame.draw.line(self.env.WIN, (0, 255, 0), com, self.start_center_of_mass, 1)


    def draw_tracer(self):
        for i in range(self.n):
            for j in range(len(self.pos_hist[i])):
                #print (self.pos_hist[i][j])
                pygame.draw.circle(self.env.WIN, (255, 255, 255), self.pos_hist[i][j], 1)