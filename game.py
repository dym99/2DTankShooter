 ###########################
#                           #
#   2D Tank Shooter Game    #
#                           #
 ###########################


import math,sys,pygame,socket,random
from pygame import *
from math import radians, sin, cos, tan, pi, atan2
pygame.init()
pygame.key.set_repeat(20)

tank_base_img = pygame.image.load("images/tank_base.png")
tank_gun_img = pygame.image.load("images/tank_gun.png")
tank_rubble_img = pygame.image.load("images/tank_rubble.png")
crosshair = pygame.image.load("images/crosshair.png")
explosion = []
epl0 = pygame.image.load("images/expl_00.png")
epl1 = pygame.image.load("images/expl_01.png")
epl2 = pygame.image.load("images/expl_02.png")
epl3 = pygame.image.load("images/expl_03.png")
epl4 = pygame.image.load("images/expl_04.png")
explosion.append(epl0)
explosion.append(epl1)
explosion.append(epl2)
explosion.append(epl3)
explosion.append(epl4)
explosion.append(epl4)
explosion.append(epl4)
explosion.append(epl4)
explosion.append(epl4)
explosion.append(epl4)
explosion.append(epl4)
explosion.append(epl4)
explosion.append(epl4)
explosions = []

edges = ["ctl","ctc","ctr","ccl","","ccr","cbl","cbc","cbr"]

water_0 = pygame.image.load("images/tiles/water_00.png")
water_1 = pygame.image.load("images/tiles/water_01.png")

pygame.mouse.set_visible(False)
font = pygame.font.SysFont("Arial",20)
black = [0,0,0,255]
grey = [127,127,127,255]
white = [255,255,255,255]
red = [255,0,0,255]
green = [0,255,0,255]
blue = [0,0,255,255]
moving = False
class Tank:
    def __init__(self,startposition,gamertag, startdir):
        self.pos = startposition
        self.speed = 0
        self.alive = True
        self.health = 100
        self.baseimg = tank_base_img
        self.tag = gamertag
        self.movdir = startdir
        self.aimdir = startdir
    def getHitbox(self):
        return pygame.Rect(self.pos[0]-24,self.pos[1]-24,48,48)
    def move(self):
        if self.alive:
            self.pos[0] = int(self.pos[0] + self.speed*cos((-self.movdir+90)*pi/180)) % width
            self.pos[1] = int(self.pos[1] + self.speed*sin((-self.movdir+90)*pi/180)) % height
    def updateGunAngle(self):
        mpos = pygame.mouse.get_pos()
        self.aimdir = ((180-atan2(mpos[1]-self.pos[1],mpos[0]-self.pos[0])*180/pi))+90
    def die(self):
        if self.alive:
            self.alive = False
            explosions.append(Explosion(self.pos))
            explosions.append(Explosion([self.pos[0]-16,self.pos[1]-16]))
            explosions.append(Explosion([self.pos[0]-16,self.pos[1]+16]))
            explosions.append(Explosion([self.pos[0]+16,self.pos[1]-16]))
            explosions.append(Explosion([self.pos[0]+16,self.pos[1]+16]))
            

class Explosion:
    def __init__(self,pos):
        self.pos = pos
        self.frame = 0
    def anim(self):
        self.frame += 1
        if self.frame >= 12:
            explosions.remove(self)
    def getImage(self):
        return explosion[int(self.frame)]

class Tile:
    def __init__(self,pos,img,solid):
        self.pos = pos
        self.img = img
        self.solid = solid
        self.hitbox = pygame.Rect(self.pos[0],self.pos[1],32,32)
        
class Water(Tile):
    def __init__(self,pos,solid):
        self.pos = pos
        self.img = water_0
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
        

class Map:
    def __init__(self,name,tiles,backtile,size,spawns):
        self.tiles = tiles
        self.backtile = backtile
        self.size = size
        self.spawns = spawns

def loadMap(mapfile):
    file = open("maps/" + mapfile + ".tsmap")
    map_name = mapfile
    back_tile = None
    map_size = (1280,960)
    tiles = []
    spawns = []
    for l in file:
        w = l.split()
        if len(w)>0:
            if w[0] == "#":
                pass
            elif w[0] == "map_name":
                map_name = w[1]
            elif w[0] == "back_tile":
                back_tile = pygame.image.load("images/tiles/" + w[1] + ".png")
            elif w[0] == "map_size":
                map_size = (int(w[1])*32,int(w[2])*32)
            elif w[0] == "tile":
                tile = Tile([int(w[1])*32,int(w[2])*32],pygame.image.load("images/tiles/"+w[3]+".png"),int(w[4]))
                tiles.append(tile)
            elif w[0] == "water":
                tile = Water([int(w[1])*32,int(w[2])*32],0)
                tiles.append(tile)
            elif w[0] == "tank":
                spawns.append([int(w[1])*32, int(w[2])*32])
    file.close()
    newmap = Map(map_name,tiles,back_tile,map_size,spawns)
    return newmap

