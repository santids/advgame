import pygame as pg
from pygame.locals import *
import numpy as np
import traceback,sys
from display.mapdisplay import MapDisplay
from hero import Hero
import display.colors as colors
import utils.vect2d as vect


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
        Game.__init__(self,settings["width"],settings["height"],caption="Adventure Game")
    def start(self):
        """Start the game"""

        self.displaylist = []
        self.mapdisplay = MapDisplay((3,3),"levels/level1.json")
        self.hero = Hero()
        loc = vect.div(self.mapdisplay.shape,2)
        pos = self.mapdisplay.loctopoint(loc)
        self.hero.x, self.hero.y = pos
        self.input = dict()
        self.hero.world = self.mapdisplay
        Game.start(self)
    def gameloop(self):
        """The game loop"""
        while self.gamealive:
            deltatime = self.clock.tick(self.fps)
            for event in pg.event.get():
                if event.type == QUIT:
                    self.close()
                elif event.type == KEYDOWN:
                    self.input[event.key] = True
                elif event.type == KEYUP:
                    del self.input[event.key]
                elif event.type == MOUSEBUTTONDOWN:
                    print "mouse clic",event.pos,self.mapdisplay.pointtoloc(event.pos)
            self.hero.handleinput(self.input)    
                    
            #Draw everything and update
            self.mapdisplay.draw(self.screen)
            self.hero.draw(self.screen)
            pg.display.update()



if __name__ == '__main__':
    game = None
    try:
        settings ={"width":640,"height":480}
        game = AdvGame(settings)
    except Exception as ex:
        print type(ex),ex
        traceback.print_exc()
        pg.quit()

        
