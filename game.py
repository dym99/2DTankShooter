 ###########################
#                           #
#   2D Tank Shooter Game    #
#                           #
 ###########################


import math,sys,pygame,socket,random
from pygame import *
from math import radians, sin, cos,pi
pygame.init()
pygame.key.set_repeat(20)

tank_base_img = pygame.image.load("images/tank_base.png")
tank_gun_img = pygame.image.load("images/tank_gun.png")
crosshair = pygame.image.load("images/crosshair.png")

black = [0,0,0,255]
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

size = width, height = (640,480)
screen = pygame.display.set_mode(size)

tank = Tank([48,48],"YOU", 0)
while True:
    moving = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[K_a]:
                tank.movdir+=5
            if keys[K_d]:
                tank.movdir-=5
            if keys[K_w]:
                moving = True

    if moving == True:
        tank.move()

    ###########

    screen.fill(black)
    transimg = pygame.transform.rotate(tank_base_img,tank.movdir)
    screen.blit(transimg, pygame.Rect(tank.pos[0]-transimg.get_rect().height/2,tank.pos[1]-transimg.get_rect().width/2,48,48))
    mpos = x,y = pygame.mouse.get_pos()
    screen.blit(crosshair, pygame.Rect(x-16,y-16,32,32))
    pygame.display.flip()
    pygame.time.wait(10)
