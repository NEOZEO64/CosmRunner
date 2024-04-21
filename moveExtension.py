from PIL import Image
import random, os

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
MoveMargin = 50
imageWidth = WINDOW_WIDTH + 2*MoveMargin
imageHeight = WINDOW_HEIGHT + 2*MoveMargin


enemyRouteFiles = os.listdir("EnemyRoutes/") # EnemyMove-Pngs need a width of 500 and height of 700
enemyRoutes = []

surroundings = [#(x,y) for x in [-1,0,1] for y in [-1,0,1]]# must have length 8
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
    image = Image.open("EnemyRoutes/" + "pixil-frame-{}.png".format(i))
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
        if (x,y) in enemyRoutes[i]:
            startPoints[i].append((x,y))

def getSpawnPoint(index):
    return startPoints[index][random.randrange(0,len(startPoints[index]))]

def getNextPoint(lastx, lasty, index, x, y, dist): # dist (distance): how many pixels to go further!
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