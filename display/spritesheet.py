import pygame as pg
from pygame.locals. import *


class spriteSheet():
    def __init__(self, filename):
        self.filename = filename
        self.sheet = pg.image.load(filename):
