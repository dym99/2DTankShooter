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
tank_base_img2 = pygame.image.load("images/tank_base_2.png")
tank_gun_img = pygame.image.load("images/tank_gun.png")
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

pygame.mouse.set_visible(False)
health = 100
font = pygame.font.SysFont("Arial",20)
black = [0,0,0,255]
white = [255,255,255,255]
red = [255,0,0,255]
blue = [0,255,0,255]
green = [0,0,255,255]
moving = False
class Tank:
    def __init__(self,startposition,gamertag, startdir):
        self.pos = startposition
        self.speed = 0
        self.baseimg = tank_base_img
        self.tag = gamertag
        self.movdir = startdir
        self.aimdir = startdir
    def move(self):
        self.pos[0] = int(self.pos[0] + self.speed*cos((-self.movdir+90)*pi/180)) % width
        self.pos[1] = int(self.pos[1] + self.speed*sin((-self.movdir+90)*pi/180)) % height
    def updateGunAngle(self):
        mpos = pygame.mouse.get_pos()
        self.aimdir = ((180-atan2(mpos[1]-self.pos[1],mpos[0]-self.pos[0])*180/pi))+90
    def anim(self):
        if self.baseimg == tank_base_img:
            self.baseimg = tank_base_img2
        else:
            self.baseimg = tank_base_img

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
    def __init__(self,pos,img):
        self.pos = pos
        self.img = img

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
size = width, height = (1366,768)
#My dimensions 1366 and 768
#1200, and 900
screen = pygame.display.set_mode(size,FULLSCREEN)

bullets = []

tank = Tank([48,48],"YOU", -90)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        keys = pygame.key.get_pressed()
        c = keys[K_d]
        cc = keys[K_a]
        f = keys[K_w]
        b = keys[K_s]
        if event.type == MOUSEBUTTONDOWN:
            bullet = Bullet([tank.pos[0],tank.pos[1]],tank.aimdir + 180, random.randint(-5,5))
            bullets.append(bullet)
        if keys[K_p] == False:
            health -= 5
        if health < 1:
            pygame.quit()
            sys.exit()
    if moving == True:
        moving = False
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
        if tank.speed > 0:
            tank.anim()
    else:
        moving = True
    tank.updateGunAngle()

    for bullet in bullets:
        bullet.move()

    for explode in explosions:
        explode.anim()
    ###########
    
    screen.fill(black)
    for bullet in bullets:
        pygame.draw.circle(screen, white, (bullet.pos[0],bullet.pos[1]), 3)
    transimg = pygame.transform.rotate(tank.baseimg,tank.movdir)
    screen.blit(transimg, pygame.Rect(tank.pos[0]-transimg.get_rect().height/2,tank.pos[1]-transimg.get_rect().width/2,48,48))
    transimg = pygame.transform.rotate(tank_gun_img,tank.aimdir)
    screen.blit(transimg, pygame.Rect(tank.pos[0]-transimg.get_rect().height/2,tank.pos[1]-transimg.get_rect().width/2,48,48))
    mpos = x,y = pygame.mouse.get_pos()
    for explode in explosions:
        screen.blit(explode.getImage(), pygame.Rect(explode.pos[0]-16,explode.pos[1]-16,32,32))
    screen.blit(crosshair, pygame.Rect(x-16,y-16,32,32))
    ##### text code goes here
    ### this is suitable for my computer
    renderedText = font.render("Health: "+str(health),1,red)
    screen.blit(renderedText, (width - 100,10))

    #########

    pygame.display.flip()
    pygame.time.wait(10)