class Bullet:
    def __init__(self, pos, movdir, accuracy):
        self.pos = pos
        self.speed = 10
        self.movdir = movdir + accuracy
    def move(self):
        self.pos[0] = int(self.pos[0] + self.speed*cos((-self.movdir+90)*pi/180))
        self.pos[1] = int(self.pos[1] + self.speed*sin((-self.movdir+90)*pi/180))
        if self.pos[0] > width:
            self.pos[0] = width
            self.remove()
        elif self.pos[0] < 0:
            self.pos[0] = 0
            self.remove()
        elif self.pos[1] > height:
            self.pos[1] = height
            self.remove()
        elif self.pos[1] < 0:
            self.pos[1] = 0
            self.remove()
    def remove(self):
        explode = Explosion(self.pos)
        explosions.append(explode)
        bullets.remove(self)
        
        
c = False
cc = False
b = False
f = False


CurrentMap = loadMap("oasis")
size = width, height = (1280,960)
#My dimensions 1366 and 768 ---> Griffin try 1280 and 960 too if those work then perfect.
#1280,960
screen = pygame.display.set_mode(size,FULLSCREEN)

bullets = []

if len(CurrentMap.spawns)>0:
    tank = Tank(CurrentMap.spawns[0],"YOU", -90)
else:
    tank = Tank([64,64],"YOU", -90)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if tank.alive:
            c = keys[K_d]
            cc = keys[K_a]
            f = keys[K_w]
            b = keys[K_s]
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                tankpos = [tank.pos[0],tank.pos[1]]
                bullet = Bullet(tankpos,tank.aimdir + 180, random.randint(-5,5))
                bullets.append(bullet)
                tank.b = False
        else:
            c = False
            cc = False
            f = False
            b = False
        if keys[K_p]:
            tank.health -= 1
        if tank.health < 1:
            tank.health = 0
            tank.die()
    movspeed = 0
    if f:
        movspeed -= 3
    if b:
        movspeed += 3
    tank.speed = movspeed
    tank.move()
    if cc:
        tank.movdir+=5
    if c:
        tank.movdir-=5
    else:
        moving = True
    tank.updateGunAngle()

    for bullet in bullets:
        bullet.move()

    for explode in explosions:
        explode.anim()

    ###############################

    tHit = tank.getHitbox()
    for t in CurrentMap.tiles:
        if type(t) == Water:
            t.anim()
        if tHit.colliderect(t.hitbox):
            if abs(tHit.y+8 - t.hitbox.y)<32:
                tank.pos[0] = t.hitbox.right+24
                if tHit.x < t.hitbox.x:
                    tank.pos[0] = t.hitbox.left-24
                
            if abs(tHit.x+8 - t.hitbox.x)<32:
                tank.pos[1] = t.hitbox.top-24
                if tHit.y > t.hitbox.y:
                    tank.pos[1] = t.hitbox.bottom+24
        for bullet in bullets:
            if type(t) != Water:
                if t.hitbox.collidepoint((bullet.pos[0],bullet.pos[1])):
                    bullet.remove()
                

    
    screen.fill(black)

    ###############################
    
    for y in range(30):
        for x in range(40):
            screen.blit(CurrentMap.backtile,(x*32,y*32))
    
    if tank.alive:
        transimg = pygame.transform.rotate(tank.baseimg,tank.movdir)
        screen.blit(transimg, pygame.Rect(tank.pos[0]-transimg.get_rect().height/2,tank.pos[1]-transimg.get_rect().width/2,48,48))
        transimg = pygame.transform.rotate(tank_gun_img,tank.aimdir)
        screen.blit(transimg, pygame.Rect(tank.pos[0]-transimg.get_rect().height/2,tank.pos[1]-transimg.get_rect().width/2,48,48))
    else:
        transimg = pygame.transform.rotate(tank_rubble_img,tank.movdir)
        screen.blit(transimg, pygame.Rect(tank.pos[0]-transimg.get_rect().height/2,tank.pos[1]-transimg.get_rect().width/2,48,48))
    for t in CurrentMap.tiles:
        screen.blit(t.img,pygame.Rect((t.pos[0],t.pos[1],32,32)))
    for explode in explosions:
        screen.blit(explode.getImage(), pygame.Rect(explode.pos[0]-16,explode.pos[1]-16,32,32))
    mpos = x,y = pygame.mouse.get_pos()
    for bullet in bullets:
        pygame.draw.circle(screen, white, (bullet.pos[0],bullet.pos[1]), 3)
    screen.blit(crosshair, pygame.Rect(x-16,y-16,32,32))
    ##### HUD code goes here #####
    
    pygame.draw.rect(screen, black, pygame.Rect(width-210,10,200,20))
    pygame.draw.rect(screen, red, pygame.Rect(width-210,10,tank.health*2,20))
    pygame.draw.rect(screen, grey, pygame.Rect(width-210,10,200,20),3)

    #########

    pygame.display.flip()
    pygame.time.wait(5)
