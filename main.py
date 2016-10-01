#Pygame Template File

import traceback,sys
import pygame as pg
from pygame.locals import *
import numpy as np


WIDTH = 640
HEIGHT = 480
FPS = 40

def init():
    """Initialize PyGame"""
    pg.init()
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    pg.display.set_caption("My Window")
    clock = pg.time.Clock()
    begin(screen,clock)
def begin(screen,clock):
    """Starting the game, call again for restart"""
    gameLoop(screen,clock)
def gameLoop(screen,clock):
    """The game loop"""
    while True:
        deltaTIme = clock.tick(FPS)
        for event in pg.event.get():
            if event.type == QUIT:
                close()
            #Add events conditions
        pg.display.update()
def close():
    """Quit and exit"""
    print "Bye"
    pg.quit()
    sys.exit()

if __name__ == '__main__':
    try:
        init()
    except Exception as ex:
        print type(ex),ex
        traceback.print_exc()
        close()
    
    
