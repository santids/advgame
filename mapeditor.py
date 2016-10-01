#Game module

import sys, traceback,random
import pygame as pg
from pygame.locals import *
from display import colors
from rectboard import Rectboard
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
        
        self.restart()

    def restart(self):
        self.color = 1
        self.gamealive = True
        if len(sys.argv) >= 2 and sys.argv[1] != "new":
            self.board = Rectboard((12,12),sys.argv[1])
        else:
            self.board = Rectboard((12,12))
        self.xpad = 50
        self.ypad = 100
        self.draw_board()
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
                    loc = self.pointtoloc(event.pos)
                    if loc != None:
                        self.board.map[loc] = self.color
                elif event.type == KEYDOWN:
                    #Save map whe press 's'
                    if event.key == K_s:
                        mapaslist = self.board.map.tolist()
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
                            
            self.draw_board()
            pg.display.update()
                            
    def draw_board(self):

        color = colors.gray6
        
        for loc in self.board.alllocs:
            if self.board.map[loc] == 0:
                color = colors.gray6
            elif self.board.map[loc] == 1:
                color = colors.black
            elif self.board.map[loc] == 2:
                color = colors.cyan6
            point = self.loctopoint(loc)
            tsize = self.tsize
            pg.draw.rect(self.screen,color,(point[0],point[1],tsize,tsize),0)

    def loctopoint(self,loc):
       """Given a location of the map returns the corresponding surface point"""
       locy,locx = loc
       x = self.xpad+locx*self.tsize
       y = self.ypad+locy*self.tsize

       return (x,y)
    def pointtoloc(self,point):
       """Given a point of the surface returns the loc in map"""
       x,y = point
       xloc = (y-self.ypad)/self.tsize
       yloc = (x-self.xpad)/self.tsize

       if self.board.isValidLoc((xloc,yloc)):
           return (xloc,yloc)
       else:
           return None
        

if __name__ == '__main__':
    try:
        game = MapEditor()
    except Exception as ex:
        print type(ex), ex
        traceback.print_exc()
        pg.quit()
        sys.exit()
