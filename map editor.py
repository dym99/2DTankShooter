import pygame,sys,math
from pygame import *


pygame.init()
NAME = input("Enter Map Name > ")
backtile = pygame.image.load("images/tiles/"+input("Background Tile > ")+".png")
sandstone = pygame.image.load("images/tiles/sandstone.png")
grasscliff = pygame.image.load("images/tiles/grasscliff.png")
sand = pygame.image.load("images/tiles/sand.png")
grass = pygame.image.load("images/tiles/grass.png")

black = [0,0,0,255]
green = [0,255,0,255]

class Tile:
    def __init__(self,pos,img,solid):
        self.pos = pos
        self.img = img
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

print("Launching Editor...")

size = width,height = (1360,960)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tank Shooter Map Editor")

NewMap = Map(NAME,[],backtile,(1280,960),[])

buttons = []
buttons.append(Tile([41*32,32],sandstone,0))
buttons.append(Tile([41*32,32*3],grasscliff,0))

currentTile = sandstone
while True:
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
                backtxt = "sand"
                if NewMap.backtile == sand:
                    backtxt = "sand"
                elif NewMap.backtile == grass:
                    backtxt = "grass"
                file.write("back_tile "+backtxt+"\n")
                file.write("map_size 1280 960 \n")
                file.write("# end options \n")
                
                for t in NewMap.tiles:
                    imgtxt = "sandstone"
                    if t.img == sandstone:
                        imgtxt = "sandstone"
                    elif t.img == grasscliff:
                        imgtxt == "grasscliff"
                    file.write("tile "+str(int(t.pos[0]/32))+" "+str(int(t.pos[1]/32))+" "+imgtxt + " 1 \n")
                file.close()
        if event.type == MOUSEBUTTONDOWN:
            mpos = x,y = pygame.mouse.get_pos()
            for b in buttons:
                if b.getHitbox().collidepoint(mpos):
                    currentTile = b.img
            if mpos[0] < 1280:
                if event.button == 1:
                    t = Tile([x-x%32,y-y%32],currentTile,1)
                    NewMap.tiles.append(t)
                else:
                    for t in NewMap.tiles:
                        if t.getHitbox().collidepoint(mpos):
                            NewMap.tiles.remove(t)

    screen.fill(black)
    for y in range(30):
        for x in range(40):
            screen.blit(backtile,(x*32,y*32))

    for b in buttons:
        screen.blit(b.img, (b.pos[0],b.pos[1]))

    for t in NewMap.tiles:
        screen.blit(t.img,t.getHitbox())

    mpos = x,y = pygame.mouse.get_pos()
    pygame.draw.rect(screen,green,pygame.Rect(x-x%32, y-y%32, 32, 32),2)
    pygame.display.flip()
    pygame.time.wait(10)
