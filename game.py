#!/usr/bin/python2.7


import pygame as pg
from pygame.locals import *
import numpy as np
import traceback,sys
from display.mapdisplay import MapDisplay
from hero import Hero
import display.colors as colors
from display.text import StatusBar,DialogBox
import utils.vect2d as vect
import json,random

class Game():
    def __init__(self,width,height,fps=25,caption="My Game"):
        """Initialize Pygame"""
        self.fps =fps
        self.width =width
        self.height =height
        pg.init()
        self.screen = pg.display.set_mode((self.width,self.height))
        pg.display.set_caption(caption)
        self.clock = pg.time.Clock()
        self.start()
    def start(self):
        """Start the game"""
        self.screen.fill(colors.white)
        self.gamealive = True
        self.gameloop()
    def gameloop(self):
        """The Game Loop"""
        while self.gamealive:
            deltatime = self.clock.tick(self.fps)
            for event in pg.event.get():
                if event.type == QUIT:
                    self.close()

            pg.display.update()
    def close(self):
        """Quit and exit"""
        print "Bye"
        pg.quit()
        sys.exit()
        
class AdvGame(Game):
    def __init__(self,settings=dict()):
        self.settings = settings
        Game.__init__(self,settings["width"],settings["height"],fps=settings["fps"],caption="Adventure Game")
    def start(self):
        """Start the game"""
        self.displaylist = []
        self.mapdisplay = MapDisplay((3,3),settings["level0"])
        self.hero = Hero(self.settings)
        loc = vect.div(self.mapdisplay.shape,2)
        if "hero-start-loc" in settings:
            loc = settings["hero-start-loc"]
        pos = self.mapdisplay.loctopoint(loc)
        self.hero.x, self.hero.y = pos
        self.input = dict()
        self.hero.world = self.mapdisplay
        self.hero.checkpoint = (self.hero.level,loc)
        self.statusbar = StatusBar()
        self.dialog = DialogBox()
        Game.start(self)
    def gameloop(self):
        """The game loop"""
        while self.gamealive:
            deltatime = self.clock.tick(self.fps)
            self.input["deltatime"] = deltatime
            for event in pg.event.get():
                if event.type == QUIT:
                    self.close()
                elif event.type == KEYDOWN:
                    self.input[event.key] = True
                    if event.key == K_SPACE:
                        self.dialog.next()
                    if event.key == K_u:
                        self.dialog.say("hello "+str(random.randint(0,100)))
                        self.dialog.show()
                    if event.key == K_p:
                        #Print when necessary
                        print self.mapdisplay.allitems
                        print self.mapdisplay.items
                elif event.type == KEYUP:
                    del self.input[event.key]
                elif event.type == MOUSEBUTTONDOWN:
                    print "mouse clic",event.pos,self.mapdisplay.pointtoloc(event.pos)
            self.hero.update(self.input, self.dialog)    
            #Casual prints
            #Draw everything and update
            self.screen.fill(colors.white)
            self.mapdisplay.draw(self.screen)
            self.hero.draw(self.screen)
            self.statusbar.say("Money:"+str(self.hero.money),self.screen)
            self.dialog.draw(self.screen)
            pg.display.update()



if __name__ == '__main__':
    game = None
    try:
        settingsfile = open('settings.json')
        settings = json.load(settingsfile)
        game = AdvGame(settings)
    except Exception as ex:
        print type(ex),ex
        traceback.print_exc()
        pg.quit()

        
