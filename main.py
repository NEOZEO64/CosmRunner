import pygame, carlsExtension, random, math, os
from PIL import Image

pygame.init()


# Programmeigenschaften einstellen
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600 #Auflösung bitte nicht ändern


bulletType = 1 # standard fast laser 
#bulletType = 2 # tracking missile

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Fenster erstellen

# Zeit einstellen
framesPerSecond = 30 # auch kurz FPS genannt
fpsClock = pygame.time.Clock()

font = pygame.font.Font('Res/uiFont.ttf', 20)

enemyTroops = []


enemyRouteFiles = os.listdir("EnemyRoutes2/") # EnemyMove-Pngs need a width of 500 and height of 700
enemyRoutes = []

MoveMargin = 50
imageWidth = WINDOW_WIDTH + 2*MoveMargin
imageHeight = WINDOW_HEIGHT + 2*MoveMargin

surroundings = [ # must have length 8
    [-1, -1], # up left
    [ 0, -1], # up
    [ 1, -1], # up right
    [ 1,  0], # right
    [ 1,  1], # down right
    [ 0,  1], # down
    [-1,  1], # down left
    [-1,  0], # left
]

borderCoords = []

for x in range(-MoveMargin, WINDOW_WIDTH+MoveMargin):
    borderCoords.append((x,-50))
    borderCoords.append((x,WINDOW_HEIGHT+49))
for y in range(-MoveMargin + 1, WINDOW_HEIGHT+MoveMargin -1):
    borderCoords.append((-50,y))
    borderCoords.append((WINDOW_WIDTH+49, y))


