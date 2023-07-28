from random import randint
from mass import Mass
import pygame
from settings import *
import numpy as np
from environment import Environment

class Block(Mass):

    randPos = np.array((randint(110, 720), randint(55, 380)))
    randVel = np.array((randint(0, 10), randint(0, 10)))
    randColor = (( randint(0, 255), randint(0, 255), randint(0, 255) ))

    randLength = randint(5, 50)
    randWidth = randint(5, 50)


    def __init__(self, environment, mass = randint(1, 50), pos = randPos, length = randLength, width = randWidth, vel=randVel, color=randColor, name="Block"):
        super().__init__(environment, mass, pos, vel, color)
        self.length = length
        self.width = width
        self.box = pygame.Rect(self.pos[0], self.pos[1], self.length, self.width)
        self.surface_area = self.length

        self.blockList = []
        self.rectList = []

        self.name = name

        self.held = False

        self.prevPos = self.pos


    def update(self, mousePos, t):
        self.box = pygame.Rect(self.pos[0], self.pos[1], self.length, self.width)
        
        self.collision()
        self.updatePos(mousePos, t)
            

    def collision(self):
        if self.pos[0] + self.vel[0] * dt  <= leftwall + self.length:
            self.vel[0] = -self.vel[0]
        if self.pos[0] + self.vel[0] * dt >= rightwall - self.length:
            self.vel[0] = -self.vel[0]
        if self.pos[1] + self.vel[1] * dt <= topwall + self.width:
            self.vel[1] = -self.vel[1]
        if self.pos[1] + self.vel[1] * dt >= bottomwall - self.width:
            self.vel[1] = 0
            self.surface = True
        else:
            self.surface = False

        


        index = self.box.collidelistall(self.rectList)

    
        for i in index:
            if i != -1:
                
                #print ("{}: {} , {}: {}".format(self.name, self.pos, self.blockList[i].name, self.blockList[i].pos))
                if abs(self.rectList[i].top - self.box.bottom) < 10:
                    self.environment.collide(self, self.blockList[i], 'top')

                if abs(self.rectList[i].bottom - self.box.top) < 10:
                    self.environment.collide(self, self.blockList[i], 'bottom')

                if abs(self.rectList[i].left - self.box.right) < 10:
                    self.environment.collide(self, self.blockList[i], 'left')

                if abs(self.rectList[i].right - self.box.left) < 10:
                    self.environment.collide(self, self.blockList[i], 'right')


    def draw(self, mousePos, t):
        self.blockList = self.environment.blockList.copy()
        self.rectList = self.environment.rectList.copy()
            
        
        self.update(mousePos, t)

        pygame.draw.rect(self.environment.WIN, self.color, self.box)
        pygame.draw.rect(self.environment.WIN, ((33, 33, 33)), self.box, 1)