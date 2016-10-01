#DisplayObjects classes
class DisplayObj():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 1
        self.height = 1
    def setpos(self,(x,y)):
        self.x = x
        self.y = y
    def pos(self):
        return (self.x,self.y)
    def draw(self,surface):
        pass
class Grid(DisplayObj):
    def __init__(self,shape, tsize=15):
        DisplayObject.__init__(self)
        self.tsize = tsize
        self.shape = shape
        self.width = shape[1]*tsize
        self.height = shape[0]*tsize
    def draw(self,surface):
        tsize = self.tsize
        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                rec = (self.x+col*tsize,self.y+row*tsize,tsize,tsize)
                pg.draw.rect(surface,0x0,rec,1)



if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((640,480))
    screen.fill(0xFFFFFF)
    grid = Grid((10,10))
    grid.x = 100
    grid.y = 70
    grid.draw(screen)
    pg.display.update()
    pg.time.wait(2000)
    pg.quit()
