#Rectangular board 
import utils.vect2d as vect
import numpy as np
import json

def strtotuple(strchain):
    l = strchain.split('_')
    return tuple([int(n) for n in l])
def tupletostr(inttuple):
    l = [str(n) for n in inttuple]
    return "_".join(l)
class Rectboard:
    def __init__(self, shape,mapsrc=None):
        self.allitems = dict()
        if mapsrc:
            self.loadlevel(mapsrc)
        else:
            self.map = np.zeros(shape,dtype=int)
            self.items = dict()
            self.portals = dict()
            self.switches = dict()
            self.artefacts = dict()
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
                    nkey = strtotuple(key)
                    self.portals[nkey] = d[key]
            else :
                self.portals = dict()
            if mapsrc in self.allitems:
                self.items = self.allitems[mapsrc]
            elif "items" in mapdata:
                d = mapdata["items"]
                self.items = dict()
                for key in d:
                    nkey = strtotuple(key)
                    self.items[nkey] = d[key].split('_')
                    self.allitems[mapsrc] = self.items
            else:
                self.items = dict() 
                self.allitems[mapsrc] = self.items
            if "switches" in mapdata:
                d = mapdata["switches"]
                self.switches = dict()
                for key in d:
                    nkey = strtotuple(key)
                    self.switches[nkey] = d[key]
            else:
                self.switches = dict()
            if "artefacts" in mapdata:
                d = mapdata["artefacts"]
                self.artefacts = dict()
                for key in d:
                    nkey = strtotuple(key)
                    self.artefacts[nkey] = d[key].split('_')
            else:
                self.artefacts = dict()


    def dumplevel(self,maptarget):
        """Write the current level in a file (used only by the editor)"""
        mapfile = open(maptarget, "w")
        data = dict()
        data["map"] = self.map.tolist()
        if self.portals:
            data["portals"] = dict()
            for key in self.portals:
                nkey = tupletostr(key)
                data["portals"][nkey] = self.portals[key]
        if self.items:
            data["items"] = dict()
            for key in self.items:
                nkey = tupletostr(key)
                data["items"][nkey] = tupletostr(self.items[key])
        if self.switches:
            data["switches"] = dict()
            for key in self.switches:
                nkey = tupletostr(key)
                data["switches"][nkey] = tupletostr(self.switches[key])
        if self.artefacts:
            data["artefacts"] = dict()
            for key in self.artefacts:
                nkey = tupletostr(key)
                data["artefacts"][nkey] = tupletostr(self.artefacts[key])

            
        json.dump(data,mapfile)
        mapfile.close()

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
