import pygame
import numpy as np

WIDTH, HEIGHT = 1280, 720
FPS = 144

constraint_radius = 200
dt = 1/FPS
SPEED = 3

def pythag(a):
    return np.sqrt(a[0]**2 + a[1]**2)

class Ball():
    def __init__(self, env, pos, vel) -> None:
        self.env = env

        self.pos = pos
        self.vel = vel
        self.accel = np.array([0, 9.8])
        self.radius = 10
        self.mass = 30
        self.color = (255, 255, 255)
        self.add_radius = False

        self.lines = []

    def update(self):
        #self.euler_step()
        self.RK4_step()

        dist_from_center = np.linalg.norm(self.pos - np.array([WIDTH//2, HEIGHT//2]))
        normal_vector = (self.pos - np.array([WIDTH//2, HEIGHT//2])) / dist_from_center

        touching = (dist_from_center + self.radius > constraint_radius)
        touching_next = self.check_next_RK4()

        # if self.add_radius and (self.radius < constraint_radius - 1) and not touching:
        #     print ("adding radius, {}".format(self.env.frame_count))
        #     self.radius += 2
        #     self.add_radius = False

        if touching or touching_next:
            projection = np.dot(self.vel, normal_vector)
            self.vel = self.vel - 2 * projection * normal_vector
            self.pos = self.pos + self.vel * dt * SPEED

            self.lines.append([np.copy(self.pos) + normal_vector * np.array([self.radius, self.radius]), self.random_color()]) #hit point, random color

            self.add_radius = True

    def euler_step(self):
        self.vel = self.vel + self.accel * dt * SPEED
        self.pos = self.pos + self.vel * dt * SPEED

    def check_next_RK4(self):
        k1 = self.accel * dt * SPEED
        k2 = (self.accel + k1/2) * dt * SPEED
        k3 = (self.accel + k2/2) * dt * SPEED
        k4 = (self.accel + k3) * dt * SPEED

        vel = self.vel + (k1 + 2*k2 + 2*k3 + k4) / 6

        p1 = vel * dt * SPEED
        p2 = (vel + k1/2) * dt * SPEED
        p3 = (vel + k2/2) * dt * SPEED
        p4 = (vel + k3) * dt * SPEED

        pos = self.pos + (p1 + 2*p2 + 2*p3 + p4) / 6

        dist_from_center = np.linalg.norm(pos - np.array([WIDTH//2, HEIGHT//2]))
        touching_next = (dist_from_center + self.radius + pythag(vel * dt * SPEED) > constraint_radius)

        return touching_next

    def RK4_step(self):
        k1 = self.accel * dt * SPEED
        k2 = (self.accel + k1/2) * dt * SPEED
        k3 = (self.accel + k2/2) * dt * SPEED
        k4 = (self.accel + k3) * dt * SPEED

        self.vel = self.vel + (k1 + 2*k2 + 2*k3 + k4) / 6

        p1 = self.vel * dt * SPEED
        p2 = (self.vel + k1/2) * dt * SPEED
        p3 = (self.vel + k2/2) * dt * SPEED
        p4 = (self.vel + k3) * dt * SPEED

        self.pos = self.pos + (p1 + 2*p2 + 2*p3 + p4) / 6

        #self.pos = self.pos + self.vel * dt * SPEED

    def random_color(self):
        return (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))

    def draw_lines(self):
        for l in self.lines:
            pygame.draw.line(self.env.WIN, l[1], l[0], self.pos, 2)

    def draw(self):
        pygame.draw.circle(E.WIN, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)

class Environment():
    def __init__(self):
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.BG = (24, 23, 51)
        self.WIN.fill(self.BG)
        
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Ball Bounce")

        self.ball1 = Ball(self, np.array([WIDTH//2 + 1, HEIGHT//2]), np.array([200, -100]))
        self.ball2 = Ball(self, np.array([WIDTH//2 + 1, HEIGHT//2]), np.array([201, -101]))
        self.ball_list = [self.ball1, self.ball2]

        self.frame_count = 0
    
    def checkCollision(self, mass1, mass2):
        response_constant = 0.75

        disp = mass1.pos - mass2.pos
        distsq = disp[0]*disp[0] + disp[1]*disp[1]
        minDist = mass1.radius + mass2.radius

        if distsq < minDist*minDist:
            dist = np.sqrt(distsq)
            dhat = (mass1.pos - mass2.pos) / dist

            mass_ratio_1 = mass1.mass / (mass1.mass + mass2.mass)
            mass_ratio_2 = mass2.mass / (mass1.mass + mass2.mass)
            delta = (minDist - dist) * 0.5 * response_constant

            try:
                mass1.pos += dhat * delta * mass_ratio_2
                mass2.pos -= dhat * delta * mass_ratio_1
            except:
                print ("collision error")

    def update(self):
        self.WIN.fill(self.BG)
        self.clock.tick(FPS)

        self.frame_count += 1

        steps = 3
        for _ in range(steps):
            for b in self.ball_list:
                b.update()
                b.draw()
                b.draw_lines()


        # dist = pythag(self.ball1.pos - self.ball2.pos)
        # if dist < self.ball1.radius + self.ball2.radius:
        #     self.checkCollision(self.ball1, self.ball2)

        self.draw_constraint()

        pygame.display.set_caption("Ball Bounce | FPS: {}".format(round(self.clock.get_fps())))

    def draw_constraint(self):
        pygame.draw.circle(self.WIN, (0, 0, 0), (WIDTH//2, HEIGHT//2), constraint_radius, 3)

E = Environment()

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        E.update()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()