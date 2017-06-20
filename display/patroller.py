from mob import Mob
from displayobj import DisplayObj
import colors
import pygame as pg
import math
from pygame.locals import *
import utils.vect2d as vect

class Patroller(Mob):
    def __init__(self,world,startloc,endloc):
        self.level = "0"
        DisplayObj.__init__(self)
        self.startloc = startloc
        self.endloc = endloc
        self.speed = 4.0
        self.width = self.height = 15
        self.world = world
        self.x, self.y = self.world.loctopoint(startloc)
        self.x += self.width/2
        self.y += self.height/2
    def move(self,deltatime):
        v = vect.resta(self.endloc,self.startloc)
        dy,dx = vect.div(v,vect.modulo(v))
        dx *= math.ceil(self.speed*deltatime/100)
        dy *= math.ceil(self.speed*deltatime/100)
        centerloc = self.world.pointtoloc(self.center())
        if centerloc == self.endloc:
            self.endloc = self.startloc
            self.startloc = centerloc
        self.x += dx
        self.y += dy
    def update(self,deltatime=0.2):
        self.move(deltatime)
    def draw(self,surface):
        pg.draw.rect(surface,colors.green6,(self.x,self.y,self.width,self.height))


