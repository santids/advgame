from display.mob import Mob
import pygame as pg
from pygame.locals import *
import display.colors as colors
import math,random
import artefacts
from display.tileinfo import TileMgr
from display.spritesheet import Sheet
import os.path

class Hero(Mob):
    def __init__(self,settings):
        Mob.__init__(self)
        self.level = "0"
        self.checkpoint = None
        self.width = self.height = 15
        self.world = None
        self.speed = 10
        self.money= 0
        self.bag = []
        self.settings = settings
        self.dir = 1
        self.idle = True
        self.sheet = Sheet('assets/images/hero.png',self.width)
        self.oldinput = dict()
    def handleinput(self,input,dialog):
        if K_UP in input or K_DOWN in input or K_LEFT in input or K_RIGHT in input:
            self.idle = False
        else:
            self.idle = True
        self.handlemovement(input)
        if K_b in input:
            dialog.say(self.printbag())
        if K_r in input:
            self.respawn()
        if not self.idle:
            dialog.next()
            dialog.hide()
    def update(self,input, dialog):
        self.handleinput(input,dialog)
        centerloc = self.world.pointtoloc(self.center())
        tilemgr = TileMgr()
        if centerloc in self.world.portals:
            newlevel = self.world.portals[centerloc][0]
            newloc = self.world.portals[centerloc][1:]
            self.spawn(newlevel,newloc)
        elif centerloc in self.world.items:
            item = self.world.items[centerloc]
            if item[0] == 'coin':
                self.money += int(item[1])
                del self.world.items[centerloc]
            elif item[0] == 'sign':
                #dialog.main_message = item[1]
                dialog.sayAll(item[1:])
            elif item[0] == 'shoes' and K_SPACE in input:
                self.speed = int(self.speed*float(item[1]))
                del self.world.items[centerloc]
            elif K_g in input:
                #Grab intems
                self.bag.append(item)
                del self.world.items[centerloc]
            else:
                dialog.main_message = " ".join(item)
        elif centerloc in self.world.switches:
            if K_SPACE in input and K_SPACE not in self.oldinput:
                targetloc = tuple(self.world.switches[centerloc])
                if targetloc in self.world.artefacts:
                    artefact = self.world.artefacts[targetloc]
                    if artefact[1] == "off":
                        artefact[1] = "on"
                    elif artefact[1] == "on":
                        artefact[1] = "off"
                    artefacts.act(artefact,targetloc,self.world,self)
        elif centerloc in self.world.artefacts:
            dialog.main_message = " ".join(self.world.artefacts[centerloc])

        elif dialog.main_message != "":
            dialog.hide()
            dialog.next()
        if tilemgr.tile(self.world.map[centerloc]).description == "checkpoint":
            if K_SPACE in input:
                if self.checkpoint != (self.level, centerloc):
                    self.checkpoint = (self.level, centerloc)
        if tilemgr.tile(self.world.map[centerloc]).kills:
            self.die()
        self.oldinput = input.copy()

    def spawn(self,level,loc):
        """Appear anywhere in the whole map"""
        newpos = self.world.loctopoint(loc)
        self.x = newpos[0]+(self.world.tsize-self.width)/2
        self.y = newpos[1]+(self.world.tsize-self.height)/2
        if self.level != level:
            levelpath = self.settings["level-path"]
            tmppath = os.path.join(levelpath,"tmp")
            oldname = self.settings["level-prefix"]+self.level+".json"
            newname = self.settings["level-prefix"]+level+".json"

            self.world.dumplevel(os.path.join(tmppath,oldname )) 
            if os.path.isfile(os.path.join(tmppath,newname)):
                self.world.loadlevel(os.path.join(tmppath,newname))
            else:
                self.world.loadlevel(os.path.join(levelpath,newname))
            self.level = level

    def respawn(self):
        """Reappear in your last checkpoint"""
        self.dir = 1
        self.spawn(self.checkpoint[0], self.checkpoint[1])
    def die(self):
        """Die and respawn"""
        self.money = 0
        self.bag = []
        self.respawn()
    def handlemovement(self,input):
        tilemgr = TileMgr()
        deltax = int(math.ceil( self.speed*input["deltatime"]/100))
        if K_UP in input:
            self.dir = 0
            self.moveup(deltax)
            loc1 = self.world.pointtoloc(self.topleft())
            loc2 = self.world.pointtoloc(self.topright())
            loc3 = self.world.pointtoloc(self.up())
            tile1 = tilemgr.tile(self.world.map[loc1])
            tile2 = tilemgr.tile(self.world.map[loc2])
            tile3 = tilemgr.tile(self.world.map[loc3])
            if tile1.isobstacle or tile2.isobstacle:
                cloc = self.world.pointtoloc(self.center())
                lpos = self.world.loctop(cloc)
                self.movedown(abs(lpos-self.y))

            if tile1.isobstacle and not tile3.isobstacle:
                self.moveright(1)
            if tile2.isobstacle and not tile3.isobstacle:
                self.moveleft(1)

        if K_DOWN in input:
            self.dir = 1
            self.movedown(deltax)
            loc1 = self.world.pointtoloc(self.bottomleft())
            loc2 = self.world.pointtoloc(self.bottomright())
            loc3 = self.world.pointtoloc(self.down())
            tile1 = tilemgr.tile(self.world.map[loc1])
            tile2 = tilemgr.tile(self.world.map[loc2])
            tile3 = tilemgr.tile(self.world.map[loc3])
            if tile1.isobstacle or tile2.isobstacle:
                cloc = self.world.pointtoloc(self.center())
                lpos = self.world.locbottom(cloc)
                self.moveup(abs(lpos-self.down()[1])+1)
            if tile1.isobstacle and not tile3.isobstacle:
                self.moveright(1)
            if tile2.isobstacle and not tile3.isobstacle:
                self.moveleft(1)
        if K_LEFT in input:
            self.dir = 3
            self.moveleft(deltax)
            loc1 = self.world.pointtoloc(self.topleft())
            loc2 = self.world.pointtoloc(self.bottomleft())
            loc3 = self.world.pointtoloc(self.left())
            tile1 = tilemgr.tile(self.world.map[loc1])
            tile2 = tilemgr.tile(self.world.map[loc2])
            tile3 = tilemgr.tile(self.world.map[loc3])
            if tile1.isobstacle or tile2.isobstacle:
                cloc = self.world.pointtoloc(self.center())
                lpos = self.world.locleft(cloc)
                self.moveright(abs(lpos-self.left()[0])+1)
            if tile1.isobstacle and not tile3.isobstacle:
                self.movedown(1)
            if tile2.isobstacle and not tile3.isobstacle:
                self.moveup(1)
        if K_RIGHT in input:
            self.dir = 2
            self.moveright(deltax)
            loc1 = self.world.pointtoloc(self.bottomright())
            loc2 = self.world.pointtoloc(self.topright())
            loc3 = self.world.pointtoloc(self.right())
            tile1 = tilemgr.tile(self.world.map[loc1])
            tile2 = tilemgr.tile(self.world.map[loc2])
            tile3 = tilemgr.tile(self.world.map[loc3])
            if tile1.isobstacle or tile2.isobstacle:
                cloc = self.world.pointtoloc(self.center())
                lpos = self.world.locright(cloc)
                self.moveleft(abs(lpos-self.right()[0])+1)
            if tile1.isobstacle and not tile3.isobstacle:
                self.moveup(1)
            if tile2.isobstacle and not tile3.isobstacle:
                self.movedown(1)

    def draw(self,surface):
        #pg.draw.rect(surface,colors.red6,(self.x,self.y,self.width,self.height))
        image = self.sheet.image_num(self.dir)
        surface.blit(image,(self.x,self.y,self.width,self.height))
    def printbag(self):
        """ Print items in bag"""
        l = []
        for el in self.bag:
            nel = " ".join(el)
            l.append(nel)
        return '| '.join(l)
