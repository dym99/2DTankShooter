 ###########################
#                           #
#   2D Tank Shooter Game    #
#       MAP EDITOR          #
#                           #
 ###########################


import pygame,sys,math
from pygame import *


pygame.init()
NAME = input("Enter Map Name > ")
BACK = input("Background Tile > ")
tnksp = pygame.image.load("images/tank_base.png")
backtile = pygame.image.load("images/tiles/"+BACK+".png")
sandstone = pygame.image.load("images/tiles/sandstone.png")
grasscliff = pygame.image.load("images/tiles/grasscliff.png")
water = pygame.image.load("images/tiles/water_00.png")
water_0 = pygame.image.load("images/tiles/water_00.png")
water_1 = pygame.image.load("images/tiles/water_01.png")
sand = pygame.image.load("images/tiles/sand.png")
grass = pygame.image.load("images/tiles/grass.png")

black = [0,0,0,255]
green = [0,255,0,255]

edges = ["ctl","ctc","ctr","ccl","","ccr","cbl","cbc","cbr"]

class Tile:
    def __init__(self,pos,img,imgstr,solid):
        self.pos = pos
        self.img = img
        self.imgstr = imgstr
        self.solid = solid
    def getHitbox(self):
        rect = pygame.Rect(self.pos[0],self.pos[1],32,32)
        return rect


class Map:
    def __init__(self,name,tiles,backtile,size,spawns):
        self.tiles = tiles
        self.backtile = backtile
        self.size = size
        self.spawns = spawns

class Spawn(Tile):
    def __init__(self,pos):
        self.pos = pos
        self.img = tnksp
        self.imgstr = "sp"
        self.imgpos = (pos[0]-8,pos[1]-8)
    def getHitbox(self):
        rect = pygame.Rect(self.pos[0],self.pos[1],32,32)
        return rect

class Water(Tile):
    def __init__(self,pos,solid):
        self.pos = pos
        self.img = water
        self.imgstr = "water_00"
        self.imgs = [water_0,water_1]
        self.frame = 0
        self.ticks = 0
        self.solid = solid
        self.hitbox = pygame.Rect(self.pos[0],self.pos[1],32,32)
    def anim(self):
        self.ticks += 1
        if self.ticks > 5:
            self.ticks = 0
            self.frame+=1
            if self.frame > len(self.imgs)-1:
                self.frame = 0
            self.img = self.imgs[self.frame]

print("Launching Editor...")

size = width,height = (1360,960)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tank Shooter Map Editor")

NewMap = Map(NAME,[],backtile,(1280,960),[])

buttons = []
buttons.append(Tile([41*32,32],sandstone,"sandstone",0))
buttons.append(Tile([41*32,32*3],grasscliff,"grasscliff",0))
buttons.append(Water([41*32,32*5],0))
buttons.append(Spawn([41*32,32*7]))

currentTile = sandstone
while True:
    print(currentTile.imgstr)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[K_s]:
                file = open("maps/"+NAME+".tsmap",'w')
                file.write("# options \n")
                file.write("map_name "+NAME+"\n")
                file.write("back_tile "+BACK+"\n")
                file.write("map_size 1280 960 \n")
                file.write("# end options \n")
                
                for t in NewMap.tiles:
                    if type(t) == Water:
                        file.write("water "+str(int(t.pos[0]/32))+" "+str(int(t.pos[1]/32))+"\n")
                    else:
                        file.write("tile "+str(int(t.pos[0]/32))+" "+str(int(t.pos[1]/32))+" "+t.imgstr + " 1 \n")
                file.close()
        if event.type == MOUSEBUTTONDOWN:
            mpos = x,y = pygame.mouse.get_pos()
            for b in buttons:
                if b.getHitbox().collidepoint(mpos):
                    currentTile = b.img
                    
            if mpos[0] < 1280:
                if event.button == 1:
                    if currentTile == sandstone:
                        t = Tile([x-x%32,y-y%32],currentTile,"sandstone",1)
                        NewMap.tiles.append(t)
                    elif currentTile == grasscliff:
                        t = Tile([x-x%32,y-y%32],currentTile,"grasscliff",1)
                        NewMap.tiles.append(t)
                    elif currentTile == water:
                        t = Water([x-x%32,y-y%32],0)
                        NewMap.tiles.append(t)
                    elif currentTile == tnksp:
                        t = Spawn([x-x%32,y-y%32])
                else:
                    for t in NewMap.tiles:
                        if t.getHitbox().collidepoint(mpos):
                            NewMap.tiles.remove(t)

    for t in NewMap.tiles:
        if type(t) == Water:
            t.anim()
    
    screen.fill(black)
    for y in range(30):
        for x in range(40):
            screen.blit(backtile,(x*32,y*32))

    for b in buttons:
        if type(b) != Spawn:
            screen.blit(b.img, (b.pos[0],b.pos[1]))
        else:
            screen.blit(b.img, b.imgpos)

    for t in NewMap.tiles:
        if type(t) != Spawn:
            screen.blit(t.img,t.getHitbox())
        else:
            screen.blit(t.img,t.imgpos)

    mpos = x,y = pygame.mouse.get_pos()
    pygame.draw.rect(screen,green,pygame.Rect(x-x%32, y-y%32, 32, 32),2)
    pygame.display.flip()
    pygame.time.wait(10)
