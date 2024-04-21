import pygame, carlsExtension

# Programmeigenschaften einstellen
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

# Pygame starten
pygame.init()

# Fenster erstellen
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Zeit einstellen
framesPerSecond = 30 # auch kurz FPS genannt
fpsClock = pygame.time.Clock()


# Farben definieren
WHITE = (255,255,255)
BLACK = (0,0,0)



# Spielschleife starten
gameLoopRuns = True
while gameLoopRuns:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoopRuns = False

    keysPressed = carlsExtension.getKeys()

    window.fill(BLACK) # Fenster schwarz zeichnen
    

    pygame.display.update() # Gezeichnetes anzeigen

    fpsClock.tick(framesPerSecond) # Maximal framesPerSecond-viele Bilder pro Sekunde anzeigen

pygame.quit()

