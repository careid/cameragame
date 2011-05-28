import pygame
import os
import random

class Player():
    def __init__(self,x,y):
        self.x = x*32
        self.y = y*32
        self.xVelocity = 0
        self.yVelocity = 0
        self.frame = 0
        self.health = 10
        #self.images = [pygame.image.load("picture.png")]
        playerImage = pygame.Surface((32,32))
        playerImage.fill((255,0,0))
        playerImage.set_colorkey((0,0,0))
        self.action = "walk"
        self.images = [[pygame.image.load("graphics\\frontwalk1.png"),pygame.image.load("graphics\\frontwalk2.png"),pygame.image.load("graphics\\frontwalk3.png"),pygame.image.load("graphics\\frontwalk4.png")],
                       [pygame.image.load("graphics\\frontwalk1.png"),pygame.image.load("graphics\\frontwalk2.png"),pygame.image.load("graphics\\frontwalk3.png"),pygame.image.load("graphics\\frontwalk4.png")],
                       [pygame.image.load("graphics\\frontwalk1.png"),pygame.image.load("graphics\\frontwalk2.png"),pygame.image.load("graphics\\frontwalk3.png"),pygame.image.load("graphics\\frontwalk4.png")],
                       [pygame.image.load("graphics\\frontwalk1.png"),pygame.image.load("graphics\\frontwalk2.png"),pygame.image.load("graphics\\frontwalk3.png"),pygame.image.load("graphics\\frontwalk4.png")]]
        self.dir = 0
    def update(self):
        self.x += self.xVelocity
        self.y += self.yVelocity
        if (self.xVelocity>0):
            self.dir = 0
        elif (self.xVelocity<0):
            self.dir = 2
        elif (self.yVelocity <0):
            self.dir = 1
        elif (self.yVelocity > 0):
            self.dir = 3
        if (self.xVelocity != 0 or self.yVelocity !=0):
            self.play("walk")
        else:
            self.play("idle")
        if (self.action == "idle"):
            self.frame += 0.3
            if self.frame > 0:
                self.frame = 0
        elif (self.action == "walk"):
            self.frame += 0.3
            if self.frame > 3:
                self.frame = 0
    def play(self,action):
        if (self.action == action):
            return
        self.action = action
        if (self.action == "idle"):
            self.frame = 0
        elif (self.action == "walk"):
            self.frame = 0
    def draw(self,screen):
        screen.blit(self.images[self.dir][int(self.frame)],(self.x,self.y))

