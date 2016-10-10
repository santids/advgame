#Thanks to http://pygame.org/wiki/Spritesheet
import pygame as pg
from pygame.locals import *

class Sheet():
    def __init__(self,filename,tsize=None):
        self.tsize = tsize
        try:
            self.sheet = pg.image.load(filename).convert()
            self.width = self.sheet.get_width()
            self.height = self.sheet.get_height()
        except pg.error, message:
            print "Unable to load spritesheet image:",filename
    def image_at(self,rectangle,colorkey=None):
        """Loads image from x,y,x+offset,y+offset"""
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert()
        image.blit(self.sheet,(0,0),rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey,pg.RLEACCEL)
        return image
    def image_num(self,n,colorkey=None):
        """Loads the n image in the spritesheet file"""
        rect = (n*self.tsize,0,self.tsize,self.tsize)
        return self.image_at(rect,colorkey)
    def images_number(self):
        return self.width/self.tsize
class AnimSheet(Sheet):
    def __init__(self,filename,tsize,speed=1):
        Sheet.__init__(self,filename,tsize)
        self.counter = 0
        self.speed = speed
    def nextImg(self,colorkey=None):
        n = (self.counter/self.speed) % self.images_number()
        self.counter +=1
        return self.image_num(n,colorkey)
if __name__ == '__main__':
    pg.init()
    w = 640
    h = 480
    screen = pg.display.set_mode((w,h))
    screen.fill((255,255,255))
    sheet = AnimSheet('assets/images/gradient.png',32,2)
    clock = pg.time.Clock()
    while True:
        deltatime = clock.tick(12)
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
        image = sheet.nextImg()
        screen.blit(image,image.get_rect())
        pg.display.update()
        
       
