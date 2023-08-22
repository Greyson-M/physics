from Mass import Mass
import pygame
import numpy as np

class Environment():
    def __init__(self) -> None:
        self.FPS = 144
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0 , 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.BG_COLOR = (217, 217, 217)
        self.dt = 1/120
        self.g = 9.81

        pygame.init()
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.WIN.fill(self.BG_COLOR)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Particle Simulation")

        self.sysfont = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(None, 18)

        self.massList = []

        self.totalEnergy = 0
        self.E_disp = 0

        self.frame_count = 0
    
    def attract(self, mass):
        atrraction_constant = 0.01

        center_dist = np.array([self.WIDTH/2, self.HEIGHT/2]) - mass.pos
        mass.addVelocity(center_dist * atrraction_constant)

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

            mass1.pos += dhat * delta * mass_ratio_2
            mass2.pos -= dhat * delta * mass_ratio_1

    def displayText(self, text, pos):
        text = self.font.render(text, True, self.BLACK)
        self.WIN.blit(text, pos)

    def update(self):
        self.WIN.fill(self.BG_COLOR)
        self.clock.tick(self.FPS)

        self.frame_count += 1

        self.totalEnergy = 0

        for mass in self.massList:
            self.attract(mass)

            for otherMass in self.massList:
                if mass != otherMass:
                    self.checkCollision(mass, otherMass)

            mass.update()

            self.totalEnergy += mass.kinetic_energy

        if self.frame_count % 20 == 0:
            self.E_disp = self.totalEnergy

        self.displayText("Total Energy: " + str(round(self.E_disp)), (10, 10))

        pygame.display.update()
        pygame.display.set_caption("Particle Simulation: " + str(round(self.clock.get_fps())) + " FPS")
        
    def addMass(self, env, radius, mass, pos, color=(0, 0, 0)):
        self.massList.append(Mass(env, radius, mass, pos, color))