class Enemy():
    def __init__(self,path):
        self.x = 0
        self.y = 0
        self.superX = path[0][0]*32
        self.superY = path[0][1]*32
        self.xVelocity = 0
        self.yVelocity = 0
        self.frame = 0
        #self.images = [pygame.image.load("picture.png")]
        playerImage = pygame.Surface((32,32))
        playerImage.fill((105,0,0))
        self.images = [playerImage]
        self.path = path
        self.pathIndex = 0
        self.range = 3
        self.playerView = 0
        self.viewWidth = 30
        self.viewLength = 75
        self.action = "walk"
        self.images = [[pygame.image.load("graphics\\enemy1right.png")],
                       [pygame.image.load("graphics\\enemy1back.png")],
                       [pygame.image.load("graphics\\enemy1left.png")],
                       [pygame.image.load("graphics\\enemy1front.png")]]
        #self.images = [[pygame.image.load("graphics\\enemy0.png"),pygame.image.load("graphics\\enemy1.png"),pygame.image.load("graphics\\enemy2.png"),pygame.image.load("graphics\\enemy3.png")],
        #               [pygame.image.load("graphics\\enemy0.png"),pygame.image.load("graphics\\enemy1.png"),pygame.image.load("graphics\\enemy2.png"),pygame.image.load("graphics\\enemy3.png")],
        #               [pygame.image.load("graphics\\enemy0.png"),pygame.image.load("graphics\\enemy1.png"),pygame.image.load("graphics\\enemy2.png"),pygame.image.load("graphics\\enemy3.png")],
        #               [pygame.image.load("graphics\\enemy0.png"),pygame.image.load("graphics\\enemy1.png"),pygame.image.load("graphics\\enemy2.png"),pygame.image.load("graphics\\enemy3.png")]]
        self.dir = 0
    def update(self):
        tempIndex = self.pathIndex+1
        if (tempIndex>=len(self.path)):
            tempIndex = 0
            
        if (self.path[tempIndex][0]<self.path[self.pathIndex][0]):
            self.xVelocity = -1
        elif (self.path[tempIndex][0]>self.path[self.pathIndex][0]):
            self.xVelocity = 1
        if (self.path[tempIndex][1]<self.path[self.pathIndex][1]):
            self.yVelocity = -1
        elif (self.path[tempIndex][1]>self.path[self.pathIndex][1]):
            self.yVelocity = 1
            
        self.superX += self.xVelocity
        self.superY += self.yVelocity
        if (int(float(self.superX)/32+0.5)==self.path[tempIndex][0] and int(float(self.superY)/32+0.5)==self.path[tempIndex][1]):
            self.pathIndex += 1
            if (self.pathIndex>=len(self.path)):
                self.pathIndex = 0
        if (self.xVelocity>0):
            self.dir = 0
        elif (self.xVelocity<0):
            self.dir = 2
        elif (self.yVelocity <0):
            self.dir = 1
        elif (self.yVelocity > 0):
            self.dir = 3
        if (self.xVelocity != 0 or self.yVelocity !=0):
            self.play("walk")
        else:
            self.play("idle")
        if (self.action == "idle"):
            self.frame += 0.3
            if self.frame > 0:
                self.frame = 0
        elif (self.action == "walk"):
            self.frame += 0.3
            if self.frame > 0:
                self.frame = 0
    def play(self,action):
        if (self.action == action):
            return
        self.action = action
        if (self.action == "idle"):
            self.frame = 0
        elif (self.action == "walk"):
            self.frame = 0
    def draw(self,screen):
        screen.blit(self.images[self.dir][int(self.frame)],(self.x,self.y))
    def drawFOV(self,screen,tiles):
        if (self.x < 0):
            return None
        center = [self.x+16,self.y+16] 
        #pygame.draw.polygon(screen,(255,255,255),[center,[center[0]+45,center[1]-45],[center[0]+45,center[1]+45]])
        surf = pygame.Surface((self.viewLength*2,self.viewLength*2))
        x = int(float(self.x)/32+0.5)
        y = int(float(self.y)/32+0.5)
        size = self.viewLength
        width = self.viewWidth
        dir = 0
        if (self.xVelocity>0):
            dir = 0
        elif (self.yVelocity<0):
            dir = 1
        elif (self.xVelocity<0):
            dir = 2
        elif (self.yVelocity>0):
            dir = 3
        if (dir == 0):
            pygame.draw.polygon(surf,(255,255,255),[[size,size],[size+size,size-width],[size+size,size+width]])
            points = self.getShadow(0,1,2,center,x+1,y+1,tiles,size,surf)
            points = self.getShadow(0,1,2,center,x+2,y+1,tiles,size,surf)
            points = self.getShadow(0,1,2,center,x+3,y+1,tiles,size,surf)
            points = self.getShadow(0,2,2,center,x+1,y,tiles,size,surf)
            points = self.getShadow(0,2,2,center,x+2,y,tiles,size,surf)
            points = self.getShadow(0,2,2,center,x+3,y,tiles,size,surf)
            points = self.getShadow(0,2,1,center,x+1,y-1,tiles,size,surf)
            points = self.getShadow(0,2,1,center,x+2,y-1,tiles,size,surf)
            points = self.getShadow(0,2,1,center,x+3,y-1,tiles,size,surf)
        elif (dir == 1):
            pygame.draw.polygon(surf,(255,255,255),[[size,size],[size-width,0],[size+width,0]])
            points = self.getShadow(1,1,2,center,x+1,y-1,tiles,size,surf)
            points = self.getShadow(1,1,2,center,x+1,y-2,tiles,size,surf)
            points = self.getShadow(1,1,2,center,x+1,y-3,tiles,size,surf)
            points = self.getShadow(1,2,2,center,x,y-1,tiles,size,surf)
            points = self.getShadow(1,2,2,center,x,y-2,tiles,size,surf)
            points = self.getShadow(1,2,2,center,x,y-3,tiles,size,surf)
            points = self.getShadow(1,2,1,center,x-1,y-1,tiles,size,surf)
            points = self.getShadow(1,2,1,center,x-1,y-2,tiles,size,surf)
            points = self.getShadow(1,2,1,center,x-1,y-3,tiles,size,surf)
        elif (dir == 2):
            pygame.draw.polygon(surf,(255,255,255),[[size,size],[0,size-width],[0,size+width]])
            points = self.getShadow(2,1,2,center,x-1,y+1,tiles,size,surf)
            points = self.getShadow(2,1,2,center,x-2,y+1,tiles,size,surf)
            points = self.getShadow(2,1,2,center,x-3,y+1,tiles,size,surf)
            points = self.getShadow(2,2,2,center,x-1,y,tiles,size,surf)
            points = self.getShadow(2,2,2,center,x-2,y,tiles,size,surf)
            points = self.getShadow(2,2,2,center,x-3,y,tiles,size,surf)
            points = self.getShadow(2,2,1,center,x-1,y-1,tiles,size,surf)
            points = self.getShadow(2,2,1,center,x-2,y-1,tiles,size,surf)
            points = self.getShadow(2,2,1,center,x-3,y-1,tiles,size,surf)
        elif (dir == 3):
            pygame.draw.polygon(surf,(255,255,255),[[size,size],[size-width,size+size],[size+width,size+size]])
            points = self.getShadow(3,1,2,center,x+1,y+1,tiles,size,surf)
            points = self.getShadow(3,1,2,center,x+1,y+2,tiles,size,surf)
            points = self.getShadow(3,1,2,center,x+1,y+3,tiles,size,surf)
            points = self.getShadow(3,2,2,center,x,y+1,tiles,size,surf)
            points = self.getShadow(3,2,2,center,x,y+2,tiles,size,surf)
            points = self.getShadow(3,2,2,center,x,y+3,tiles,size,surf)
            points = self.getShadow(3,2,1,center,x-1,y+1,tiles,size,surf)
            points = self.getShadow(3,2,1,center,x-1,y+2,tiles,size,surf)
            points = self.getShadow(3,2,1,center,x-1,y+3,tiles,size,surf)
            
        surf.set_colorkey((0,0,0))
        surf.set_alpha(100)
        screen.blit(surf,(center[0]-self.viewLength,center[1]-self.viewLength))
        return pygame.mask.from_surface(surf,50)
        
    def getShadow(self,dir,a,b,center,x,y,tiles,size,surf):
        if (x >= len(tiles[0]) or y >= len(tiles) or checkCollidable(tiles[y][x])==0 or x*32 == center[0] or y*32 == center[1]):
            return 0
        x = x*32-center[0]
        y = y*32-center[1]

        if (dir==0):
            if (a==1):
                p1 = [x,y]
                p4 = [size,y]
            elif (a==2):
                p1 = [x,y]
                p4 = [size,size*(y)/(x)]

            if (b==1):
                p2 = [x,y+32]
                p3 = [size,y+32]
            elif (b==2):
                p2 = [x,y+32]
                p3 = [size,size*(y+32)/(x)]

        elif (dir==2):
            if (a==1):
                p1 = [x+32,y]
                p4 = [-size,y]
            elif (a==2):
                p1 = [x+32,y]
                p4 = [-size,-size*(y)/(x)]

            if (b==1):
                p2 = [x+32,y+32]
                p3 = [-size,y+32]
            elif (b==2):
                p2 = [x+32,y+32]
                p3 = [-size,-size*(y+32)/(x)]

        elif (dir==1):
            if (a==1):
                p1 = [x,y+32]
                p4 = [x,-size]
            elif (a==2):
                p1 = [x,y+32]
                p4 = [-size*(x)/(y+32),-size]

            if (b==1):
                p2 = [x+32,y+32]
                p3 = [x+32,-size]
            elif (b==2):
                p2 = [x+32,y+32]
                p3 = [-size*(x+32)/(y+32),-size]

        elif (dir==3):
            if (a==1):
                p1 = [x,y]
                p4 = [x,size]
            elif (a==2):
                p1 = [x,y]
                p4 = [size*(x)/(y),size]

            if (b==1):
                p2 = [x+32,y]
                p3 = [x+32,size]
            elif (b==2):
                p2 = [x+32,y]
                p3 = [size*(x+32)/(y),size]                

        #alter points
        p1[0]+=size
        p1[1]+=size
        p2[0]+=size
        p2[1]+=size
        p3[0]+=size
        p3[1]+=size
        p4[0]+=size
        p4[1]+=size
        pygame.draw.polygon(surf,(0,0,0),[p1,p2,p3,p4])
        return 1
        
