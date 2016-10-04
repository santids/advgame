import pygame as pg
import numpy as np
from displayobj import DisplayObj
from rectboard import Rectboard 
import colors


class MapDisplay(DisplayObj,Rectboard):
    def __init__(self,shape,map):
        Rectboard.__init__(self,shape,map)
        DisplayObj.__init__(self)
        self.xpad = 100
        self.ypad = 100
        self.tsize = 25
        self.width = self.tsize*self.shape[1]
        self.height = self.tsize*self.shape[0]
    def draw(self,surface):
        """Draw map on surface"""
        color = colors.brown8
        for loc in self.alllocs:
            if self.map[loc] == 0:
                color = colors.gray6
            elif self.map[loc] == 1:
                color = colors.black
            elif self.map[loc] == 2:
                color = colors.cyan6
            point = self.loctopoint(loc)
            pg.draw.rect(surface,color,(point[0],point[1],self.tsize,self.tsize),0)

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
