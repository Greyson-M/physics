import numpy as np
import pygame

from Settings import *
from Utils import *

class Rocket():
    def __init__(self, env, length, mass) -> None:
        self.env = env
        self.length = length
        self.mass = mass
        self.camera = self.env.camera

        self.pid_pos = self.PID(self, (np.array((100, HEIGHT/2)) - np.array((0, 100))), 1.2, 1.5, 0.3)
        self.pid_ang = self.PID(self, np.radians(0), 1, 1, 0, False)
        self.controller = self.Controller(self.pid_pos, self.pid_ang)

        self.screen_center = np.array((WIDTH / 2, HEIGHT / 2))
        self.pos = self.screen_center = np.array((100, 0))
        self.vel = np.array((0, 0))
        self.acc = np.array((0, 0))

        self.base = self.pos + np.array((0, self.length/2))
        self.head = self.pos + np.array((0, -self.length/2))

        #self.angle = np.radians(15)
        self.angle = 0
        self.angle_vel = 0
        self.angle_acc = 0

        self.thrust = 0
        self.thrust_acc = 0
        self.thrust_vel = 0

        self.color = BLACK

        self.size = 10

        self.prev_error = 0
        self.signal_total = 0
        self.signal_total_pos = 0
        self.prev_error_pos = 0

        self.error = 0

        self.MAX_THRUST = np.array((20, -1000))
        self.f = np.array((0, 0))

    def rotate(self, point1, point2, targ_point, angle):

        dp1 = point1 - targ_point

        dp2 = point2 - targ_point


        d1rothat = np.array((dp1[0] * np.cos(angle) - dp1[1] * np.sin(angle), dp1[0] * np.sin(angle) + dp1[1] * np.cos(angle)))
        d2rothat = np.array((dp2[0] * np.cos(angle) - dp2[1] * np.sin(angle), dp2[0] * np.sin(angle) + dp2[1] * np.cos(angle)))

        point1 = targ_point + d1rothat
        point2 = targ_point + d2rothat

        return point1, point2
    
    def rotate3(self, point1, point2, point3, targ_point, angle):
            dp1 = point1 - targ_point
            dp2 = point2 - targ_point
            dp3 = point3 - targ_point
    
            d1rothat = np.array((dp1[0] * np.cos(angle) - dp1[1] * np.sin(angle), dp1[0] * np.sin(angle) + dp1[1] * np.cos(angle)))
            d2rothat = np.array((dp2[0] * np.cos(angle) - dp2[1] * np.sin(angle), dp2[0] * np.sin(angle) + dp2[1] * np.cos(angle)))
            d3rothat = np.array((dp3[0] * np.cos(angle) - dp3[1] * np.sin(angle), dp3[0] * np.sin(angle) + dp3[1] * np.cos(angle)))
    
            point1 = targ_point + d1rothat
            point2 = targ_point + d2rothat
            point3 = targ_point + d3rothat
    
            return point1, point2, point3

    def update(self):
        self.thrust_acc = 0
        self.thrust_vel = 0
        self.angle_acc = 0
        self.acc = np.array((0, 9.8))
        if not self.checkControls():
            
          
            target = self.pid_pos.target
            error = target - self.head
            print (target, self.head, error)

            #print (error[1] + self.length)
            if False: #(error[1] + self.length) > 0:      
                angle = -np.arctan(error[0] / (error[1] + self.length))
                #print (np.degrees(angle))
                self.pid_ang.target = angle

                pygame.draw.circle(self.env.WIN, BLACK, (self.head[0] + error[0], self.head[1] + error[1]), 5)


            self.posControl()
            self.angleControl()

            
            

        self.angle_vel += self.angle_acc * dt * SPEED
        self.angle += self.angle_vel * dt * SPEED

        
        self.pid_pos.target[1] += dt * -10 * SPEED

        

        angle_vec = np.array((np.sin(self.angle), np.cos(self.angle)))

        self.vel  = self.vel + self.acc * dt * SPEED# * angle_vec
        self.pos  = self.pos + self.vel * dt * SPEED

        

        self.length_constraint()

        self.draw()

    def length_constraint(self):
        
        self.base = self.pos + np.array((0, self.length/2))
        self.head = self.pos + np.array((0, -self.length/2))

        b, h = self.rotate(self.base, self.head, self.pos, self.angle)

        self.base = b
        self.head = h

        #self.base = self.pos + np.array((0, self.length/2)) + np.array((np.sin(-self.angle), np.cos(-self.angle))) * self.length/2
        #self.head = self.pos + np.array((0, -self.length/2)) + np.array((np.sin(self.angle), np.cos(self.angle))) * self.length/2

    def draw(self):

        self.displayStats()

        pygame.draw.line(self.env.WIN, self.color, self.base - self.camera.offset, self.head - self.camera.offset, 5)
        pygame.draw.circle(self.env.WIN, self.color, self.base - self.camera.offset, 10)
        pygame.draw.circle(self.env.WIN, self.color, self.head - self.camera.offset, 10)
        #truster
        offset = self.camera.offset
        point1 = np.array([self.base[0]+self.size, self.base[1] + self.size])
        point2 = np.array([self.base[0]-self.size, self.base[1] + self.size])

        point1, point2 = self.rotate(point1, point2, self.base, self.angle)

        #exhaust
        e_off = np.sqrt(self.size * self.size + (self.size/2)*(self.size/2))
        if self.f[1] < -1000:
            self.f[1] = -1000
        ep1 = np.array([self.base[0], self.base[1] + self.size * -self.f[1]/100])
        ep2 = np.array([self.base[0] + self.size, self.base[1] + e_off])
        ep3 = np.array([self.base[0] - self.size, self.base[1] + e_off])

        ep1, ep2, ep3 = self.rotate3(ep1, ep2, ep3, self.base, self.angle)

        pygame.draw.polygon(self.env.WIN, self.color, (self.base - offset, point1 - offset, point2 - offset), 2)

        if self.f[1] < -1:
            pygame.draw.polygon(self.env.WIN, ((252, 111, 3)), (ep1 - offset, ep2 - offset, ep3 - offset), 2)

    def displayStats(self):
        offset = self.camera.offset
        font = pygame.font.SysFont("Arial", 12)
        thrust_text = font.render("Trust: " + str(self.thrust), True, BLACK)
        self.env.WIN.blit(thrust_text, (self.base[0] - offset[0], self.base[1] + 20 - offset[1])) 

        text_angle = font.render("Angle: " + str(self.angle), True, BLACK)
        self.env.WIN.blit(text_angle, (self.base[0] - offset[0], self.base[1] + 40 - offset[1]))

        acc_text = font.render("Acc: " + str(self.acc), True, BLACK)
        self.env.WIN.blit(acc_text, (self.base[0] - offset[0], self.base[1] + 60 - offset[1]))

        error_text = font.render("Error: " + str(self.error), True, BLACK)
        self.env.WIN.blit(error_text, (self.base[0] - offset[0], self.base[1] + 80 - offset[1]))

    def applyThrust(self, force):
        if force[1]/self.mass <= self.MAX_THRUST[1]:
            force[1] = self.MAX_THRUST[1]
        elif force[1]/self.mass >= 0:
            force[1] = 0


        angle_vec = np.array((np.sin(-self.angle), np.cos(-self.angle)))
        force = force[1] * angle_vec

        self.acc = self.acc + force/self.mass
        self.f = force


    def applyControl(self, force):
        self.angle_acc += force/self.mass

    def checkControls(self):
        #angle_vec = np.array((np.sin(-self.angle), np.cos(-self.angle)))

        if pygame.key.get_pressed()[pygame.K_UP]:
            self.applyThrust(np.array((0, -100)))
            return True
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.applyThrust(np.array((0, 100)))
            return True
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.applyControl(np.radians(-50))
            return True
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.applyControl(np.radians(50))
            return True
        
        return False

    def angleControl(self):

        f = self.pid_ang.compute(self.angle)
        self.applyControl(f)

        '''
        error = target_ang - self.angle
        derror = (error - self.prev_error)/dt
        #print (error, derror)


        #print (target_ang, self.angle, error)

        kp = 1
        kd = 1
        ki = 0

        self.signal_total += (kp * error + kd * derror) * dt
        print (kp * error , kd * derror , ki * self.signal_total)

        correction = kp * error + kd * derror + ki * self.signal_total
        print (correction)

        self.applyControl(correction)
        self.prev_error = error

        self.env.pdata.append(kp * error)
        self.env.idata.append(ki * self.signal_total)
        self.env.ddata.append(kd * derror)
        self.env.correctiondata.append(correction)
        '''

    def posControl(self):

        f = self.pid_pos.compute(self.head)
        #print (f)
        self.applyThrust(f)

        '''
        error = target_pos - self.pos
        #derror = (error - self.prev_error_pos)/dt
        derror = 0 - self.vel

        kp = 0.5
        kd = 0.5
        ki = 0

        self.signal_total_pos += (kp * error + kd * derror) * dt
        print (kp * error , kd * derror , ki * self.signal_total_pos)

        correction = kp * error + kd * derror + ki * self.signal_total_pos

        self.applyThrust(correction)

        self.prev_error_pos = error

        self.env.pdata.append(kp * error[1])
        self.env.idata.append(ki * self.signal_total_pos[1])
        self.env.ddata.append(kd * derror[1])
        self.env.correctiondata.append(correction[1])
        '''

    class PID():
        def __init__(self, rocket, target, kp, kd, ki, draw=True) -> None:
            self.rocket = rocket
            self.env = rocket.env
            self.draw = draw

            ku = 0.5
            period = 0.017 #seconds
            KP = 0.6 * ku
            KI = 1.2 * ku / period
            KD = 3 * ku * period / 40

            print (KP, KI, KD)


            self.kp = kp     # propotional gain
            self.kd = kd     # derivative gain
            self.ki = ki    # integral gain



            self.target = target
            self.prev_error = 0

            self.error = np.array((0, 0))
            self.derror = 0
            self.ierror = 0

            self.correction = 0

        def compute(self, current):
            self.error = self.target - current
            self.rocket.error = self.error
            self.ierror += self.error * dt
            self.derror = (self.error - self.prev_error)/dt
            self.prev_error = self.error

            self.correction = self.kp * self.error + self.kd * self.derror + self.ki * self.ierror
           

            if not self.draw:
                self.draw_desired()

                if type(self.error) == np.ndarray:
                    self.env.pdata.append(self.kp * self.error[1])
                    self.env.idata.append(self.ki * self.ierror[1])
                    self.env.ddata.append(self.kd * self.derror[1])
                    self.env.correctiondata.append(self.correction[1])

                else:
                    self.env.pdata.append(self.kp * self.error)
                    self.env.idata.append(self.ki * self.ierror)
                    self.env.ddata.append(self.kd * self.derror)
                    self.env.correctiondata.append(self.correction)

            return self.correction * self.rocket.mass
        
        def draw_desired(self):
            pygame.draw.line(self.env.WIN, ((180, 0, 50)), self.target - self.env.camera.offset + np.array((-20, 0)), self.target - self.env.camera.offset + np.array((20, 0)), 2)


    class Controller():
        def __init__(self, pos_pid, ang_pid) -> None:
            
            self.pos_pid = pos_pid
            self.ang_pid = ang_pid

        def compute_pos(self, pos_curr, ang_curr):
            correction = self.pos_pid.compute(pos_curr)
            error = self.pos_pid.error
            angle = np.atan2(error[0], error[1])

            self.ang_pid.target = angle
            ang_correction = self.compute_ang(ang_curr)

            return correction, ang_correction

        def compute_ang(self, angle):
            correction = self.ang_pid.compute(angle)
            return correction

