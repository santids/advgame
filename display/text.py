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
        self.y = 450
        self.width = 350
        self.font = pg.font.SysFont('Arial',15)
        self.height = self.font.get_height()*3
        self.display = False
        self.messages = []
        self.main_message = ""
    def say(self,string):
        """Display Message"""
        if string not in self.messages:
            self.messages.append(string)
            self.show()
    def sayAll(self,messagelist):
        for m in messagelist:
            self.say(m)
    def show(self):
        """Display Message"""
        self.display = True
    def next(self):
        if self.main_message != "":
            self.display = not self.display
        else:
            if not self.display:
                if self.messages:
                    self.show()
            else:
                self.hide()
                if self.messages:
                    self.show()

    def hide(self):
        """Hide message"""
        if self.main_message != "":
            self.main_message = ""
        elif self.messages:
            del self.messages[0]
        self.display = False
    def toggle(self):
        """Hide and show"""
        if self.display:
            self.hide()
        else:
            self.show()
    def draw(self,surface): 
        """Draw messgae box if convenient"""
        if self.display and (self.messages or self.main_message != ""):
            msg = None
            if self.main_message != "":
                msg = self.main_message
            else:
                msg = self.messages[0]
            text = self.font.render(msg,True,black)
            r = (self.x,self.y,self.width,self.height)
            pg.draw.rect(surface,white,r)
            surface.blit(text,r)



        
