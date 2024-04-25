import pygame
from Settings import *
from Grid import Grid
from Utils import *
import numpy as np
from Camera import Camera
from Slider import Slider

class TriangleTest():
    def __init__(self, env) -> None:
        
        self.environment = env
        self.pos = np.array((600, 400))
        self.size = 30
        self.color = BLACK
        
        self.angle = 0

        self.point1 = np.array([self.pos[0]+self.size, self.pos[1] - self.size])
        self.point2 = np.array([self.pos[0]+self.size, self.pos[1] + self.size])
        self.point3 = np.array([self.pos[0]-self.size, self.pos[1] - self.size])
        self.point4 = np.array([self.pos[0]-self.size, self.pos[1] + self.size])

    def draw(self):
        pygame.draw.polygon(self.environment.WIN, self.color, (self.pos, self.point1, self.point2), 2)
        #pygame.draw.polygon(self.environment.WIN, self.color, (self.pos, self.point3, self.point4), 2)

    def rotate(self, angle):
        dp1 = self.point1 - self.pos
        dp1hat = (dp1 / pythag(dp1))
        dp1mag = pythag(dp1)
        dp2 = self.point2 - self.pos
        dp2hat = (dp2 / pythag(dp2))
        dp2mag = pythag(dp2)

        d1rothat = np.array((dp1hat[0] * np.cos(angle) - dp1hat[1] * np.sin(angle), dp1hat[0] * np.sin(angle) + dp1hat[1] * np.cos(angle)))
        d2rothat = np.array((dp2hat[0] * np.cos(angle) - dp2hat[1] * np.sin(angle), dp2hat[0] * np.sin(angle) + dp2hat[1] * np.cos(angle)))

        self.point1 = self.pos + d1rothat * dp1mag
        self.point2 = self.pos + d2rothat * dp2mag


        #dp3 = self.point3 - self.pos
        #dp4 = self.point4 - self.pos

class Environment():
    def __init__(self):
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.WIN.fill((217, 217, 217))
        self.BG_COLOR = (217, 217, 217)

        

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Rocket Simulation")


        self.sysfont = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(None, 18)

        self.massList = []
        self.constraintList = []
        self.thrusterList = []
        self.systemList = []

        self.camera = Camera(self)

        self.Grid = Grid(self, 20)

        self.t = 0
        
        self.camera.initialize()

        self.pdata_ang = []
        self.idata_ang = []
        self.ddata_ang = []
        self.correctiondata_ang = []

        self.pdata_pos = []
        self.idata_pos = []
        self.ddata_pos = []
        self.correctiondata_pos = []

        self.frame_count = 0
        self.frames = []

        self.font_small = pygame.font.SysFont(None, 15)

        self.KP_slider = Slider(self, (150, 50), (200, 20), 0.05, 0, 10, "KP", 3)
        self.KI_slider = Slider(self, (150, 100), (200, 20), 0.07, 0, 10, "KI", 3)
        self.KD_slider = Slider(self, (150, 150), (200, 20), 0.1, 0, 10, "KD", 3)
        self.sliders = [self.KP_slider, self.KI_slider, self.KD_slider]



    def update(self):

        pygame.display.set_caption("Rocket Simulation - " + str(int(self.clock.get_fps())) + " FPS")

        self.t += dt

        self.WIN.fill(self.BG_COLOR)
        self.clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for s in self.sliders:
            s.draw()

        for c in self.constraintList:
            c.update()

        for m in self.massList:
            m.update()

        for t in self.thrusterList:
            t.update()

        self.Grid.draw()
        self.camera.update()
        #self.triangle.draw()
        #self.triangle.rotate(0.1)

        #pos display
        text = self.font.render("Pos: " + str(self.camera.target.pos), True, BLACK)
        self.WIN.blit(text, (10, 10))

        pygame.display.update()


    def addMass(self, mass):
        self.camera.target = mass
        self.massList.append(mass)

    def addConstraint(self, constraint):
        self.constraintList.append(constraint)

    def addThruster(self, thruster):
        self.thrusterList.append(thruster)

    def addSystem(self, system):
        self.systemList.append(system)

        

        