import pygame, carlsExtension, random, math
import os, json

pygame.init()


# Programmeigenschaften einstellen
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600 #Auflösung bitte nicht ändern


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Fenster erstellen

# Zeit einstellen
framesPerSecond = 30 # auch kurz FPS genannt
fpsClock = pygame.time.Clock()

font = pygame.font.Font('Res/uiFont.ttf', 20)

wayFilenames = ["move.json"]

ways = []

enemyTroops = []

for wF in wayFilenames:
    if os.path.isfile(wF):
        file = open(wF,"r")
        ways.append(json.loads(file.read()))
        file.close()



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
    x = WINDOW_WIDTH/2 - w/2
    y = WINDOW_HEIGHT * 0.8
    pic = carlsExtension.loadIMG("Res/player_ship.png",w)
    h = pic.get_height()

    vx = 0
    vy = 0
    acc = 4
    friction = 0.65
    maxSpeed = 20
    bullets = []

    def move():
        if Player.x + Player.w/2 > WINDOW_WIDTH and Player.vx > 0:
            Player.x = -Player.w/2
        elif Player.x + Player.w/2 < 0 and Player.vx < 0:
            Player.x = WINDOW_WIDTH-Player.w/2

        if Player.y + Player.h > WINDOW_HEIGHT and Player.vy > 0:
            Player.vy = 0
        elif Player.y < 0 and Player.vy < 0:
            Player.vy = 0

        Player.vx *= Player.friction
        Player.vy *= Player.friction

        Player.x += Player.vx
        Player.y += Player.vy

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
        self.x = x
        self.y = y
        self.speed = 0.5
        self.state = 0
        self.type = type
    def move(self): # returns if animation done
        self.state += self.speed
        

        if self.state >= Explosion.numbers[self.type]:
            return True
        return False
        
    def show(self):
        window.blit(self.animations[self.type][int(self.state)], (self.x, self.y))

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
    w = 5
    h = 20
    vx = 0
    vy = -27
    pic = carlsExtension.loadIMG("Res/player_laser.png",w,h)
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def move(self):
        self.x += self.vx
        self.y += self.vy

    def show(self):
        window.blit(self.pic, (self.x,self.y))

class Enemy:
    w = 50
    vx = 0
    vy = 0
    moveRad = 2
    pic = carlsExtension.loadIMG("Res/enemy_1.png",w)
    h = pic.get_height()
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
        self.x = self.cx #+ Enemy.moveRad * math.cos(self.phi)
        self.y = self.cy #+ Enemy.moveRad * math.sin(self.phi)

    def show(self):
        window.blit(self.pic, (self.x,self.y))


class EnemyTroup:
    def __init__(self, wayIndex,count):
        self.objs = []
        self.wayPos = [0] * count # index of position in way
        self.count = count
        self.wayIndex = wayIndex
        self.spawnCoolDown = 10 # time between spawing enemies
        self.spawnCoolDownLeft = self.spawnCoolDown
        self.spawnCount = 0

        self.speed = 4 # the higher the slower

    def move(self):
        self.spawnCoolDownLeft -= 1

        if self.spawnCount < self.count and self.spawnCoolDownLeft < 0:
            
            self.spawnCoolDownLeft = self.spawnCoolDown
            self.objs.append(Enemy(ways[self.wayIndex]["points"][self.wayPos[self.spawnCount]][0],
                                    ways[self.wayIndex]["points"][self.wayPos[self.spawnCount]][1]))
            self.spawnCount += 1
        
        for i in range(len(self.objs)):
            if self.wayPos[i] + 1 < len(ways[self.wayIndex]["points"]):
                self.objs[i].cx += (ways[self.wayIndex]["points"][self.wayPos[i]+1][0] - ways[self.wayIndex]["points"][self.wayPos[i]][0])/self.speed
                self.objs[i].cy += (ways[self.wayIndex]["points"][self.wayPos[i]+1][1] - ways[self.wayIndex]["points"][self.wayPos[i]][1])/self.speed

            if [int(self.objs[i].cx), int(self.objs[i].cy)] == ways[self.wayIndex]["points"][self.wayPos[i]+1]:
                self.wayPos[i] += 1

        for enemy in self.objs:
            enemy.move()
        

    def isDone(self):
        if self.wayPos == []:
            return False
        return self.wayPos[-1] == ways[self.wayIndex]["points"][-1]


    def show(self):
        for enemy in self.objs:
            enemy.show()



def movePhysics():
    Player.move()

    for eT in enemyTroops:
        eT.move()

    i = 0
    while i < len(enemyTroops):
        if enemyTroops[i].isDone():
            del enemyTroops[i]
        else:
            i += 1


    iBullet = 0
    while iBullet < len(Player.bullets):
        Player.bullets[iBullet].x += Bullet.vx
        Player.bullets[iBullet].y += Bullet.vy
        

        noExplosion = True

        iEnemyTroop = 0
        while iEnemyTroop < len(enemyTroops):
            iEnemy = 0 
            
            while iEnemy < len(enemyTroops[iEnemyTroop].objs) and iBullet < len(Player.bullets):
                if carlsExtension.getRectRectCollide(
                            Player.bullets[iBullet].x, Player.bullets[iBullet].y, Bullet.w,Bullet.h,
                            enemyTroops[iEnemyTroop].objs[iEnemy].x,enemyTroops[iEnemyTroop].objs[iEnemy].y,Enemy.w,Enemy.h):

                    Score.set(Score.score + 10)

                    Explosion.objs.append(Explosion(
                        enemyTroops[iEnemyTroop].objs[iEnemy].x+Enemy.w/2-Explosion.ws[0]/2,
                        enemyTroops[iEnemyTroop].objs[iEnemy].y+Enemy.h/2-Explosion.hs[0]/2,
                        0)) # 0 for type
                    
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
        if Player.bullets[i].y + Bullet.h < 0:
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

    window.blit(Player.pic, (Player.x,Player.y))

def handleEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Player.bullets.append(Bullet(Player.x+Player.w/2 - Bullet.w/2,Player.y + Player.h/2 - Bullet.h/2))
            elif event.key == pygame.K_ESCAPE:
                return False

    keysPressed = carlsExtension.getKeys()

    if keysPressed["w"]: # W
        Player.vy -= Player.acc
    if keysPressed["a"]: # A
        Player.vx -= Player.acc
    if keysPressed["s"]: # S
        Player.vy += Player.acc
    if keysPressed["d"]: # D
        Player.vx += Player.acc
    
    return True

# Richtiges Programm startet hier


enemyTroops.append(EnemyTroup(0,5))

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

