import numpy as np
import pygame

class Camera():
    def __init__(self, env, solver, scale=1) -> None:
        self.env = env
        self.solver = solver
        self.scale = scale
        self.target = self.solver.get_center_of_mass()
        self.zoom = 1



        # offset = target - self.env.CENTER
        # adj_pos = [pos * self.scale + offset for pos in self.solver.positions]
        # self.start_COM = self.get_adj_center_of_mass(adj_pos, self.solver.masses)

    def update(self):
        min_x = np.min(self.solver.positions[:, 0])
        max_x = np.max(self.solver.positions[:, 0])
        min_y = np.min(self.solver.positions[:, 1])
        max_y = np.max(self.solver.positions[:, 1])

        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        self.target = np.array([center_x, center_y])

        size_x = max_x - min_x
        size_y = max_y - min_y
        self.zoom = max(size_x / self.env.WIDTH, size_y / self.env.HEIGHT, 1) * 1  # Add 0% padding
        self.zoom = min(self.zoom, 5)
        print ("Zoom: ", self.zoom)

        adj_pos = np.array([pos - self.target for pos in self.solver.positions]) / self.zoom + self.env.CENTER
        self.draw_bodies(adj_pos)

    def draw_bodies(self, adj_pos):
        for pos in adj_pos:
            pygame.draw.circle(self.env.WIN, (255, 255, 255), pos, 5/self.zoom)


    # def update(self):
    #     #do not need to transpose the positions since the center of mass, the target, is already at the center of the screen
    #     #only need to zoom out to keep all bodies in view

    #     print (self.solver.positions)

    #     # xs = [pos[0] for pos in self.solver.positions]
    #     # ys = [pos[1] for pos in self.solver.positions]
        
    #     # xdiff = max(xs) - min(xs)
    #     # ydiff = max(ys) - min(ys)

    #     xdiff = np.max(self.solver.positions[:, 0]) - np.min(self.solver.positions[:, 0])
    #     ydiff = np.max(self.solver.positions[:, 1]) - np.min(self.solver.positions[:, 1])

    #     self.scale = min(self.env.WIDTH / xdiff, self.env.HEIGHT / ydiff)

    #     # if xdiff > ydiff:
    #     #     self.scale = self.env.WIDTH / xdiff
    #     # else:
    #     #     self.scale = self.env.HEIGHT / ydiff

    #     adj_radius = 5 * self.scale
    #     adj_pos = self.solver.positions * self.scale

    #     self.draw_bodies(adj_pos, adj_radius)
    #     self.draw_center_of_mass(adj_pos)

    # def draw_bodies(self, adj_pos, adj_radius):
    #     for pos in adj_pos:
    #         pygame.draw.circle(self.env.WIN, (255, 255, 255), pos, adj_radius)

    # def draw_center_of_mass(self, adj_pos):
    #     com = self.get_adj_center_of_mass(adj_pos, self.solver.masses)
    #     pygame.draw.circle(self.env.WIN, (0, 255, 0), com, 2)
    #     # pygame.draw.circle(self.env.WIN, (0, 0, 255), self.start_COM, 2)
    #     # pygame.draw.line(self.env.WIN, (0, 255, 0), com, self.start_COM, 1)

    # def get_adj_center_of_mass(self, adj_pos, mass):
    #     return np.sum([adj_pos[i] * mass[i] for i in range(self.solver.n)], axis=0) / np.sum(mass)


    # def update(self):
    #     target = self.solver.get_center_of_mass()
        
    #     offset = target - self.env.CENTER
    #     adj_pos = [pos * self.scale + offset for pos in self.solver.positions]

    #     self.env.CENTER = target

    #     bodies = self.solver.positions

    #     #zoom to show all bodies
    #     xs = [pos[0] for pos in bodies]
    #     ys = [pos[1] for pos in bodies]
    #     x_diff = max(xs) - min(xs)
    #     y_diff = max(ys) - min(ys)

    #     if (x_diff )
    #     if x_diff > y_diff:
    #         self.scale = self.env.WIDTH / x_diff
    #     else:
    #         self.scale = self.env.HEIGHT / y_diff

    #     self.solver.radius = 5 * self.scale


    #     self.draw_bodies(adj_pos)
    #     self.draw_center_of_mass(adj_pos)

    # def draw_bodies(self, adj_pos):
    #     for pos in adj_pos:
    #         pygame.draw.circle(self.env.WIN, (255, 255, 255), pos, self.solver.radius)

    # def get_adj_center_of_mass(self, adj_pos, mass):
    #     return np.sum([adj_pos[i] * mass[i] for i in range(self.solver.n)], axis=0) / np.sum(mass)
        

    # def draw_center_of_mass(self, adj_pos):
    #     com = self.get_adj_center_of_mass(adj_pos, self.solver.masses)
    #     pygame.draw.circle(self.env.WIN, (255, 0, 0), com, 2)
    #     pygame.draw.circle(self.env.WIN, (0, 0, 255), self.start_COM, 2)
    #     pygame.draw.line(self.env.WIN, (0, 255, 0), com, self.start_COM, 1)




    