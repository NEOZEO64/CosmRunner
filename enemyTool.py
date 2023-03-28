import pygame
import lib
import math
import random
import json
import os

pygame.init()

margin = 40

# Programmeigenschaften einstellen
WINDOW_WIDTH = 400 + 2*margin
backgroundPic = lib.loadIMG("Res/background.png",WINDOW_WIDTH - 2*margin)
WINDOW_HEIGHT = backgroundPic.get_height() + 2*margin
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Fenster erstellen

# Zeit einstellen
framesPerSecond = 30 # auch kurz FPS genannt
fpsClock = pygame.time.Clock()

font = pygame.font.Font('Res/uiFont.ttf', 20)

leftClick, rightClick, middleClick = (False,False,False)
mLeftClick, mRightClick, mMiddleClick = (True,True,True)
mouseX, mouseY = (0,0)


fileName = input("Filename (standard: move.json):")

if fileName == "":
    fileName = "move.json"



waypoints = {}

waypoints = {
    "color":(255,0,0),
    "size":3,
    "points":[],
}

if os.path.isfile(fileName):
    file = open(fileName,"r")
    waypoints = json.loads(file.read())
    file.close()
else:
    file = open(fileName,"w")
    file.write(json.dumps(waypoints))
    file.close()

for w in waypoints["points"]:
    w[0] += margin
    w[1] += margin



class Star:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.s = random.randrange(1,4)
        self.vx = 0
        self.vy = self.s * random.randrange(2,4)/10
        self.color = (
            int(50 * self.s * random.randrange(8,12)/10),
            int(50 * self.s * random.randrange(8,12)/10),
            int(70 * self.s * random.randrange(8,12)/10)
            )
    def move(self): # returns True if still inside screen after move
        self.x += self.vx
        self.y += self.vy
        
        if self.y + self.s < WINDOW_HEIGHT - margin:
            return True
        else:
            return False
        
    def show(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.s, 0)

class Player: # Player
    w = 50
    x = WINDOW_WIDTH/2 - w/2
    y = WINDOW_HEIGHT * 0.8
    pic = lib.loadIMG("Res/player_ship.png",w)
    h = pic.get_height()


class Background:
    spaceColor = (10,10,30)
    galaxyPic = lib.loadIMG("Res/galaxy.png",1000)
    backgroundPic = lib.loadIMG("Res/background.png",WINDOW_WIDTH-2*margin)
    stars = []
    
    y = 0
    vy = 2
    
    
    for y in range(margin, WINDOW_HEIGHT-2*margin,vy):
        if random.randrange(0,100) > 90:
            stars.append(Star(random.randrange(-10 + margin,WINDOW_WIDTH+10 - margin),y))


    def move():
        Background.y += Background.vy
        if Background.y > WINDOW_HEIGHT - margin:
            Background.y = 0
        
        if random.randrange(0,100) > 90:
            Background.stars.append(Star(random.randrange(-10 + margin,WINDOW_WIDTH-margin+10),-10 + margin))
        
        i = 0
        while i < len(Background.stars):
            if Background.stars[i].move() != True:
                del Background.stars[i]
            else:
                i += 1

        
    def show():
        window.fill((100,100,100))
        pygame.draw.rect(window, Background.spaceColor, (margin, margin, WINDOW_WIDTH-2*margin, WINDOW_HEIGHT-2*margin), 0)
        #
        # window.fill(Background.spaceColor) # Fenster schwarz zeichnen
        #window.blit(backgroundPic,(0,backgroundY-WINDOW_HEIGHT))
        #window.blit(backgroundPic,(0,backgroundY))

        window.blit(Background.galaxyPic, (-100 + margin,20 + margin))

        for star in Background.stars:
            star.show()

        #window.blit(Background.background2Pic,(0,Background.y))

class Enemy:
    w = 50
    vx = 0
    vy = 0
    moveRad = 2
    pic = carlsExtension.loadIMG("Res/enemy_1.png",w)
    h = pic.get_height()
    objs = [] # stores all the Enemy.objs 
    def __init__(self,x,y):
        self.cx = x
        self.cy = y
        self.x = self.cx
        self.y = self.cy
        self.phi = random.randrange(0,360)
        self.rv = random.randint(0,1) * 2 - 1 # -1 or 1
    def move(self):
        self.cx += self.vx
        self.cy += self.vy

        self.phi += self.rv * random.randrange(0,10)/20
        self.x = self.cx + Enemy.moveRad * math.cos(self.phi)
        self.y = self.cy + Enemy.moveRad * math.sin(self.phi)

    def show(self):
        window.blit(self.pic, (self.x,self.y))


def drawCross(color, p1, size, weight):
    pygame.draw.line(window, color, (p1[0] - size/2, p1[1] - size/2), (p1[0] + size/2, p1[1] + size/2), weight)
    pygame.draw.line(window, color, (p1[0] + size/2, p1[1] - size/2), (p1[0] - size/2, p1[1] + size/2), weight)


def show():
    Background.show()
    
    window.blit(Player.pic, (Player.x,Player.y))
    
    for e in Enemy.objs:
        e.show()


    for w in waypoints["points"]:
        drawCross(waypoints["color"], w, waypoints["size"], 2)

    for i in range(1, len(waypoints["points"])):
        currentP = waypoints["points"][i]
        lastP = waypoints["points"][i-1]
        pygame.draw.line(window, waypoints["color"], (currentP[0], currentP[1]), (lastP[0],lastP[1]), 2)

    pygame.draw.line(window, waypoints["color"],(waypoints["points"][-1][0], waypoints["points"][-1][1]), (mouseX, mouseY), 2)


def handleEvents():
    global leftClick, rightClick, middleClick, mouseX, mouseY, mLeftClick, mRightClick, mMiddleClick
    quit = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit = True



    leftClick, rightClick, middleClick = pygame.mouse.get_pressed()
    mouseX, mouseY = pygame.mouse.get_pos()
    keysPressed = carlsExtension.getKeys()


    Enemy.objs[0].cx = mouseX - Enemy.w/2
    Enemy.objs[0].cy = mouseY - Enemy.h/2


    if leftClick and mLeftClick:
        mLeftClick = False
        waypoints["points"].append([Enemy.objs[0].cx + Enemy.w/2 - waypoints["size"]/2,Enemy.objs[0].cy + Enemy.w/2 - waypoints["size"]/2])

    elif not leftClick:
        mLeftClick = True

    Enemy.objs[0].move()

    Background.move()

    if quit:
        for w in waypoints["points"]:
            w[0] -= margin
            w[1] -= margin

        file = open(fileName, "w")
        file.write(json.dumps(waypoints))
        file.close()
        return False
    return True



# Richtiges Programm startet hier
Enemy.objs.append(Enemy(-100,-100))

gameLoopRuns = True
while gameLoopRuns:
    gameLoopRuns = handleEvents()
    show()

    pygame.display.update() # Gezeichnetes anzeigen

    fpsClock.tick(framesPerSecond) # Maximal framesPerSecond-viele Bilder pro Sekunde anzeigen

pygame.quit()

