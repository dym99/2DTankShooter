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
crosshair = pygame.image.load("images/crosshair.png")
pygame.mouse.set_visible(False)
black = [0,0,0,255]
white = [255,255,255,255]
moving = False
class Tank:
    def __init__(self,startposition,gamertag, startdir):
        self.pos = startposition
        self.speed = 3
        self.tag = gamertag
        self.movdir = startdir
        self.aimdir = startdir
    def move(self):
        self.pos[0] = int(self.pos[0] + self.speed*cos((-self.movdir+90)*pi/180)) % width
        self.pos[1] = int(self.pos[1] + self.speed*sin((-self.movdir+90)*pi/180)) % height
    def updateGunAngle(self):
        mpos = pygame.mouse.get_pos()
        self.aimdir = ((180-atan2(mpos[1]-self.pos[1],mpos[0]-self.pos[0])*180/pi))+90

class Bullet:
    def __init__(self, pos, movdir, accuracy):
        self.pos = pos
        self.speed = 10
        self.movdir = movdir + accuracy
    def move(self):
        self.pos[0] = int(self.pos[0] + self.speed*cos((-self.movdir+90)*pi/180))
        self.pos[1] = int(self.pos[1] + self.speed*sin((-self.movdir+90)*pi/180))
        if self.pos[0] > width or self.pos[0] < 0:
            bullets.remove(self)
        if self.pos[1] > height or self.pos[1] < 0:
            bullets.remove(self)
        
        

size = width, height = (640,480)
screen = pygame.display.set_mode(size)

bullets = []

tank = Tank([48,48],"YOU", 0)
while True:
    moving = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            if keys[K_d]:
                tank.movdir-=5
            if keys[K_w]:
                moving = True
        if event.type == MOUSEBUTTONDOWN:
            bullet = Bullet([tank.pos[0],tank.pos[1]],tank.aimdir + 180, random.randint(-5,5))
            bullets.append(bullet)
    if moving == True:
        tank.move()
    tank.updateGunAngle()

    for bullet in bullets:
        bullet.move()
    ###########
    
    screen.fill(black)
    for bullet in bullets:
        pygame.draw.circle(screen, white, (bullet.pos[0],bullet.pos[1]), 3)
    transimg = pygame.transform.rotate(tank_base_img,tank.movdir)
    screen.blit(transimg, pygame.Rect(tank.pos[0]-transimg.get_rect().height/2,tank.pos[1]-transimg.get_rect().width/2,48,48))
    transimg = pygame.transform.rotate(tank_gun_img,tank.aimdir)
    screen.blit(transimg, pygame.Rect(tank.pos[0]-transimg.get_rect().height/2,tank.pos[1]-transimg.get_rect().width/2,48,48))
    mpos = x,y = pygame.mouse.get_pos()
    screen.blit(crosshair, pygame.Rect(x-16,y-16,32,32))
    pygame.display.flip()
    pygame.time.wait(10)
