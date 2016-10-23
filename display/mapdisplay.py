import pygame as pg
import numpy as np
from displayobj import DisplayObj
from rectboard import Rectboard 
import colors
from tileinfo import TileMgr
from spritesheet import Sheet

class MapDisplay(DisplayObj,Rectboard):
    def __init__(self,shape,mapsrc=None):
        Rectboard.__init__(self,shape,mapsrc)
        DisplayObj.__init__(self)
        self.x= 20
        self.y= 20
        self.tsize = 32
        self.width = self.tsize*self.shape[1]
        self.height = self.tsize*self.shape[0]
        self.bgsheet = Sheet('assets/images/terrain.png',self.tsize)
        self.fgsheet = Sheet('assets/images/beacon.png',self.tsize)
        self.itsheet = Sheet('assets/images/items.png',self.tsize)

    def draw(self,surface):
        """Draw map on surface"""
        tilemgr = TileMgr()
        for loc in self.alllocs:
            tile = tilemgr.tile(self.map[loc])
            point = self.loctopoint(loc)
            pg.draw.rect(surface,tile.color,(point[0],point[1],self.tsize,self.tsize),0)
            if tile.bg != None:
                image = self.bgsheet.image_num(tile.bg)
                surface.blit(image,(point[0],point[1],self.tsize,self.tsize))
            if tile.fg != None:
                image = self.fgsheet.image_num(tile.fg,-1)
                surface.blit(image,(point[0],point[1],self.tsize,self.tsize))
            if loc in self.items:
                image = self.itsheet.image_num(0,-1)
                surface.blit(image,(point[0],point[1],self.tsize,self.tsize))



    def loctopoint(self,loc):
       """Given a location of the map returns the corresponding surface point"""
       locy,locx = loc
       x = self.x+locx*self.tsize
       y = self.y+locy*self.tsize

       return (x,y)
    def pointtoloc(self,point):
       """Given a point of the surface returns the loc in map"""
       x,y = point
       xloc = (y-self.y)/self.tsize
       yloc = (x-self.x)/self.tsize

       if self.isValidLoc((xloc,yloc)):
           return (xloc,yloc)
       else:
           return None
    def loctop(self,loc):
        x,y = self.loctopoint(loc)
        return y 
    def locbottom(self,loc):
        x,y = self.loctopoint(loc)
        return y+self.tsize
    def locleft(self,loc):
        x,y = self.loctopoint(loc)
        return x
    def locright(self,loc):
        x,y = self.loctopoint(loc)
        return x+self.tsize

if __name__ == '__main__':
    mapobj = MapDisplay()
