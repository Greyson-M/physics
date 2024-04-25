import numpy as np
import pygame

pygame.init()
WIDTH = 1280
HEIGHT = 720
fps = 144
drawGrid = True

dt = 1/fps

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN.fill((217, 217, 217))
pygame.display.set_caption("Beam Visualization")

clock = pygame.time.Clock()

sysfont = pygame.font.SysFont("Arial", 20)
font = pygame.font.Font("freesansbold.ttf", 20)

BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Load():
    def __init__(self, x, y, mass) -> None:
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        if pygame.mouse.get_pressed()[0]:
            self.x, self.y = pygame.mouse.get_pos()

        pygame.draw.rect(WIN, RED, (self.x, self.y, 5, -40))

class Segment():
    def __init__(self, x, y, width) -> None:
        self.x = x
        self.y = y
        self.width = width

        self.color = BLACK

    def draw(self):
        #print(self.x, self.y, self.width)
        pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, 5))


class Beam:
    def __init__(self, x, y, color, segs, width):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = 12
        
        self.EI = 4 * pow(10, 12)

        self.seg_width = self.width / segs
        
        self.segments = []
        for i in range(segs):
            self.segments.append(Segment(self.x + i * self.seg_width, self.y, self.seg_width))




    def draw(self):
        for s in self.segments:
            s.draw()

        self.drawSupports()

    def drawSupports(self):
        #pygame.draw.rect(WIN, BLACK, (self.x - 10, self.y - 10, 20, 20))
        pygame.draw.rect(WIN, BLACK, (self.x + self.width - 10, self.y - 10, 20, 20))

    def update(self, solver):
        for i in range(len(self.segments)):
            #print (solver.solveDeflection(self.segments[i].x))
            self.segments[i].y = self.y + solver.solveDeflection(self.segments[i].x - (self.x+self.width))

class Solver():
    def __init__(self, env) -> None:
        self.beam = env.B1
        self.load = env.L1

        self.EI = self.beam.EI

  
    def solveDeflection(self, x):
        if self.load.x > self.beam.x + self.beam.width:
            return 0

        dist = x - self.load.x

        moment = -self.load.mass * dist
        #deflection = moment * (-x**3 + 3*dist**2*x - 2*dist**3)/(6*self.EI)
        #deflection = (-moment * x**3) /(6*self.EI)
        deflection = (-moment * dist**3 + 3*self.beam.width**2 * dist + 2*self.beam.width) /(6*self.EI)
        return deflection
        

class Environment():
    def __init__(self) -> None:
        self.B1 = Beam(200, 360, BLACK, 300, 600)
        self.L1 = Load(790, self.B1.y, 1000)

        self.solver = Solver(self)

    def update(self):
        self.B1.draw()
        self.L1.draw()
        self.B1.update(self.solver)


def main():
    run = True
    env = Environment()
    while run:
              
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False


        WIN.fill((217, 217, 217))
        clock.tick(fps)
        
        env.update()


        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()