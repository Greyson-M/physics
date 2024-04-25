import numpy as np
import pygame

from Settings import *
from Utils import *

class Rocket2():
    def __init__(self, env, length, mass) -> None:
        self.env = env
        self.length = length
        self.mass = mass
        self.camera = self.env.camera
        self.color = BLACK

        self.screen_center = (WIDTH/2, HEIGHT/2)
        
        self.pos = self.screen_center + np.array((0, 200))
        self.vel = np.array((0, 0))
        self.acc = np.array((0, 0))

        self.mass_center = self.pos

        self.angle = 0
        self.angle_vel = 0
        self.angle_acc = 0

        self.thruster_angle = 0
        self.moment_of_inertia = 50000

        self.base = self.pos + np.array((0, self.length/2))
        self.head = self.pos + np.array((0, -self.length/2))

        self.thruster_size = 10
        self.max_thrust = np.array((0, -600))
        self.terminal_velocity = 80

        self.gravity = np.array((0, g))

        self.f = np.array((0, 0))

        self.controller = self.Controller(self, self.screen_center)


    def rotate(self, points, targ_point, angle):
        new_points = []
        for point in points:
            dp = point - targ_point
            drot = np.array((dp[0] * np.cos(angle) - dp[1] * np.sin(angle), dp[0] * np.sin(angle) + dp[1] * np.cos(angle)))
            new_points.append(targ_point + drot)

        return new_points
        
    def length_constraint(self):
        self.mass_center = self.pos
        
        self.base = self.pos + np.array((0, self.length/2))
        self.head = self.pos + np.array((0, -self.length/2))

        b, h = self.rotate([self.base, self.head], self.pos, self.angle)

        self.base = b
        self.head = h

    def resolve_torque(self, force):
        
        force_pos = self.base

        torque = np.cross(force_pos - self.mass_center, force)
        #print (torque)
        self.angle_acc = torque / self.moment_of_inertia

    def apply_force(self, force):
        #print ("Force: {}".format(force))

        if force[1]/self.mass <= self.max_thrust[1]:
            force[1] = self.max_thrust[1]
        elif force[1]/self.mass >= 0:
            force[1] = 0

        force = np.array([0, force[1]])
        ang_vec_thrust = np.array((np.sin(self.thruster_angle), np.cos(self.thruster_angle)))
        self.resolve_torque(force[1] * ang_vec_thrust)

        ang_vec = np.array((np.sin(self.angle), np.cos(self.angle)))


        self.f = force[1] * ang_vec

        self.acc = self.gravity + (self.f / self.mass)

    def update(self):
        self.f = np.array((0, 0))
        #self.acc = self.gravity
        self.acc = np.array((0, 0))
        self.angle_acc = 0

        self.checkControls()
        self.controller.update(self.head, self.angle)
        

        self.angle_vel += self.angle_acc * dt
        self.angle += self.angle_vel * dt

        self.vel = self.vel + self.acc * dt * SPEED
        self.pos = self.pos + self.vel * dt * SPEED

        self.length_constraint()

        self.draw()

    def displayStats(self):
        offset = self.camera.offset
        font = pygame.font.SysFont("Arial", 12)

        thrust_angle_text = font.render("Thrust Angle: " + str(np.degrees(self.thruster_angle)), True, BLACK)
        self.env.WIN.blit(thrust_angle_text, (self.base[0] - offset[0], self.base[1] + 30 - offset[1]))

        text_angle = font.render("Angle: " + str(np.degrees(self.angle)), True, BLACK)
        self.env.WIN.blit(text_angle, (self.base[0] - offset[0], self.base[1] + 40 - offset[1]))

        acc_text = font.render("Acc: " + str(self.acc), True, BLACK)
        self.env.WIN.blit(acc_text, (self.base[0] - offset[0], self.base[1] + 60 - offset[1]))

        vel_text = font.render("Vel: " + str(self.vel), True, BLACK)
        self.env.WIN.blit(vel_text, (100, 100))

    def draw(self):
        self.displayStats()

        pygame.draw.line(self.env.WIN, self.color, self.base - self.camera.offset, self.head - self.camera.offset, 5)
        pygame.draw.circle(self.env.WIN, self.color, self.base - self.camera.offset, 10)
        pygame.draw.circle(self.env.WIN, self.color, self.head - self.camera.offset, 10)
        #truster
        offset = self.camera.offset
        point1 = np.array([self.base[0]+self.thruster_size, self.base[1] + self.thruster_size])
        point2 = np.array([self.base[0]-self.thruster_size, self.base[1] + self.thruster_size])

        point1, point2 = self.rotate([point1, point2], self.base, self.angle + self.thruster_angle)

        #exhaust
        e_off = np.sqrt(self.thruster_size * self.thruster_size + (self.thruster_size/2)*(self.thruster_size/2))
        if self.f[1] < -1000:
            self.f[1] = -1000
        ep1 = np.array([self.base[0], self.base[1] + self.thruster_size * -self.f[1]/100])
        ep2 = np.array([self.base[0] + self.thruster_size, self.base[1] + e_off])
        ep3 = np.array([self.base[0] - self.thruster_size, self.base[1] + e_off])

        ep1, ep2, ep3 = self.rotate([ep1, ep2, ep3], self.base, self.angle + self.thruster_angle)

        pygame.draw.polygon(self.env.WIN, self.color, (self.base - offset, point1 - offset, point2 - offset), 2)

        if self.f[1] < -1:
            pygame.draw.polygon(self.env.WIN, ((252, 111, 3)), (ep1 - offset, ep2 - offset, ep3 - offset), 2)

    def addThrustAngle(self, angle):
        self.thruster_angle += angle
        

    def checkControls(self):

        if pygame.key.get_pressed()[pygame.K_UP]:
            self.apply_force(np.array((0, -1000)))
            return True
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.apply_force(np.array((0, 0)))
            return True
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.addThrustAngle(np.radians(-0.001))
            return True
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.addThrustAngle(np.radians(0.001))
            return True
        
        return False
    
    class Controller():
        def __init__(self, rocket, target_pos) -> None:
            self.rocket = rocket
            self.target_pos = target_pos
            self.env = rocket.env

            ku = 1.3
            frames = 140
            tu = (140 * dt)/FPS
            kp = 0.6 * ku
            ki = 2 * kp / tu
            kd = kp * tu / 8

            self.KP_pos = kp
            self.KI_pos = 0
            self.KD_pos = 1

            self.KP_ang = 1
            self.KI_ang = 1
            self.KD_ang = 1

            self.last_error_pos = np.array((0, 0))
            self.last_error_ang = 0

            self.error_pos = np.array((0, 0))
            self.error_ang = 0
            self.derror_pos = np.array((0, 0))
            self.derror_ang = 0


            self.integral_pos = np.array((0, 0))
            self.integral_ang = 0

            self.thrusting = False

        def draw_target(self):
            pygame.draw.line(self.rocket.env.WIN, BLACK, self.target_pos - self.rocket.camera.offset + np.array((-10, 0)),
                              self.target_pos - self.rocket.camera.offset + np.array((10, 0)), 2)
            
        def displayStats(self):
            error_text = self.env.font_small.render("Error: " + str(self.target_pos - self.rocket.pos), True, BLACK)
            self.env.WIN.blit(error_text, (self.target_pos[0] - self.rocket.camera.offset[0], self.target_pos[1] - self.rocket.camera.offset[1] + 20))

        def update(self, current_pos, current_ang):
            self.draw_target()
            self.displayStats()
            #self.pos_compute(current_pos)
            self.ang_compute()

        def add_grapg_data(self, error, derror, ierror, correction):
            self.env.pdata_pos.append(error[1] * self.KP_pos)
            self.env.ddata_pos.append(derror[1] * self.KD_pos)
            self.env.idata_pos.append(ierror[1] * self.KI_pos)
            self.env.correctiondata_pos.append(correction[1])

        def pos_compute(self, current):
            self.error = self.target_pos - current
            self.integral_pos = self.integral_pos + self.error * dt
            if pythag(self.error - self.last_error_pos) > 1000:
                self.derror_pos = np.array((0, 0))
                print("deriv errro")
            else:
                self.derror_pos = (self.error - self.last_error_pos) / dt

            self.last_error_pos = self.error

            correction = self.KP_pos * self.error + self.KI_pos * self.integral_pos + self.KD_pos * self.derror_pos

            self.rocket.apply_force(correction * self.rocket.mass)
            self.add_grapg_data(self.error, self.derror_pos, self.integral_pos, correction)

        def ang_compute(self):
            #target_ang = np.arctan2(self.target_pos[0] - self.rocket.pos[0], self.target_pos[1] - self.rocket.pos[1])
            #print (target_ang)
            target_ang = np.radians(45)
            error = target_ang - self.rocket.angle
            self.integral_ang += error * dt
            derivative = (error - self.last_error_ang) / dt

            self.last_error_ang = error

            correction = self.KP_ang * error + self.KI_ang * self.integral_ang + self.KD_ang * derivative
            
            self.rocket.addThrustAngle(correction)
            if not self.thrusting:
                self.rocket.apply_force(np.array((0, -1000)))
                


