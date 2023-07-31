import numpy as np
from spring import Spring
from settings import *
import pygame
from Utils import *
from pytmx.util_pygame import load_pygame
from grid import Grid

class Environment():
    def __init__(self):
        #load
        pygame.init()
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.WIN.fill((217, 217, 217))

        self.sysfont = pygame.font.get_default_font()
        self.font = pygame.font.SysFont(None, 18)

        self.blockList = []
        self.rectList = []

        self.heldBlock = None
        self.heldPuck = None

        self.springList = []
        self.puckList = []
        self.pivotList = []
        self.constraintList = []
        self.spinnerList = []
        self.cylinderList = []
        self.generatorList = []

        self.totalEnergy = 0

        self.stableCount = 0
        self.contractingCount = 0
        self.expandingCount = 0

        self.buttonList = []
        self.sliderList = []

        self.t = 0

        self.g = 9.81
        self.stiffness = 1
        self.breakable = False

        self.grid = Grid(self, 120)
        #self.map = load_pygame("D:/Documents/programming/physics/NewSim/boxes.tmx")
        
        
        pygame.mixer.init()
        #self.combustion_sound = pygame.mixer.Sound("D:/Documents/programming/physics/NewSim/audio/combustion.wav")
        #self.combustion_sound.set_volume(VOLUME)

    def update(self, clock):
        #print(self.buttonList[0].pos)

        #self.grid.draw()

        self.stableCount = 0
        self.contractingCount = 0
        self.expandingCount = 0
        for s in self.springList:
            if s.stable:
                self.stableCount += 1
            elif s.contracting:
                self.contractingCount += 1
            elif s.expanding:
                self.expandingCount += 1

        if pygame.time.get_ticks() % 200 == 0:
            self.totalEnergy = 0

        for p in self.puckList:
            if pygame.time.get_ticks() % 200 == 0:
                self.totalEnergy += p.kineticEnergy
            gridParticles = self.grid.cells[p.cell[1]][p.cell[0]].particles
            if len(gridParticles) > 1:
                #print ("checking for collisions in cell: " + str(p.cell)) 
                for q in gridParticles:
                    if p == q:
                        pass
                    else:
                        dist = distance(p.pos, q.pos)

                        if dist <= (p.radius + q.radius):
                            p.interCollide(dist, q)
                            pass

        '''
        for p in self.puckList:
            self.totalEnergy += p.kineticEnergy
            for q in self.puckList:
                if p == q:
                    pass

                else:

                    dist = distance(p.pos, q.pos)

                    if dist <= (p.radius + q.radius):
                        p.interCollide(dist, q)
                        pass
            '''
        mult = 0.7
        for c in self.cylinderList:
            for p in self.puckList:
                if c.rect.collidepoint(p.pos + np.array((p.radius, p.radius))) or c.rect.collidepoint(p.pos - np.array((p.radius, p.radius))):
                    #print ("ball is in container!")
                    currpos = p.pos
                    nextpos = p.pos + p.vel + p.accel * dt**2 * SPEED
                    x = nextpos[0]
                    y = nextpos[1]
                    xleft = nextpos[0] - p.radius
                    xright = nextpos[0] + p.radius
                    ytop = nextpos[1] - p.radius
                    ybottom = nextpos[1] + p.radius

                    c.combustionArea = c.rect.height * (p.pos[0] - p.radius - c.rect.left)
                    #print (c.combustionArea)

                    if c.top.collidepoint(x, ytop) and c.bottom.collidepoint(x, ybottom):
                        #print("COLLIDE TOP AND BOTTOM")
                        p.pos[1] = c.rect.centery

                    elif c.left.collidepoint(xleft, y):
                        #print("COLLIDE LEFT")
                        p.pos[0] = p.prevPos[0]
                        p.prevPos[0] = currpos[0]
                        p.vel[0] = -p.vel[0] * mult
                    elif c.right.collidepoint(xright, y):
                        #print("COLLIDE RIGHT")
                        p.pos[0] = p.prevPos[0]
                        p.prevPos[0] = currpos[0]
                        p.vel[0] = -p.vel[0] * mult
                    elif c.top.collidepoint(x, ytop):
                        #print("COLLIDE TOP")
                        p.pos[1] = p.prevPos[1]
                        p.prevPos[1] = currpos[1]
                        p.vel[1] = -p.vel[1] * mult
                    elif c.bottom.collidepoint(x, ybottom):
                        #print("COLLIDE BOTTOM")
                        p.pos[1] = p.prevPos[1]
                        p.prevPos[1] = currpos[1]
                        p.vel[1] = -p.vel[1] * mult



        self.WIN.fill((217, 217, 217))
        pygame.draw.rect(self.WIN, BLACK, pygame.Rect(leftwall, topwall, rightwall-100, bottomwall-50),  5)

        stableText = self.font.render("Stable: " + str(self.stableCount), True, BLACK)
        self.WIN.blit(stableText, (10, 10))
        contractingText = self.font.render("Contracting: " + str(self.contractingCount), True, BLACK)
        self.WIN.blit(contractingText, (10, 30))
        expandingText = self.font.render("Expanding: " + str(self.expandingCount), True, BLACK)
        self.WIN.blit(expandingText, (10, 50))
    
        totalEnergyText = self.font.render("Total Energy: " + str(round(self.totalEnergy)), True, BLACK)
        self.WIN.blit(totalEnergyText, (leftwall, 70))

        gravityText = self.font.render("Gravity: " + str(self.g), True, BLACK)
        self.WIN.blit(gravityText, (10, 90))
        stiffnessText = self.font.render("Stiffness: " + str(self.stiffness), True, BLACK)
        self.WIN.blit(stiffnessText, (10, 110))
        mousePosTest = self.font.render("Mouse Pos: " + str(pygame.mouse.get_pos()), True, BLACK)
        self.WIN.blit(mousePosTest, (10, 130))
        FPS = self.font.render("FPS: " + str(int(clock.get_fps())), True, BLACK)
        self.WIN.blit(FPS, (10, 170))

    def collide(self, block1, block2, side):
        block1_vel = block1.vel

        if side == "top":
            block1.pos[1] = block2.pos[1] - block1.width
            block1.vel[1] = block2.vel[1]
            block2.vel[1] = block1_vel[1]
            block1.surface = block2.surface

        if side == "bottom":
            block1.pos[1] = block2.pos[1] + block2.width
            block1.vel[1] = block2.vel[1]
            block2.vel[1] = block1_vel[1]
            block1.surface = block2.surface

        if side == "left":
            block1.pos[0] = block2.pos[0] - block1.length
            block1.vel[0] = block2.vel[0]
            block2.vel[0] = block1_vel[0]

        if side == "right":
            block1.pos[0] = block2.pos[0] + block2.length
            block1.vel[0] = block2.vel[0]
            block2.vel[0] = block1_vel[0]

    def addSpring(self, p1, p2, length, k, name=None, block=False, offset=0):
        self.springList.append(Spring(p1, p2, length, k, name=name, block=block, offset=offset))

    def addPuck(self, puck):
        self.puckList.append(puck)
        return puck
    
    def addPivot(self, pivot):
        self.pivotList.append(pivot)
        return pivot
    
    def addBlock(self, block):
        self.blockList.append(block)
        return block
    
    def addButton(self, button):
        self.buttonList.append(button)
        return button
    
    def addConstraint(self, constraint):
        self.constraintList.append(constraint)
        return constraint
    
    def addSpinner(self, spinner):
        self.spinnerList.append(spinner)
        return spinner
    
    def addCylinder(self, cylinder):
        self.cylinderList.append(cylinder)
        return cylinder
    
    def addGenerator(self, generator):
        self.generatorList.append(generator)
        return generator