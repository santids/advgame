from display.mob import Mob
import pygame as pg
from pygame.locals import *
import display.colors as colors
import math,tileinfo

class Hero(Mob):
    def __init__(self,settings):
        Mob.__init__(self)
        self.level = "0"
        self.width = self.height = 15
        self.world = None
        self.speed = 10
        self.settings = settings
    def handleinput(self,input):
        self.handlemovement(input)
        self.update()

    def update(self):
        centerloc = self.world.pointtoloc(self.center())
        if centerloc in self.world.portals:
            newlevel = self.world.portals[centerloc][0]
            newpos = self.world.loctopoint(self.world.portals[centerloc][1:])
            self.x = newpos[0]+(self.world.tsize-self.width)/2
            self.y = newpos[1]+(self.world.tsize-self.height)/2
            if self.level != newlevel:
                self.level = newlevel
                self.world.loadlevel(self.settings["level-path"]+newlevel+'.json')
    def handlemovement(self,input):
        deltax = int(math.ceil( self.speed*input["deltatime"]/100))
        if K_UP in input:
           self.moveup(deltax)
           loc1 = self.world.pointtoloc(self.topleft())
           loc2 = self.world.pointtoloc(self.topright())
           if tileinfo.isobstacle(self.world.map[loc1]) or tileinfo.isobstacle(self.world.map[loc2]):
               cloc = self.world.pointtoloc(self.center())
               lpos = self.world.loctop(cloc)
               self.movedown(abs(lpos-self.y))
        if K_DOWN in input:
            self.movedown(deltax)
            loc1 = self.world.pointtoloc(self.bottomleft())
            loc2 = self.world.pointtoloc(self.bottomright())
            if tileinfo.isobstacle(self.world.map[loc1]) or tileinfo.isobstacle(self.world.map[loc2]):
                cloc = self.world.pointtoloc(self.center())
                lpos = self.world.locbottom(cloc)
                self.moveup(abs(lpos-self.down()[1])+1)
        if K_LEFT in input:
            self.moveleft(deltax)
            loc1 = self.world.pointtoloc(self.topleft())
            loc2 = self.world.pointtoloc(self.bottomleft())
            if tileinfo.isobstacle(self.world.map[loc1]) or tileinfo.isobstacle(self.world.map[loc2]):
                cloc = self.world.pointtoloc(self.center())
                lpos = self.world.locleft(cloc)
                self.moveright(abs(lpos-self.left()[0])+1)
        if K_RIGHT in input:
            self.moveright(deltax)
            loc1 = self.world.pointtoloc(self.bottomright())
            loc2 = self.world.pointtoloc(self.topright())
            if tileinfo.isobstacle(self.world.map[loc1]) or tileinfo.isobstacle(self.world.map[loc2]):
                cloc = self.world.pointtoloc(self.center())
                lpos = self.world.locright(cloc)
                self.moveleft(abs(lpos-self.right()[0])+1)

    def draw(self,surface):
        pg.draw.rect(surface,colors.red6,(self.x,self.y,self.width,self.height))

        

