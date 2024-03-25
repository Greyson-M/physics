import pygame
import numpy as np

class Gon:
    def __init__(self, env, pos, points = [(-5, 5), (5, 5), (5, -5), (-5, -5)], vel=np.array([0, 0]), mass = 10):
        self.env = env
        #self.pos = pos
        self.vel = vel
        self.g = 0
        self.acc = np.array([0, self.g])

        self.angle = np.deg2rad(0)
        self.angle_vel = np.deg2rad(0)
        self.angle_acc = 0
        self.last_angle = 0

        self.mass = mass

        self.count = 0
        self.last_center = pos

        self.points = []
        for p in points:
            self.points.append(pos + np.array(p))

        #bounding circle
        self.radius = 0
        for p in self.points:
            dist = np.linalg.norm(p - pos)
            if dist > self.radius:
                self.radius = dist


       #self.updates = 0
        
        self.scale(3)
        self.next_points = np.copy(self.points)

    def display(self):
        #display velocity on the screen
        text = self.env.font.render(str(self.vel), 1, (10, 10, 10))
        self.env.WIN.blit(text, self.points[0])


    def draw(self):
        self.display()
        pygame.draw.polygon(self.env.WIN, (0, 0, 0), self.points, 1)

    def scale(self, s):
        # Compute the center of the polygon
        center = np.mean(self.points, axis=0)

        # Translate points to origin
        self.points = [p - center for p in self.points]

        for i in range(len(self.points)):
            self.points[i] = self.points[i] * s

        # Translate points back
        self.points = [p + center for p in self.points]

        #bounding circle
        self.radius = 0
        for p in self.points:
            dist = np.linalg.norm(p - center)
            if dist > self.radius:
                self.radius = dist

    def apply_rotation(self):
        ang = self.angle - self.last_angle
        self.last_angle = self.angle

        # Compute the center of the polygon
        center = np.mean(self.points, axis=0)

        # Translate points to origin
        self.points = [p - center for p in self.points]

        # Apply rotation
        for i in range(len(self.points)):
            x = self.points[i][0]
            y = self.points[i][1]
            self.points[i][0] = x * np.cos(ang) - y * np.sin(ang)
            self.points[i][1] = x * np.sin(ang) + y * np.cos(ang)

        # Translate points back
        self.points = [p + center for p in self.points]

    def move(self, x, y):
        self.points = [p + np.array([x, y]) for p in self.points]

    def check_boundary(self):
        # Compute the center of the polygon
        center = np.mean(self.points, axis=0)

        restitution = 0  # Set a restitution coefficient
        dampening = 0.5  # Set a dampening coefficient

        wall = False
        floor = False
        points_hit = 0
        point_hit = 0
        total_impulse = np.array([0, 0])

        for i, p in enumerate(self.points):
            if p[0] > self.env.WIDTH or p[0] < 0:
                wall = True
                point_hit = p
                points_hit+=1

                # Compute the relative velocity of the point
                r = p - center
                relative_vel = self.vel + self.angle_vel * np.array([-r[1], r[0]])

                # Compute the impulse
                impulse = -2 * relative_vel[0] * np.array([1, 0])
                total_impulse = np.add(total_impulse, impulse)

                # Apply the impulse
                # self.angle_vel += -(impulse[0] * r[1] - impulse[1] * r[0]) / (self.mass * np.linalg.norm(r)**2)


            if p[1] > self.env.HEIGHT or p[1] < 0:
                floor = True
                point_hit = p
                points_hit+=1

                # Compute the relative velocity of the point
                r = p - center
                relative_vel = self.vel + self.angle_vel * np.array([-r[1], r[0]])

                # Compute the impulse
                impulse = -2 * relative_vel[1] * np.array([0, 1])
                total_impulse = np.add(total_impulse, impulse)

                # Apply the impulse
               # self.angle_vel += dampening * -(impulse[0] * r[1] - impulse[1] * r[0]) / (self.mass * np.linalg.norm(r)**2)

                

        if points_hit > 0:
            if floor:
                # Reflect the y-component of the velocity
                self.vel[1] *= -1
                # Apply the restitution force
                self.vel += restitution * np.array([0, -np.sign(self.vel[1])])

            if wall:
                # Reflect the x-component of the velocity
                self.vel[0] *= -1
                # Apply the restitution force
                self.vel += restitution * np.array([-np.sign(self.vel[0]), 0])

            avg_impulse = total_impulse / points_hit
            r_avg = np.mean([p-center for p in self.points if (p[0] > self.env.WIDTH or p[0] < 0) or (p[1] > self.env.HEIGHT or p[1] < 0)], axis=0)
            inertia = np.linalg.norm(r_avg)**2 * self.mass
            self.angle_vel += dampening * -(avg_impulse[0] * r_avg[1] - avg_impulse[1] * r_avg[0]) / inertia

        for p in self.points:
            if floor:
                #print (points_hit)
                if center[1] < self.env.HEIGHT / 2:
                    print ("hit ceiling")
                    pass
                else:
                    #print ("floor")
                    delta = self.env.HEIGHT - point_hit[1]
                    self.points = [p + np.array([0, delta]) for p in self.points]


    def lin_interp(self):
        vel = self.vel + self.acc * self.env.dt
        acc = np.array([0, 9.8])

        for i in range(len(self.points)):
            self.next_points[i] = self.points[i] + vel * self.env.dt

    def update(self):
        self.vel = self.vel + self.acc * self.env.dt
        self.acc = np.array([0, self.g])

        mouse_pos = np.array(pygame.mouse.get_pos())

        center = np.mean(self.points, axis=0)
        #pygame.draw.circle(self.env.WIN, (0, 0, 0), (int(center[0]), int(center[1])), self.radius, 1)
        for i in range(len(self.points)):       
            self.points[i] = self.points[i] + self.vel * self.env.dt

        self.count += 1
        if self.count == 5:
            self.count = 1
            self.last_center = center
        

        if self.env.click:
            #print ("click")
            if np.linalg.norm(mouse_pos - center) < self.radius:
                #print("dragging")
                new_center = mouse_pos
                self.points = [p - center for p in self.points]
                self.points = [p + new_center for p in self.points]
                self.vel = np.array([0, 0])
                self.angle_vel = 0
                self.angle = 0
                #self.vel = center - self.last_center / self.count


        self.angle_vel = self.angle_vel + self.angle_acc * self.env.dt

        self.angle_acc = 0
        self.angle = self.angle + self.angle_vel * self.env.dt

        self.apply_rotation()
        self.lin_interp()
        self.check_boundary()
        

