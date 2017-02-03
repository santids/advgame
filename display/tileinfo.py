"""Different functions that provide information about a tiletype indicated by a number"""
from display import colors

_tiletypes = dict()
class TileType:
    def __init__(self,num,isobstacle=False,color=colors.gray6,bg=None,fg=None,kills=False,description=""):
        self.num = num
        self.color = color
        self.bg = bg
        self.fg = fg
        self.description = description
        self.isobstacle = isobstacle
        self.kills = kills
    def __str__(self):
        #return " ".join(["Tile:",str(self.num), self.description,str(self.isobstacle),str(self.kills)])
        return str(self.kills)
class TileMgr:
    def __init__(self):
        self.tiletypes = dict()
        self.tiletypes[0] = TileType(0,False,colors.gray6,0,None,description="simple walkable sand")
        self.tiletypes[1] = TileType(1,True,colors.black,1,None,description="simple wood obstacle")
        self.tiletypes[2] = TileType(2,bg=0,fg=0,description="portal")
        self.tiletypes[3] = TileType(3,False,colors.brown7,description="checkpoint")
        self.tiletypes[5] = TileType(5,False,colors.red7,kills=True,description="lava")
    
        self.defaulttile = TileType(256)
    def tile(self,num):
        if num in self.tiletypes:
            return self.tiletypes[num]
        else:
            return self.defaulttile





if __name__ == '__main__':
    print color(0)
    print isobstacle(1)
    print isobstacle(2)
