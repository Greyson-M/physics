import pygame

from Field import Field

class Environment():
    def __init__(self) -> None:
        pygame.init()
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.fps = 144
        self.drawGrid = True

        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.WIN.fill((217, 217, 217))
        pygame.display.set_caption("Vector Field Visualization")

        self.clock = pygame.time.Clock()

        self.sysfont = pygame.font.SysFont("Arial", 20)
        self.font = pygame.font.Font("freesansbold.ttf", 20)

        self.dt = 1/self.fps

        self.vector_list = []
        self.mass_list = []
        self.field = Field(self, 50)

        self.heldMass = None

    def update(self):
        self.clock.tick(self.fps)
        self.WIN.fill((217, 217, 217))

        self.field.update()
        self.field.draw()

        for mass in self.mass_list:
            mass.update()
            mass.draw()

        pygame.display.update()

    def add_vector(self, vector):
        self.vector_list.append(vector)

    def add_mass(self, mass):
        self.mass_list.append(mass)
