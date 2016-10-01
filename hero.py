from display.mob import Mob
import pygame as pg
from pygame.locals import *
import display.colors as colors

class Hero(Mob):
    def __init__(self):
        Mob.__init__(self)
        self.width = self.height = 15
        self.world = None
        self.speed = 5
    def handleinput(self,input):
        if K_UP in input:
           self.moveup()
           loc1 = self.world.pointtoloc(self.topleft())
           loc2 = self.world.pointtoloc(self.topright())
           if self.world.board.map[loc1] == 1 or self.world.board.map[loc2] == 1:
               cloc = self.world.pointtoloc(self.center())
               lpos = self.world.loctop(cloc)
               self.movedown(abs(lpos-self.y))
        if K_DOWN in input:
            self.movedown()
            loc1 = self.world.pointtoloc(self.bottomleft())
            loc2 = self.world.pointtoloc(self.bottomright())
            if self.world.board.map[loc1] == 1 or self.world.board.map[loc2] == 1:
                cloc = self.world.pointtoloc(self.center())
                lpos = self.world.locbottom(cloc)
                self.moveup(abs(lpos-self.down()[1])+1)
        if K_LEFT in input:
            self.moveleft()
            loc1 = self.world.pointtoloc(self.topleft())
            loc2 = self.world.pointtoloc(self.bottomleft())
            if self.world.board.map[loc1] == 1 or self.world.board.map[loc2] == 1:
                cloc = self.world.pointtoloc(self.center())
                lpos = self.world.locleft(cloc)
                self.moveright(abs(lpos-self.left()[0])+1)
        if K_RIGHT in input:
            self.moveright()
            loc1 = self.world.pointtoloc(self.bottomright())
            loc2 = self.world.pointtoloc(self.topright())
            if self.world.board.map[loc1] == 1 or self.world.board.map[loc2] == 1:
                cloc = self.world.pointtoloc(self.center())
                lpos = self.world.locright(cloc)
                self.moveleft(abs(lpos-self.right()[0])+1)
        self.update()

    def update(self):
        centerloc = self.world.pointtoloc(self.center())
        if centerloc in self.world.board.portals:
            newpos = self.world.loctopoint(self.world.board.portals[centerloc])
            self.x = newpos[0]
            self.y = newpos[1]
    def draw(self,surface):
        pg.draw.rect(surface,colors.red6,(self.x,self.y,self.width,self.height))

        

