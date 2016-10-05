#Game module

import sys, traceback,random
import pygame as pg
from pygame.locals import *
from display import colors
from display.mapdisplay import MapDisplay
import utils.vect2d as vect
import numpy as np
import json


WIDTH = HEIGHT = 650
FPS = 24
SHAPE = (12,12)
KNUMS = [K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9]
TSIZE = 25

class MapEditor:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        self.tsize = TSIZE
        pg.display.set_caption('BotSurvival!')
        self.screen.fill(colors.white)
        pg.display.update()
        self.clock = pg.time.Clock()
        self.startportal = None
        self.endportal = None
        self.portalmode = 0
        self.verbose = False
        
        self.restart()

    def restart(self):
        self.color = 1
        self.gamealive = True
        if len(sys.argv) >= 2 and sys.argv[1] != "new":
            self.world= MapDisplay((24,24),sys.argv[1])
        else:
            self.world= MapDisplay((24,24))
        self.world.draw(self.screen)
        pg.display.update()
        if len(sys.argv) == 3:
            self.filename = sys.argv[2]
        else:
            self.filename = 'map'+str(random.randrange(9999))+".json"
        while self.gamealive:
            deltaTime = self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    loc = self.world.pointtoloc(event.pos)
                    if self.verbose:
                        print "Clic",loc,event.pos
                    if loc != None:
                        self.world.map[loc] = self.color
                    if self.portalmode == 1:
                        self.startportal = loc
                        self.portalmode = 2
                    elif self.portalmode == 2:
                        self.endportal = loc
                        self.printportal()
                        self.portalmode = 0
                elif event.type == KEYDOWN:
                    #Save map whe press 's'
                    if event.key == K_s:
                        mapaslist = self.world.map.tolist()
                        mapout = open(self.filename,'w')
                        d = {"map":mapaslist}
                        json.dump(d,mapout)
                        mapout.close()
    
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
                            
            self.world.draw(self.screen)
            pg.display.update()
    def printportal(self):
        """Print portal in json format"""
        key = "_".join(str(v) for v in self.startportal)
        value = tuple(["0"])+self.endportal
        d = {key:value}
        print json.dumps(d)
                            
if __name__ == '__main__':
    try:
        game = MapEditor()
    except Exception as ex:
        print type(ex), ex
        traceback.print_exc()
        pg.quit()
        sys.exit()
