#Game module

import sys, traceback,random
import pygame as pg
from pygame.locals import *
from display import colors
from display.mapdisplay import MapDisplay
from display.tileinfo import TileMgr
from display.spritesheet import Sheet
import utils.vect2d as vect
import numpy as np
import json


WIDTH = HEIGHT = 650
FPS = 24
SHAPE = (12,12)
KNUMS = [K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9]
TSIZE = 32
MAINITEMS = ['item','sign','shoes','stone']

class PickSurface:
    def __init__(self):
        self.width = 400
        self.height = 64
        self.x = 25
        self.y = 550
        self.bgsheet = Sheet('assets/images/terrain.png',TSIZE) 
        self.fgsheet = Sheet('assets/images/beacon.png',TSIZE)
        self.numsize = 10
    def draw(self,surface):
        surface.fill(colors.black,(self.x,self.y,self.width,self.height))
        tilemgr = TileMgr()
        x = self.x
        y = self.y
        for n in range(self.numsize):
            tile = tilemgr.tile(n)
            pg.draw.rect(surface,tile.color,(x,y,TSIZE,TSIZE))
            if tile.bg != None:
                image = self.bgsheet.image_num(tile.bg)
                surface.blit(image,(x,y,TSIZE,TSIZE))
            if tile.fg != None:
                image = self.fgsheet.image_num(tile.fg,-1)
                surface.blit(image,(x,y,TSIZE,TSIZE))
            x+=TSIZE
    def insideSurf(self,(x,y)):
        return y > self.y and y < self.y+TSIZE and x > self.x and x < self.x+TSIZE*(self.numsize+1)
    def getnum(self,(x,y)):
        if y > self.y and y < self.y+TSIZE:
            num =  (x-self.x)/TSIZE
            if num>self.numsize:
                num = 0
            return num
        else:
            return 0







class MapEditor:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        self.tsize = TSIZE
        pg.display.set_caption('Map editor!')
        self.screen.fill(colors.white)
        pg.display.update()
        self.clock = pg.time.Clock()
        self.startportal = None
        self.endportal = None
        self.portalmode = 0
        self.portals = dict()
        self.items= dict()
        self.coinmode = 0
        self.itemsmode = 0
        self.itemcounter = 0
        self.verbose = False
        self.picksurf = PickSurface() 
        try:
            self.restart()
        except Exception as ex:
            print type(ex), ex
            self.world.dumplevel(self.filename+".tmp")
            print "temp file saved as tmp: "+self.filename+".tmp"
            traceback.print_exc()
            pg.quit()
            sys.exit()

    def restart(self):
        self.color = 1
        self.gamealive = True
        if len(sys.argv) >= 2 and sys.argv[1] != "new":
            self.world= MapDisplay((15,15),sys.argv[1])
        else:
            self.world= MapDisplay((15,15))

        self.world.draw(self.screen)
        pg.display.update()
        if len(sys.argv) == 3:
            self.filename = sys.argv[2]
        else:
            self.filename = 'map'+str(random.randrange(9999))+".json"
        while self.gamealive:
            #Main loop
            deltaTime = self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    loc = self.world.pointtoloc(event.pos)
                    if self.picksurf.insideSurf(event.pos):
                        self.color = self.picksurf.getnum(event.pos)
                        tilemgr = TileMgr()
                        print tilemgr.tile(self.color).description

                    if loc != None and self.portalmode == 0 and self.coinmode == 0 and self.itemsmode == 0:
                        self.world.map[loc] = self.color
                    elif self.portalmode == 1:
                        self.startportal = loc
                        self.portalmode = 2
                        print "Source portal", loc
                    elif self.portalmode == 2:
                        self.endportal = loc
                        self.printportal()
                        self.portalmode = 0
                        print "End portal", loc
                    elif self.coinmode == 1:
                        self.world.items[loc] = ("coin",10)
                    elif self.itemsmode != 0:
                        item = (MAINITEMS[self.itemcounter],random.randrange(999))
                        self.world.items[loc] =   item
                        print loc,item
                elif event.type == KEYDOWN:
                    #Save map when press 's'
                    if event.key == K_s:
                        self.world.dumplevel(self.filename)
                        print "Map Saved as",self.filename
                    elif event.key == K_1:
                        self.color = 0
                    elif event.key == K_2:
                        self.color = 1
                    elif event.key == K_3:
                        self.color = 2
                    elif event.key == K_p:
                        self.portalmode = 1
                        print "Click to choose portal points"
                    elif event.key == K_v:
                        if not self.verbose:
                            self.verbose = True
                        else:
                            self.verbose = False
                    elif event.key == K_c:
                        if self.coinmode == 0:
                            self.coinmode = 1
                        else:
                            self.coinmode = 0
                    elif event.key == K_i:
                        if self.itemsmode == 0:
                            self.itemsmode = MAINITEMS[0]
                        else:
                            self.itemsmode = 0
                    elif event.key == K_SPACE:
                        self.itemcounter += 1
                        if self.itemcounter >= len(MAINITEMS):
                            self.itemcounter = 0
                        print MAINITEMS[self.itemcounter]

                            
            self.world.draw(self.screen)
            self.picksurf.draw(self.screen)
            pg.display.update()
    def printportal(self):
        """Writes a portal in the map data"""
        self.world.portals[self.startportal] = tuple(["0"])+self.endportal
                            
if __name__ == '__main__':
    try:
        game = MapEditor()
    except Exception as ex:
        print type(ex), ex
        traceback.print_exc()
        pg.quit()
        sys.exit()