class Controls():
    def __init__(self):
        self.W = 0
        self.A = 0
        self.S = 0
        self.D = 0
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
            elif event.type == pygame.KEYDOWN:
                if event.key ==  pygame.K_ESCAPE:
                    return 1
                elif event.key ==  pygame.K_a:
                    self.A = 1
                elif event.key ==  pygame.K_d:
                    self.D = 1
                elif event.key ==  pygame.K_s:
                    self.S = 1
                elif event.key ==  pygame.K_w:
                    self.W = 1
            elif event.type == pygame.KEYUP:
                if event.key ==  pygame.K_a:
                    self.A = 0
                elif event.key ==  pygame.K_d:
                    self.D = 0
                elif event.key ==  pygame.K_s:
                    self.S = 0
                elif event.key ==  pygame.K_w:
                    self.W = 0
        return 0

class Camera():
    def __init__(self,rect,x,y,scale=1):
        self.view = rect
        self.x = x
        self.y = y
        self.active = 0
        self.scale = scale
        self.white = 0
        self.maxWhite = 100

class Game():
    def __init__(self):
        pygame.init()
        self.menu = pygame.Surface((640,480))
        self.menu.fill((255,255,255))
        self.clock = pygame.time.Clock()
        self.controls = Controls()
        self.screen = pygame.display.set_mode((640,480))
        self.world = pygame.Surface((1000,1000))
        greenTile = pygame.Surface((32,32))
        blueTile = pygame.Surface((32,32))
        greenTile.fill((0,255,0))
        blueTile.fill((0,0,255))
        self.tileSize = 32
        i = 0
        self.tileImages = []
        while(os.path.exists("graphics\\tile"+str(i)+".png")):
            self.tileImages.append(pygame.image.load("graphics\\tile"+str(i)+".png"))
            i+=1
        self.wallTiles = []
        for i in range(0,10):
            self.wallTiles.append(pygame.Surface((32,32)))
            self.wallTiles[i].fill((30+i,30+i,30+i))
        self.floorTiles = []
        for i in range(0,10):
            self.floorTiles.append(pygame.Surface((32,32)))
            self.floorTiles[i].fill((100+i,100+i,100+i))
        pygame.mixer.music.load("The start.mp3")
        pygame.mixer.music.play(-1)
        #self.tileImages = [greenTile,blueTile]

    def restart(self,level):
        if level == 0: #level0
            self.tiles = [[20,20,20,20,20,20,20,20,20,20,20,0,0,0,0,0,0,0,0,0,0,0,0],
                          [20,21,21,20,20,20,20,21,21,21,21,1,1,1,1,1,1,1,1,1,1,1,0],
                          [20,21,21,20,20,21,21,21,21,21,21,1,1,1,1,1,1,1,1,1,1,1,0],
                          [20,21,21,20,20,21,21,21,20,20,20,0,0,1,1,1,1,1,1,1,1,1,0],
                          [20,21,21,21,21,21,21,20,20,21,21,1,1,1,1,1,1,1,1,1,1,1,0],
                          [20,20,20,20,20,20,20,20,20,21,21,1,1,1,1,1,1,1,1,1,1,1,0],
                          [20,20,20,20,20,20,20,20,20,21,21,1,1,1,1,1,1,1,1,1,1,1,0],
                          [0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1,1,1,1,0],
                          [0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,0],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                          [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
            self.player = Player(2,2)
            self.enemies = []
            self.enemies.append(Enemy([[13,2],[13,13]]))
            self.enemies.append(Enemy([[2,12],[20,12]]))
            self.enemies.append(Enemy([[3,8],[3,12]]))
            self.cameras = [Camera(pygame.Rect(0,0,32*6,32*6),0,0,.86), #1,1 SCREEN POSITIONS (1,1 is always top right).
                            Camera(pygame.Rect(32*5,0,32*7,32*7),32*6*.86,0,.86*.86),#2,1
                            Camera(pygame.Rect(32*11,0,32*6,32*6),32*12*.86,0,.86),#3,1
                            Camera(pygame.Rect(32*16,0,32*7,32*7),32*18*.86,0,.86*.86),#4,1
                            
                            Camera(pygame.Rect(0,32*5,32*6,32*6),0,32*6*.86,.86),#1,2
                            Camera(pygame.Rect(32*5,32*5,32*7,32*7),32*6*.86,32*6*.86,.86*.86),#2,2
                            Camera(pygame.Rect(32*11,32*5,32*7,32*7),32*12*.86,32*6*.86,.86*.86),#3,2
                            Camera(pygame.Rect(32*16,32*5,32*7,32*7),32*18*.86,32*6*.86,.86*.86),#4,2

                            Camera(pygame.Rect(0,32*11,32*6,32*6),0,32*12*.86,.86), #1,3
                            Camera(pygame.Rect(32*5,32*11,32*6,32*6),32*6*.86,32*12*.86,.86),#2,3
                            Camera(pygame.Rect(32*11,32*11,32*6,32*6),32*12*.86,32*12*.86,.86),#3,3
                            Camera(pygame.Rect(32*16,32*11,32*6,32*6),32*18*.86,32*12*.86,.86)#4,3
                            ]

            
        
        
        elif level == 1: #level1
            self.tiles = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
                          [0,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
                          [0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
                          [0,1,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,1,1],
                          [0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
                          [0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1,1,1,1,0,1,1],
                          [0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,1,1,1,1,1,1,0,1,1],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
                          [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]]
            self.player = Player(2,2)
            self.enemies = []
            self.enemies.append(Enemy([[13,2],[13,13]]))
            self.enemies.append(Enemy([[2,12],[20,12]]))
            self.cameras = [#Camera(pygame.Rect(0,0,32*23,32*16),0,32*6*.86,.15), #special Cam
                            Camera(pygame.Rect(0,0,32*6,32*6),0,0,.86),#1,1
                            Camera(pygame.Rect(32*5,0,32*7,32*7),32*6*.86,0,.86*.86),#2,1
                            Camera(pygame.Rect(32*11,0,32*6,32*6),32*18*.86,32*12*.86,.86),#4,3
                            Camera(pygame.Rect(32*16,0,32*7,32*7),32*18*.86,0,.86*.86),#4,1
                            
                            Camera(pygame.Rect(0,32*5,32*6,32*6),0,32*12*.86,.86),#1,3
                            Camera(pygame.Rect(32*5,32*5,32*7,32*7),32*6*.86,32*6*.86,.86*.86),#2,2
                            Camera(pygame.Rect(32*11,32*5,32*7,32*7),32*12*.86,32*6*.86,.86*.86),#3,2
                            Camera(pygame.Rect(32*16,32*5,32*7,32*7),32*12*.86,32*12*.86,.86*.86),#3,3

                            Camera(pygame.Rect(0,32*11,32*6,32*6),0,32*6*.86,.86),#1,2
                            Camera(pygame.Rect(32*5,32*11,32*7,32*7),32*6*.86,32*12*.86,.86*.86),#2,3
                            Camera(pygame.Rect(32*11,32*11,32*7,32*7),32*12*.86,32*6*.86,.86*.86),#4,2
                            Camera(pygame.Rect(32*16,32*11,32*7,32*7),32*12*.86,0,.86*.86)#3,1
                            ]
        elif level == 2:
            self.tiles = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                          [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                          [0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,1],
                          [0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,1],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
                          [0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
                          [0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
                          [0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
                          [0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
                          [0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
                          [0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
                          [0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                          [0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                          [0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
            self.player = Player(14,10)
            self.enemies = []
            self.enemies.append(Enemy([[18,2],[2,2]]))
            self.enemies.append(Enemy([[2,6],[9,6]]))
            self.enemies.append(Enemy([[9,6],[18,6]]))
            self.cameras = [Camera(pygame.Rect(0,0,32*6,32*6),0,0,.86), #1,1 SCREEN POSITIONS (1,1 is always top right).
                            Camera(pygame.Rect(32*6,0,32*6,32*6),32*6*.86,32*12*.86,.86),#2,1 32*6*.86,0,.86
                            Camera(pygame.Rect(32*12,0,32*6,32*6),32*12*.86,0,.86),#3,1 32*12*.86,0,.86
                            Camera(pygame.Rect(32*18,0,32*6,32*6),32*18*.86,32*12*.86,.86),#4,1 32*18*.86,0,.86
                            
                            Camera(pygame.Rect(0,32*11,32*6,32*6),0,32*12*.86,.86),#1,3 0,32*12*.86,.86
                            Camera(pygame.Rect(32*6,32*11,32*6,32*6),32*6*.86,0,.86),#2,3 32*6*.86,32*12*.86,.86
                            Camera(pygame.Rect(32*12,32*11,32*6,32*6),32*12*.86,32*12*.86,.86),#3,3 32*12*.86,32*12*.86,.86
                            Camera(pygame.Rect(32*18,32*11,32*6,32*6),32*18*.86,0,.86),#4,3 32*18*.86,32*12*.86,.86

                            Camera(pygame.Rect(0,32*5,32*24,32*6),0,32*6*.86,.86), #longcam of mid row
                            ]
        elif level == 3: #level3
            self.tiles = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
                          [0,1,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0],
                          [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
                          [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
                          [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
                          [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
                          [0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0],
                          [0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0],
                          [0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0],
                          [0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0],
                          [0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0],
                          [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
            self.player = Player(12,2)
            self.enemies = []
            self.enemies.append(Enemy([[5,2],[19,2]]))
            self.enemies.append(Enemy([[19,6],[5,6]]))
            self.enemies.append(Enemy([[8,12],[8,7]]))
            self.enemies.append(Enemy([[3,12],[18,12]]))
            self.cameras = [Camera(pygame.Rect(0,0,32*6,32*6),0,0,.9), #1,1 SCREEN POSITIONS (1,1 is always top right).
                            Camera(pygame.Rect(32*5,0,32*12,32*17),32*6*.9,0,.9),#2&3,1&2&3
                            Camera(pygame.Rect(32*16,0,32*6,32*6),32*18*.9,0,.9),#4,1 32*18*.9,0,.9
                            
                            Camera(pygame.Rect(0,32*5,32*6,32*6),32*18*.9,32*12*.83,.9),#1,2 0,32*6*.75,.9
                            Camera(pygame.Rect(32*16,32*5,32*6,32*6),32*18*.9,32*6*.75,.9),#4,2 32*18*.9,32*6*.75,.9

                            Camera(pygame.Rect(0,32*11,32*6,32*6),0,32*12*.83,.9), #1,3 0,32*12*.83,.9
                            Camera(pygame.Rect(32*16,32*11,32*6,32*6),32*18*.9,0,.9)#4,3 32*18*.9,32*12*.83,.9
                            ]



        else:
            self.tiles = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                          [1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                          [1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                          [1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                          [1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                          [1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                          [1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                          [1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                          [1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                          [1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                          [1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                          [1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1]]
            self.player = Player(0,3)
            self.enemies = []
            self.enemies.append(Enemy([[2,0],[6,0]]))
            self.cameras = [Camera(pygame.Rect(0,0,32*5,32*5),210,0),Camera(pygame.Rect(32*5,0,32*5,32*5),0,0),Camera(pygame.Rect(0,32*5,32*5,32*5),0,210),Camera(pygame.Rect(32*5,32*5,32*5,32*5),210,210)]

    def fromCameraToWorld(self,loc):
        worldLoc = [-1000,-1000]
        cam = None
        for c in self.cameras:
            if (checkContain(loc,pygame.Rect(c.x,c.y,c.view.width*c.scale,c.view.height*c.scale))==1):
                worldLoc[0] = c.view.x + float(loc[0] - c.x)/c.scale
                worldLoc[1] = c.view.y + float(loc[1] - c.y)/c.scale
                cam = c
        return cam,worldLoc[0], worldLoc[1]

    def playMenu(self):
        while 1:
            self.clock.tick(30)
            self.screen.blit(self.menu,(0,0))
            if (self.controls.update()==1):
                return -1
            if self.controls.A==1:
                return 1
            pygame.display.flip()

    def play(self):
        while 1:
            self.clock.tick(30)
            self.screen.fill((0,0,0))
            #controls
            if (self.controls.update()==1):
                return -1
            
            #update player controls
            self.player.xVelocity = 0
            self.player.yVelocity = 0
            if (self.controls.W==1):
                self.player.yVelocity = -5
            elif (self.controls.S==1):
                self.player.yVelocity = 5
            if (self.controls.A==1):
                self.player.xVelocity = -5
            elif (self.controls.D==1):
                self.player.xVelocity = 5
            
            for c in self.cameras:
                c.active = 0
            oldPlayerLoc = [self.player.x,self.player.y]
            self.player.update()
            playerCamera = None
            for c in self.cameras:
                if (checkContain([self.player.x,self.player.y],c.view)==1):
                    c.active = 1
                    playerCamera = c
            for e in self.enemies:
                e.update()
                c,e.x,e.y = self.fromCameraToWorld([e.superX,e.superY])
                inRange = 0
                e.playerView = 0
                if (c):
                    c.active = 1
                    if (c == playerCamera):
                        inRange = 1
                        e.playerView = 1
                
            for y in range(len(self.tiles)):
                for x in range(len(self.tiles[y])):
                    if (checkCollidable(self.tiles[y][x])==1):
                        if (int(float(self.player.x)/32+0.5) == x and int(float(self.player.y)/32+0.5) == y):
                            self.player.x = oldPlayerLoc[0]
                            self.player.y = oldPlayerLoc[1]
                    if (self.tiles[y][x]==1):
                        img = self.floorTiles[random.randrange(0,len(self.floorTiles))]
                        self.world.blit(img,(self.tileSize*x,self.tileSize*y))
                    elif (self.tiles[y][x]==0):
                        img = self.wallTiles[random.randrange(0,len(self.wallTiles))]
                        self.world.blit(img,(self.tileSize*x,self.tileSize*y))
                    else:
                        self.world.blit(self.tileImages[self.tiles[y][x]],(self.tileSize*x,self.tileSize*y))
            self.player.draw(self.world)
            for e in self.enemies:
                e.draw(self.world)
                mask = e.drawFOV(self.world,self.tiles)
                if e.playerView==1:
                    img = pygame.Surface((32,32))
                    img.fill((255,255,255))
                    img.set_colorkey((0,0,0))
                    playerMask = pygame.mask.from_surface(img,50)
                    if not (mask.overlap(playerMask,[self.player.x-(e.x+16-e.viewLength),self.player.y-(e.y+16-e.viewLength)])==None):
                        self.player.health -= 1
            
            #draw
            for c in self.cameras:
                if c.active == 1:
                    if (c.scale == 1):
                        self.screen.blit(self.world,(c.x,c.y),c.view)
                    else:
                        img = pygame.Surface((c.view.width,c.view.height))
                        img.blit(self.world,(0,0),c.view)
                        img = pygame.transform.scale(img,(c.view.width*c.scale,c.view.height*c.scale))
                        self.screen.blit(img,(c.x,c.y))
                        if (c.white < c.maxWhite):
                            c.white+=3
                else:
                    if (c.white > 0):
                        c.white-=2
                if (c.white > 0):
                    white = pygame.Surface((c.view.width*c.scale,c.view.height*c.scale))
                    if (c.active==0):
                        white.fill((50,50,50))
                        white.set_alpha(c.white)
                    else:
                        white.fill((255,255,255))
                        white.set_alpha(c.maxWhite-c.white)
                    self.screen.blit(white,(c.x,c.y))

            #check for end condition
            if (self.player.health < 0):
                return 0
            elif (checkContain([self.player.x,self.player.y],pygame.Rect(0,0,len(self.tiles[0])*32,len(self.tiles)*32))==0):
                return 1
            pygame.display.flip()

def checkCollidable(num):
    if num==0 or num==20:
        return 1
    else:
        return 0

def checkContain(point,rect):
    if (point[0] >= rect.x and point[1] >= rect.y and point[0] <= rect.x + rect.width and point[1] <= rect.y + rect.height):
        return 1
    return 0

game = Game()
currentLevel = 0
game.restart(0)
while 1:
    num = game.play()
    print num
    if (num==-1):
        if (game.playMenu()==-1):
            break
        else:
            game.restart(0)
    elif (num==0):
        game.restart(currentLevel)
    elif (num==1):
        currentLevel+=1
        game.restart(currentLevel)