i = 0
while "pixil-frame-{}.png".format(i) in enemyRouteFiles:
    image = Image.open("EnemyRoutes2/" + "pixil-frame-{}.png".format(i))
    pixels = list(image.convert('L').getdata())
    black_pixels = [i for i, pixel in enumerate(pixels) if pixel in list(range(0,10))]
    black_pixels_coords = [(index % imageWidth, index // imageWidth) for index in black_pixels]
    black_pixels_coords_moved = [(x-MoveMargin, y-MoveMargin) for (x,y) in black_pixels_coords]
    enemyRoutes.append(black_pixels_coords_moved)
    i += 1


startPoints = [] # gather all the enemy-spawnpoints in the pictures (at the border of the image)
for i in range(0, len(enemyRoutes)):
    startPoints.append([])
    for (x,y) in borderCoords: 
        if (x, y) in enemyRoutes[i]:
            startPoints[i].append((x,y))

def getSpawnPoint(index):
    return startPoints[index][random.randrange(0,len(startPoints[index]))]

def getNextPoint(lastx, lasty, index, x, y, dist): # dist: how many pixels to go further!
    tempX, tempY = (x,y)
    tempLastX, tempLastY = (lastx, lasty)

    for i in range(0, dist):
        found = False
        j = 0
        while j < len(surroundings) and not found:
            dir = surroundings[j]
            if (tempX + dir[0],tempY + dir[1]) in enemyRoutes[index] and not (tempX + dir[0] == tempLastX and tempY + dir[1] == tempLastY):
                found = True
                tempLastX,tempLastY = (tempX,tempY)
                tempX,tempY = (tempX+dir[0], tempY+dir[1])
            j += 1
        if not found:
            #print("Done")
            return (-1000, -1000, 0, 0) # if no way possible or if arrived at the end of the route
    
    return tempX, tempY, tempLastX, tempLastY

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
        
        if self.y + self.s < WINDOW_HEIGHT:
            return True
        else:
            return False
        
    def show(self):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.s, 0)

class Background:
    spaceColor = (10,10,30)
    galaxyPic = carlsExtension.loadIMG("Res/galaxy.png",1000)
    backgroundPic = carlsExtension.loadIMG("Res/background.png",WINDOW_WIDTH)
    stars = []
    
    y = 0
    vy = 2
    
    
    for y in range(0, WINDOW_HEIGHT,vy):
        if random.randrange(0,100) > 90:
            stars.append(Star(random.randrange(-10,WINDOW_WIDTH+10),y))


    def move():
        Background.y += Background.vy
        if Background.y > WINDOW_HEIGHT:
            Background.y = 0
        
        if random.randrange(0,100) > 90:
            Background.stars.append(Star(random.randrange(-10,WINDOW_WIDTH+10),-10))
        
        i = 0
        while i < len(Background.stars):
            if Background.stars[i].move() != True:
                del Background.stars[i]
            else:
                i += 1

        
    def show():
        window.fill(Background.spaceColor) # Fenster schwarz zeichnen
        #window.blit(backgroundPic,(0,backgroundY-WINDOW_HEIGHT))
        #window.blit(backgroundPic,(0,backgroundY))

        window.blit(Background.galaxyPic, (-100,20))

        for star in Background.stars:
            star.show()

        #window.blit(Background.background2Pic,(0,Background.y))

class Player: # Player
    w = 50
    x = WINDOW_WIDTH/2 - w/2 # Center coordinates
    y = WINDOW_HEIGHT * 0.8
    pic = carlsExtension.loadIMG("Res/player_ship.png",w)
    h = pic.get_height()

    #vx = 0
    #vy = 0
    speed = 0
    rot = 0

    acc = 2
    friction = 0.9
    maxSpeed = 20
    bullets = []

    def move():
        nextX = Player.x - Player.speed*math.sin(math.radians(Player.rot))
        nextY = Player.y - Player.speed*math.cos(math.radians(Player.rot))

        if nextX + Player.w/2 > WINDOW_WIDTH:
            nextX = -Player.w/2 + 1
        elif nextX + Player.w/2 < 0:
            nextX = WINDOW_WIDTH-Player.w/2 - 1

        if nextY + Player.h/2 > WINDOW_HEIGHT:
            nextY = -Player.h/2 + 1
        elif nextY + Player.h/2 < 0:
            nextY = WINDOW_HEIGHT-Player.h/2 - 1

        Player.speed *= Player.friction
        #Player.vx *= Player.friction
        #Player.vy *= Player.friction

        Player.x = nextX
        Player.y = nextY
        #Player.x += Player.vx
        #Player.y += Player.vy
    def show():
        carlsExtension.blitRotate(window,Player.pic,(Player.x,Player.y),Player.rot)
        #window.blit(Player.pic, (Player.x,Player.y))


class Explosion:
    ws = [ # widths
        80 # type 0
    ]
    
    animations = []

    tempAnimation = []
    for i in range(1,9):
        tempAnimation.append(carlsExtension.loadIMG("Res/Explosion_{}.png".format(i), ws[0]))
    animations.append(tempAnimation)

    numbers = [len(animation) for animation in animations] # animation pic length

    hs = [i[0].get_height() for i in animations]# heights

    objs = []

    def __init__(self,x,y, type):
        self.cx = x # center
        self.cy = y
        self.type = type
        self.x = self.cx-Explosion.ws[self.type]/2
        self.y = self.cy-Explosion.hs[self.type]/2
        self.speed = 0.5
        self.state = 0
        
    def move(self): # returns if animation done
        self.state += self.speed
        

        if self.state >= Explosion.numbers[self.type]:
            return True
        return False
        
    def show(self):
        window.blit(self.animations[self.type][int(self.state)], (self.x, self.y))
        #window.blit(self.animations[self.type][int(self.state)], (self.x, self.y))

class Score:
    score = 0
    cx = 0 # centerx

    label1 = font.render("Score ", 0, (180,0,0))
    w1, h1 = font.size  ("Score ")

    label2 = font.render("%06d"%score, 0, (255,0,0))
    w2, h2 = font.size("5"*6)

    x = WINDOW_WIDTH - w1 - w2 - 20
    x2 = WINDOW_WIDTH - w1 - 20 # changed also
    y = 10
    
    
    def set(newScore):
        Score.score = newScore
        Score.label2 = font.render("%06d"%newScore, 0, (255,0,0))

    def show():
        window.blit(Score.label1, (Score.x,Score.y))
        window.blit(Score.label2, (Score.x2, Score.y))

class Bullet:
    trackAngle = 80
    trackRange = 200
    trackRotationSpeed = 12

    def __init__(self,x,y,rot,type):
        self.rot = rot
        if type == 1: # standard laser
            self.speed = 27
            self.move = self.standardMove
            self.w = 5
            self.h = 20
            self.pic = carlsExtension.loadIMG("Res/player_laser.png",self.w,self.h)
        else: #e.g. type == 2: tracking missile
            self.speed = 10
            self.move = self.trackingMove
            self.w = 10
            self.h = 20
            self.aimRot = 0
            self.pic = carlsExtension.loadIMG("Res/rocket.png",self.w,self.h)
        self.x = x - self.w/2
        self.y = y - self.h/2
    
    def getNextAim(self):
        bestEnemyX, bestEnemyY = (1000000,1000000)
        bestEnemyDist = 10000000
        angle = 0

        for troop in enemyTroops:
            for enemy in troop.objs:
                toEnemyX, toEnemyY = (enemy.x2-self.x, enemy.y2-self.y)
                dist = math.hypot(toEnemyX, toEnemyY)
                if dist < bestEnemyDist:
                    vx, vy = (self.speed*math.sin(math.radians(self.rot)), self.speed*math.cos(math.radians(self.rot)))
                    # calculate absolute angle
                    angle = math.degrees(math.acos((vx*toEnemyX + vy*toEnemyY)/(math.hypot(vx, vy)*math.hypot(toEnemyX, toEnemyY))))
                    if angle < Bullet.trackAngle/2:
                        bestEnemyDist = dist
                        bestEnemyX, bestEnemyY = (toEnemyX, toEnemyY)
        if bestEnemyDist > 100000:
            return 0
        # calculate angle
        vx2, vy2 = (self.speed*math.sin(math.radians(self.rot+0.01)), self.speed*math.cos(math.radians(self.rot+0.01)))
        angle2 = math.degrees(math.acos((vx2*bestEnemyX + vy2*bestEnemyY)/(math.hypot(vx2, vy2)*math.hypot(bestEnemyX, bestEnemyY))))
        if angle2 > angle:
            return -angle
        return angle

    def standardMove(self):
        #self.x += self.vx
        #self.y += self.vy
        self.x -= self.speed*math.sin(math.radians(self.rot))
        self.y -= self.speed*math.cos(math.radians(self.rot))

    def trackingMove(self):
        self.aimRot = self.getNextAim()
        if self.aimRot < 0: # is on the left
            self.rot += Bullet.trackRotationSpeed
        if self.aimRot > 0: # is on the right
            self.rot -= Bullet.trackRotationSpeed
        
        self.x -= self.speed*math.sin(math.radians(self.rot))
        self.y -= self.speed*math.cos(math.radians(self.rot))


    def show(self):
        #window.blit(self.pic, (self.x,self.y))
        carlsExtension.blitRotate(window, self.pic, (self.x, self.y), self.rot)

class Enemy:
    w = 50
    vx = 0
    vy = 0
    moveRad = 2
    pic = carlsExtension.loadIMG("Res/enemy_1.png",w)
    h = pic.get_height()
    def __init__(self,x,y, moveIndex, speed):
        self.x = x # center coordinates
        self.y = y
        self.moveIndex = moveIndex
        self.lastx = -1000 # needed for direction; also center coordinates
        self.lasty = -1000 # needed for direction
        self.x2 = self.x # also center coordinates
        self.y2 = self.y
        self.speed = speed
        self.phi = random.randrange(0,360)
        self.rv = random.randint(0,1) * 2 - 1 # -1 or 1
    def move(self):
        self.x, self.y, self.lastx, self.lasty = getNextPoint(self.lastx, self.lasty, self.moveIndex, self.x, self.y, self.speed)

        self.phi += self.rv * random.randrange(0,10)/20
        self.x2 = self.x + Enemy.moveRad * math.cos(self.phi)
        self.y2 = self.y + Enemy.moveRad * math.sin(self.phi)

    def show(self):
        window.blit(self.pic, (self.x2 - Enemy.w/2,self.y2 - Enemy.h/2))


class EnemyTroup:
    def __init__(self, routeIndex ,count, speed):
        self.objs = []
        self.routeIndex = routeIndex # index of position in way
        self.count = count
        self.speed = speed

        self.startx, self.starty = getSpawnPoint(routeIndex)
        #print(self.startx, self.starty)

        self.spawnCoolDown = 10 # time between spawing enemies
        self.spawnCoolDownLeft = -100
        self.spawnCount = 0 # number of enemies already spawned

        self.speed = speed

        self.isDone = False

    def move(self):
        self.spawnCoolDownLeft -= 1

        if self.spawnCount < self.count and self.spawnCoolDownLeft < 0:            
            self.spawnCoolDownLeft = self.spawnCoolDown
            self.objs.append(Enemy(self.startx, self.starty, self.routeIndex, self.speed))
            self.spawnCount += 1
        
        for i in range(0, len(self.objs)):
            self.objs[i].move()
        
        #print(self.objs[0].x,self.objs[0].y)

        i = 0
        while i < len(self.objs):
            if (self.objs[i].x, self.objs[i].y) == (-1000,-1000):
                del self.objs[i]
            else:
                i += 1

        if i == 0:
            self.isDone = True


    def show(self):
        for enemy in self.objs:
            enemy.show()



def movePhysics():
    Player.move()

    if enemyTroops == []:
        enemyTroops.append(EnemyTroup(random.randrange(0,len(enemyRoutes)),random.randrange(1,20),random.randrange(2,8))) # Troup of one Enemy
        #enemyTroops.append(EnemyTroup(0,5,8)) # Troup of one Enemy

    for eT in enemyTroops:
        eT.move()

    i = 0
    while i < len(enemyTroops):
        if enemyTroops[i].isDone:
            del enemyTroops[i]
        else:
            i += 1


    iBullet = 0
    while iBullet < len(Player.bullets):
        Player.bullets[iBullet].move()
        #Player.bullets[iBullet].x += Bullet.vx
        #Player.bullets[iBullet].y += Bullet.vy
        

        noExplosion = True

        iEnemyTroop = 0
        while iEnemyTroop < len(enemyTroops):
            iEnemy = 0 
            
            while iEnemy < len(enemyTroops[iEnemyTroop].objs) and iBullet < len(Player.bullets):
                if carlsExtension.getRectRectCollide(
                            Player.bullets[iBullet].x, Player.bullets[iBullet].y, Player.bullets[iBullet].w,Player.bullets[iBullet].h,
                            enemyTroops[iEnemyTroop].objs[iEnemy].x,enemyTroops[iEnemyTroop].objs[iEnemy].y,Enemy.w,Enemy.h):

                    Score.set(Score.score + 10)

                    Explosion.objs.append(Explosion(enemyTroops[iEnemyTroop].objs[iEnemy].x,enemyTroops[iEnemyTroop].objs[iEnemy].y,0)) # 0 for type
                    
                    del enemyTroops[iEnemyTroop].objs[iEnemy]
                    del Player.bullets[iBullet]

                    noExplosion = False
                else:
                    iEnemy += 1

            iEnemyTroop += 1
            
        if noExplosion == True:
            iBullet += 1
            

    i = 0
    while i < len(Explosion.objs):
        if Explosion.objs[i].move() == True:
            del Explosion.objs[i]
        else:
            i += 1

    i = 0
    while i < len(Player.bullets):
        if Player.bullets[i].y + Player.bullets[i].h > WINDOW_HEIGHT or \
            Player.bullets[i].y - Player.bullets[i].h < 0 or \
            Player.bullets[i].x - Player.bullets[i].w < 0 or \
            Player.bullets[i].x + Player.bullets[i].w > WINDOW_WIDTH:

            del Player.bullets[i]
        else:
            i += 1

    Background.move()

def show():
    Background.show()
    
    for b in Player.bullets:
        b.show()
    
    for eT in enemyTroops:
        eT.show()
    
    for e in Explosion.objs:
        e.show()

    Score.show()

    Player.show()

def handleEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Player.bullets.append(Bullet(Player.x+Player.w/2,Player.y + Player.h/2, Player.rot, bulletType))
            elif event.key == pygame.K_ESCAPE:
                return False

    keysPressed = carlsExtension.getKeys()

    if keysPressed["w"]: # W
        #Player.vy -= Player.acc
        Player.speed += Player.acc
    if keysPressed["a"]: # A
        Player.rot += 8
        #Player.vx -= Player.acc
    if keysPressed["s"]: # S
        Player.speed -= Player.acc
        #Player.vy += Player.acc
    if keysPressed["d"]: # D
        Player.rot -= 8
        #Player.vx += Player.acc
    
    return True

# Richtiges Programm startet hier


#enemyTroops.append(EnemyTroup(0,5,2)) # Troup of 5 Enemies

#enemyTroops.append(EnemyTroup(1,1,2)) # Troup of one Enemy

#for x in range(20,WINDOW_WIDTH-20, 80):
#    for y in range(40,220, 80):
#        Enemy.objs.append(Enemy(x,y))


gameLoopRuns = True
while gameLoopRuns:
    gameLoopRuns = handleEvents()

    movePhysics()
    show()

    pygame.display.update() # Gezeichnetes anzeigen

    fpsClock.tick(framesPerSecond) # Maximal framesPerSecond-viele Bilder pro Sekunde anzeigen

pygame.quit()