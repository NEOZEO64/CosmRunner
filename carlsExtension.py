from math import sqrt
import pygame
pygame.init()

# version 11.4.2023


# circX: Kreis X Position
# circY: Kreis X Position
# circRad: Kreis Radius (Distanz vom Kreis-Mittelpunkt nach außen)
# recX: Rechteck X Position
# recY: Rechteck Y Position
# recW: Rechteck Breite
# recH: Rechteck Höhe

'''
class Score:
    font = pygame.font.Font('Res/uiFont.ttf', 20)
    lastScore = 0
    label1 = font.render("Score ", 0, (180,0,0))
    w1, h1 = font.size  ("Score ")
    label2 = font.render("%06d"%lastScore, 0, (255,0,0))
    w2, h2 = font.size("5"*6)



def showScore(window, score, posX, posY):
    if score != Score.lastScore:
        Score.label2 = Score.font.render("%06d"%score, 0, (255,0,0))
        Score.w2, Score.h2 = Score.font.size("5"*6)
        Score.lastScore = score

    window.blit(Score.label1, (posX, posY))
    window.blit(Score.label2, (posX + Score.w2, posY))

'''


# Bild in bestimmter Größe laden
def loadIMG(bildPfad, width, height = -1):    
    # Bild laden
    rawPic = pygame.image.load(bildPfad)

    # Größe anpassen (Bild skalieren)
    if height == -1:
        pic = pygame.transform.scale(rawPic, (width, width * rawPic.get_height()/rawPic.get_width()))
    else:
        pic = pygame.transform.scale(rawPic, (width, height))

    return pic

def blitRotate(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect)

def getRectRectCollide(rec1X, rec1Y, rec1W,rec1H,rec2X,rec2Y,rec2W,rec2H):
    rec1 = pygame.Rect(rec1X, rec1Y, rec1W, rec1H)
    rec2 = pygame.Rect(rec2X, rec2Y, rec2W, rec2H)

    return pygame.Rect.colliderect(rec1, rec2) #pygame soll die Kollisionen selbst checken

# checken, ob Kreis mit Rechteck kollidiert
def getCircRectCollide(circX, circY, circRad, recX, recY, recW, recH):
    recXCenter = recX + recW/2
    recYCenter = recY + recH/2

    closestX = recXCenter + max(-recW/2, min(recW/2,circX - recXCenter)) # clamp function
    closestY = recYCenter + max(-recH/2, min(recH/2,circY - recYCenter)) # clamp function

    distToClosestX = closestX - circX
    distToClosestY = closestY - circY
    
    distToClosestLen = sqrt(distToClosestX**2 + distToClosestY**2)

    outCircPosX = circX + distToClosestX * circRad / distToClosestLen
    outCircPosY = circY + distToClosestY * circRad / distToClosestLen

    if distToClosestLen < circRad:
        return True # Kollision passiert!
    else:
        return False # Kugel ist im freien



def getKeys():
    #keys = pygame.key.get_pressed()
    return {
        "w":pygame.key.get_pressed()[pygame.K_w],
        "a":pygame.key.get_pressed()[pygame.K_a],
        "s":pygame.key.get_pressed()[pygame.K_s],
        "d":pygame.key.get_pressed()[pygame.K_d],
        "space":pygame.key.get_pressed()[pygame.K_SPACE],
        "shift":pygame.key.get_pressed()[pygame.K_RSHIFT],
        "q":pygame.key.get_pressed()[pygame.K_q],
        "e":pygame.key.get_pressed()[pygame.K_e]
    }

# checken, ob Kreis mit Rechteck kollidiert und gib den kleinsten Weg des Kreises zurück aus
def bounce(circX, circY, circRad, recX, recY, recW, recH):
    recXCenter = recX + recW/2
    recYCenter = recY + recH/2

    closestX = recXCenter + max(-recW/2, min(recW/2,circX - recXCenter)) # clamp function
    closestY = recYCenter + max(-recH/2, min(recH/2,circY - recYCenter)) # clamp function

    distToClosestX = closestX - circX
    distToClosestY = closestY - circY
    
    distToClosestLen = sqrt(distToClosestX**2 + distToClosestY**2)

    outCircPosX = circX + distToClosestX * circRad / distToClosestLen
    outCircPosY = circY + distToClosestY * circRad / distToClosestLen

    if distToClosestLen < circRad:
        return outCircPosX-closestX, outCircPosY-closestY
    else:
        return 0, 0