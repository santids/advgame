import pygame as pg
import sys
from pygame.locals import *
from displayobj import DisplayObj

black = (0,0,0)
white = (255,255,255)

class StatusBar(DisplayObj):
    def __init__(self):
        DisplayObj.__init__(self)
        self.x = 25
        self.y = 0
        self.width = 200
        self.height = 20
        self.font =pg.font.SysFont('Arial',15)
    def say(self,string,surface):
        """write text on bar"""
        text = self.font.render(string,True,black)
        r = (self.x,self.y,self.width,self.height)
        #pg.draw.rect(surface,white,r)
        surface.blit(text,r)

class DialogBox(DisplayObj):
    def __init__(self):
        """Generates a dialog box"""
        DisplayObj.__init__(self)
        self.x = 25
        self.y = 300
        self.width = 350
        self.font = pg.font.SysFont('Arial',15)
        self.height = self.font.get_height()*3
        self.display = False
        self.messages = []
    def say(self,string):
        """Display Message"""
        if string not in self.messages:
            self.messages.append(string)
    def show(self):
        """Display Message"""
        self.display = True
    def next(self):
        if self.messages:
            del self.messages[0]
            if not self.messages:
                self.hide()

    def hide(self):
        """Hide message"""
        self.display = False
    def toggle(self):
        """Hide and show"""
        if self.display:
            self.hide()
        else:
            self.show()
    def draw(self,surface): 
        """Draw messgae box if convenient"""
        if self.display and self.messages:
            msg = self.messages[0]
            text = self.font.render(msg,True,black)
            r = (self.x,self.y,self.width,self.height)
            pg.draw.rect(surface,white,r)
            surface.blit(text,r)



        
