import pygame

class Player():
    def __init__(self,x,y):
        self.x = x*32
        self.y = y*32
        self.xVelocity = 0
        self.yVelocity = 0
        self.frame = 0
        self.health = 10
        #self.images = [pygame.image.load("picture.png")]
        playerImage = pygame.Surface((50,50))
        playerImage.fill((255,0,0))
        self.images = [playerImage]
    def update(self):
        self.x += self.xVelocity
        self.y += self.yVelocity
    def draw(self,screen):
        screen.blit(self.images[self.frame],(self.x,self.y))

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
        playerImage = pygame.Surface((50,50))
        playerImage.fill((105,0,0))
        self.images = [playerImage]
        self.path = path
        self.pathIndex = 0
        self.range = 3
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
    def draw(self,screen):
        screen.blit(self.images[self.frame],(self.x,self.y))
        
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
    def __init__(self,rect,x,y):
        self.view = rect
        self.x = x
        self.y = y
        self.active = 0

class Game():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.controls = Controls()
        self.screen = pygame.display.set_mode((640,480))
        self.world = pygame.Surface((1000,1000))
        greenTile = pygame.Surface((32,32))
        blueTile = pygame.Surface((32,32))
        greenTile.fill((0,255,0))
        blueTile.fill((0,0,255))
        self.tileSize = 32
        self.tileImages = [greenTile,blueTile]

    def restart(self,level):
        if level == 0:
            self.tiles = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                          [0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                          [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                          [0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0],
                          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
            self.player = Player(1,3)
            self.enemies = []
            self.enemies.append(Enemy([[2,0],[8,0]]))
            self.cameras = [Camera(pygame.Rect(0,0,32*5,32*5),0,0),Camera(pygame.Rect(32*5,0,32*5,32*5),32*5,0),
                            Camera(pygame.Rect(32*10,0,32*5,32*5),32*10,0),Camera(pygame.Rect(32*15,0,32*5,32*5),32*15,0),
                            Camera(pygame.Rect(0,32*5,32*5,32*5),0,32*5),Camera(pygame.Rect(32*5,32*5,32*5,32*5),32*5,32*5),
                            Camera(pygame.Rect(32*10,32*5,32*5,32*5),32*10,32*5),Camera(pygame.Rect(32*15,32*5,32*5,32*5),32*15,32*5)]
        elif level == 1:
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
            self.enemies.append(Enemy([[2,0],[18,0]]))
            self.cameras = [Camera(pygame.Rect(0,0,32*5,32*5),210,0),Camera(pygame.Rect(32*5,0,32*5,32*5),0,0),Camera(pygame.Rect(0,32*5,32*5,32*5),0,210),Camera(pygame.Rect(32*5,32*5,32*5,32*5),210,210)]
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
        worldLoc = [-100,-100]
        for c in self.cameras:
            if (checkContain(loc,pygame.Rect(c.x,c.y,c.view.width,c.view.height))==1):
                worldLoc[0] = c.view.x + (loc[0] - c.x)
                worldLoc[1] = c.view.y + (loc[1] - c.y)
        return worldLoc[0], worldLoc[1]

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
                e.x,e.y = self.fromCameraToWorld([e.superX,e.superY])
                inRange = 0
                for c in self.cameras:
                    if (checkContain([e.x,e.y],c.view)==1):
                        c.active = 1
                        if (c == playerCamera):
                            inRange = 1
                if (inRange):
                    oriX = int(float(e.x)/32+0.5)
                    oriY = int(float(e.y)/32+0.5)
                    #check up
                    x = oriX
                    y = oriY
                    r = e.range
                    while(r > 0 and x >= 0 and y >= 0 and x < len(self.tiles[0]) and y < len(self.tiles) and checkCollidable(self.tiles[y][x])==0):
                        y -= 1
                        r -=1
                        if (int(float(self.player.x)/32+0.5) == x and int(float(self.player.y)/32+0.5) == y):
                            self.player.health -= 1
                    #check down
                    x = oriX
                    y = oriY+1
                    r = e.range
                    while(r > 0 and x >= 0 and y >= 0 and x < len(self.tiles[0]) and y < len(self.tiles) and checkCollidable(self.tiles[y][x])==0):
                        y += 1
                        r -= 1
                        if (int(float(self.player.x)/32+0.5) == x and int(float(self.player.y)/32+0.5) == y):
                            self.player.health -= 1
                    #check left
                    x = oriX-1
                    y = oriY
                    r = e.range
                    while(r > 0 and x >= 0 and y >= 0 and x < len(self.tiles[0]) and y < len(self.tiles) and checkCollidable(self.tiles[y][x])==0):
                        x -= 1
                        r -= 1
                        if (int(float(self.player.x)/32+0.5) == x and int(float(self.player.y)/32+0.5) == y):
                            self.player.health -= 1
                    #check right
                    x = oriX+1
                    y = oriY
                    r = e.range
                    while(r > 0 and x >= 0 and y >= 0 and x < len(self.tiles[0]) and y < len(self.tiles) and checkCollidable(self.tiles[y][x])==0):
                        x += 1
                        r -= 1
                        if (int(float(self.player.x)/32+0.5) == x and int(float(self.player.y)/32+0.5) == y):
                            self.player.health -= 1
            
            for y in range(len(self.tiles)):
                for x in range(len(self.tiles[y])):
                    if (checkCollidable(self.tiles[y][x])==1):
                        if (int(float(self.player.x)/32+0.5) == x and int(float(self.player.y)/32+0.5) == y):
                            self.player.x = oldPlayerLoc[0]
                            self.player.y = oldPlayerLoc[1]
                    self.world.blit(self.tileImages[self.tiles[y][x]],(self.tileSize*x,self.tileSize*y))
            self.player.draw(self.world)
            for e in self.enemies:
                e.draw(self.world)
            
            #draw
            for c in self.cameras:
                if c.active == 1:
                    self.screen.blit(self.world,(c.x,c.y),c.view)

            #check for end condition
            if (self.player.health < 0):
                return 0
            elif (checkContain([self.player.x,self.player.y],pygame.Rect(0,0,len(self.tiles[0])*32,len(self.tiles)*32))==0):
                return 1
            pygame.display.flip()

def checkCollidable(num):
    if num==0:
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
        break
    elif (num==0):
        game.restart(currentLevel)
    elif (num==1):
        currentLevel+=1
        game.restart(currentLevel)
