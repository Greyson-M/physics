import pygame
from Settings import *
from Grid import Grid
from Utils import *
import numpy as np
from Camera import Camera
from Slider import Slider


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

        self.camera = Camera(self)
        self.Grid = Grid(self, 20)

        self.t = 0
        
        self.massList = []

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

        for m in self.massList:
            m.update()

        self.Grid.draw()
        self.camera.update()
       
        #pos display
        text = self.font.render("Pos: " + str(self.camera.target.pos), True, BLACK)
        self.WIN.blit(text, (10, 10))

        pygame.display.update()


    def addMass(self, mass):
        self.camera.target = mass
        self.massList.append(mass)

        

        