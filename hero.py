from display.mob import Mob
import pygame as pg
from pygame.locals import *
import display.colors as colors
import math
from display.tileinfo import TileMgr

class Hero(Mob):
    def __init__(self,settings):
        Mob.__init__(self)
        self.level = "0"
        self.width = self.height = 15
        self.world = None
        self.speed = 10
        self.score = 0
        self.settings = settings
    def handleinput(self,input,dialog):
        self.handlemovement(input)
        self.update(dialog)

    def update(self,dialog):
        centerloc = self.world.pointtoloc(self.center())
        if centerloc in self.world.portals:
            newlevel = self.world.portals[centerloc][0]
            newpos = self.world.loctopoint(self.world.portals[centerloc][1:])
            self.x = newpos[0]+(self.world.tsize-self.width)/2
            self.y = newpos[1]+(self.world.tsize-self.height)/2
            if self.level != newlevel:
                self.level = newlevel
                self.world.loadlevel(self.settings["level-path"]+newlevel+'.json')
        if centerloc in self.world.items:
            item = self.world.items[centerloc]
            if item[0] == 'coin':
                self.score += int(item[1])
                del self.world.items[centerloc]
            if item[0] == 'sign':
                dialog.main_message = item[1]
        elif dialog.main_message != "":
            dialog.hide()
            dialog.next()

    def handlemovement(self,input):
        tilemgr = TileMgr()
        deltax = int(math.ceil( self.speed*input["deltatime"]/100))
        if K_UP in input:
           self.moveup(deltax)
           loc1 = self.world.pointtoloc(self.topleft())
           loc2 = self.world.pointtoloc(self.topright())
           tile1 = tilemgr.tile(self.world.map[loc1])
           tile2 = tilemgr.tile(self.world.map[loc2])
           if tile1.isobstacle or tile2.isobstacle:
               cloc = self.world.pointtoloc(self.center())
               lpos = self.world.loctop(cloc)
               self.movedown(abs(lpos-self.y))
        if K_DOWN in input:
            self.movedown(deltax)
            loc1 = self.world.pointtoloc(self.bottomleft())
            loc2 = self.world.pointtoloc(self.bottomright())
            tile1 = tilemgr.tile(self.world.map[loc1])
            tile2 = tilemgr.tile(self.world.map[loc2])
            if tile1.isobstacle or tile2.isobstacle:
                cloc = self.world.pointtoloc(self.center())
                lpos = self.world.locbottom(cloc)
                self.moveup(abs(lpos-self.down()[1])+1)
        if K_LEFT in input:
            self.moveleft(deltax)
            loc1 = self.world.pointtoloc(self.topleft())
            loc2 = self.world.pointtoloc(self.bottomleft())
            tile1 = tilemgr.tile(self.world.map[loc1])
            tile2 = tilemgr.tile(self.world.map[loc2])
            if tile1.isobstacle or tile2.isobstacle:
                cloc = self.world.pointtoloc(self.center())
                lpos = self.world.locleft(cloc)
                self.moveright(abs(lpos-self.left()[0])+1)
        if K_RIGHT in input:
            self.moveright(deltax)
            loc1 = self.world.pointtoloc(self.bottomright())
            loc2 = self.world.pointtoloc(self.topright())
            tile1 = tilemgr.tile(self.world.map[loc1])
            tile2 = tilemgr.tile(self.world.map[loc2])
            if tile1.isobstacle or tile2.isobstacle:
                cloc = self.world.pointtoloc(self.center())
                lpos = self.world.locright(cloc)
                self.moveleft(abs(lpos-self.right()[0])+1)

    def draw(self,surface):
        pg.draw.rect(surface,colors.red6,(self.x,self.y,self.width,self.height))

        

