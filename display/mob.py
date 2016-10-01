from displayobj import DisplayObj

class Mob(DisplayObj):
    """Display Object that Moves"""
    def __init__(self):
        DisplayObj.__init__(self)
        self.speed = 0
    def center(self):
        xcenter = self.x+self.width/2
        ycenter = self.y+self.height/2
        return (xcenter,ycenter)
    def right(self):
        xright = self.x+self.width
        yright = self.y+self.height/2
        return xright,yright
    def left(self):
        xleft = self.x
        yleft = self.y+self.height/2
        return xleft,yleft
    def down(self):
        x = self.x+self.width/2
        y = self.y+self.height
        return x,y
    def up(self):
        x = self.x+self.width/2
        y = self.y
        return x,y
    def topleft(self):
        x = self.x
        y = self.y
        return x,y
    def topright(self):
        x = self.x+self.width
        y = self.y
        return x,y
    def bottomleft(self):
        x = self.x
        y = self.y+self.height
        return x,y
    def bottomright(self):
        x = self.x+self.width
        y = self.y+self.height
        return x,y
    def moveup(self,delta=0):
        if delta == 0:
            delta = self.speed
        self.y -=delta
    def movedown(self,delta=0):
        if delta == 0:
            delta = self.speed
        self.y +=delta
    def moveleft(self,delta=0):
        if delta == 0:
            delta = self.speed
        self.x -=delta
    def moveright(self,delta=0):
        if delta == 0:
            delta = self.speed
        self.x +=delta

