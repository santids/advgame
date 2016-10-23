#Rectangular board 
import utils.vect2d as vect
import numpy as np
import json

class Rectboard:
    def __init__(self, shape,mapsrc=None):
        self.allitems = dict()
        if mapsrc:
            self.loadlevel(mapsrc)
        else:
            self.map = np.zeros(shape,dtype=int)
            self.items = dict()
        self.shape = self.map.shape
        self.alllocs = [(r,c) for r in xrange(self.shape[0]) for c in xrange(self.shape[1])]
        self.mapcenter = vect.div(self.shape,2)
    def loadlevel(self,mapsrc):
            mapfile = open(mapsrc)
            mapdata = json.load(mapfile)
            self.map = np.asarray(mapdata["map"])
            if "portals" in mapdata:
                d = mapdata["portals"]
                self.portals = dict()
                for key in d:
                    nkey =key.split('_')
                    nkey = tuple([int(n) for n in nkey])
                    self.portals[nkey] = d[key]
            else :
                self.portals = dict()
                
                
            if mapsrc in self.allitems:
                self.items = self.allitems[mapsrc]
            elif "items" in mapdata:
                d = mapdata["items"]
                self.items = dict()
                for key in d:
                    nkey = key.split('_')
                    nkey = tuple([int(n) for n in nkey])
                    self.items[nkey] = d[key].split('_')
                    self.allitems[mapsrc] = self.items
            else:
                self.items = dict() 
                self.allitems[mapsrc] = self.items

    def isValidLoc(self,loc):
        """True if loc is inside map bounds"""
        return vect.isInsideRect(loc,self.shape)
    def locs_around(self,loc):
        """return nearby locs"""
        locs = list()
        locs.append(vect.suma(loc,(0,1)))
        locs.append(vect.suma(loc,(0,-1)))
        locs.append(vect.suma(loc,(1,0)))
        locs.append(vect.suma(loc,(-1,0)))
        
        nl = [loc for loc in locs if self.isValidLoc(loc)]
        return nl
    def toward(self,curr,target):
        """Returnes the nearbyloc that is closest to target"""
        options = self.locs_around(curr)
        dist = min([vect.dist(loc,target) for loc in options])
        for loc in options:
            if vect.dist(loc,target) == dist:
                return loc

if __name__ == '__main__':
    board = Rectboard((5,5),'levels/level1.json')
    print board.portals
