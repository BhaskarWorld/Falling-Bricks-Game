import pygame
import random
import sys
import time
try:
    import pkg_resources.py2_warn
except ImportError:
    pass

pygame.init()
pygame.font.init()
pygame.mixer.pre_init()

screenWidth = 800
screenHeight = 600

hoverWidth = 115
hoverHeight = 15

hoverx = screenWidth * .5 - hoverWidth * .5
hovery = screenHeight * .95

objectWidth = 10
objectHeight = 30

scl = screenWidth / objectWidth

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
CosmicLatte = (254, 249, 226)
ChoclateBrown = (87, 50, 13)
Midnight = (25, 25, 112)
Darkvanilla = (210, 202, 159)
Burgundy = (128, 0, 21)
a = (226, 207, 161)
b = (150, 170, 145)
darkBrown = (83, 52, 30)

clock = pygame.time.Clock()

music = pygame.mixer.music.load("Light-Digital.mp3")
gameover = pygame.mixer.Sound("gameover.wav")
gameOverImage = pygame.image.load('gameoverimg.png')
gameWindow = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Falling Bricks')

hoverx_change = 0
hoverobjectSpeed = 10

objectPosx = []
objectPosy = []
objectPosy_change = 0
objectSpeed = 5

counter = 0
fps = 60

nObject = 1

score = 0

gameOver = False
Pause = False


def drawHover():
    pygame.draw.rect(gameWindow, ChoclateBrown, (hoverx, hovery, hoverWidth, hoverHeight))


def drawObject():
    global objectPosx, objectPosy, score
    for p in range(len(objectPosx)):
        objectPosy[p] += objectSpeed
        pygame.draw.rect(gameWindow, Midnight, (objectPosx[p], objectPosy[p], objectWidth, objectHeight))


def popObject():
    global objectPosx, objectPosy, score, objectSpeed, nObject
    if len(objectPosx) >= 1:
        if objectPosy[0] >= screenHeight:
            objectPosx.pop(0)
            objectPosy.pop(0)
            score += 1
            objectSpeed += 0.1
            if (nObject > .2):
                nObject -= 0.009


def pushObject():
    global counter
    if counter >= (nObject) * fps:
        objectPosx.append(random.randint(0, scl) * objectWidth)
        objectPosy.append(0)
        counter = 0


def checkcollision():
    global gameOver, gameWindow
    for objects in range(len(objectPosx)):
        if (objectPosy[objects] + objectHeight) >= hovery and (objectPosy[objects] <= hovery) and (
                objectPosx[objects] >= hoverx) and (objectPosx[objects] <= hoverx + hoverWidth):
            gameOver = True
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(gameover)
            renderMessage('GameOver', 115, Darkvanilla, 'Cambria', screenWidth / 2, screenHeight / 2, True)
            pygame.display.update()
            time.sleep(4)

            reRun()


def renderMessage(text, size, color, font, x, y, center, bold=False, italic=False):
    myfont = pygame.font.SysFont(font, size, bold, italic)
    textsurface = myfont.render(text, True, color)
    textPos = textsurface.get_rect()
    textPos.center = (x, y)
    if center:
        gameWindow.blit(textsurface, textPos)
    else:
        gameWindow.blit(textsurface, (x, y))


def pause():
    global Pause
    while Pause:
        renderMessage('Paused', 100, Darkvanilla, 'Cambria', screenWidth / 2, screenHeight / 2, True)
        pygame.mixer.music.pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Pause = False
                    pygame.mixer.music.unpause()
        pygame.display.update()


def restart():
    global gameOver, score, nObject, objectSpeed, hoverx_change, hoverx, hovery
    score = 0
    nObject = 1
    objectSpeed = 5
    objectPosx.clear()
    objectPosy.clear()
    score = 0
    gameOver = False
    hoverx_change = 0

    hoverx = screenWidth * .5 - hoverWidth * .5
    hovery = screenHeight * .95

    gameLoop()


def button(win, msg, size, msgColor, color1, color2, posx, posy, btn_width, btn_height, task):
    mousePos = pygame.mouse.get_pos()
    mouseClick = pygame.mouse.get_pressed()

    if posx <= mousePos[0] <= posx + btn_width and posy <= mousePos[1] <= posy + btn_height:
        pygame.draw.rect(win, color1, (posx, posy, btn_width, btn_height))
        if mouseClick[0] == 1:
            task()
    else:
        pygame.draw.rect(win, color2, (posx, posy, btn_width, btn_height))

    renderMessage(msg, size, msgColor, 'Cambria', (posx + (btn_width / 2)), (posy + (btn_height / 2)), True)
    # print(mouseClick, mousePos)


def reRun():
    while gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        gameWindow.fill(CosmicLatte)
        gameWindow.blit(gameOverImage, (200, 100))
        button(gameWindow, 'Restart', 20, white, a, b, 200, 400, 120, 40, restart)
        button(gameWindow, 'Quit', 20, white, a, b, 500, 400, 120, 40, sys.exit)
        pygame.display.update()
        clock.tick(fps / 4)


def start():
    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        gameWindow.fill(CosmicLatte)
        renderMessage("Let's Begin", 130, darkBrown, 'Edwardian Script ITC', 400, 200, True)
        button(gameWindow, 'Start', 20, green, a, CosmicLatte, 325, 300, 150, 50, gameLoop)
        button(gameWindow, 'Exit', 20, red, a, CosmicLatte, 325, 370, 150, 50, sys.exit)

        pygame.display.update()
        clock.tick(fps / 4)


def gameLoop():
    global hoverx, hovery, hoverx_change, hoverobjectSpeed, objectPosx, objectPosy, objectPosy_change, objectSpeed, counter, fps, nObject, score, gameOver, Pause
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(.1)
    # pygame.mixer.Sound.set_volume(.1)
    while not gameOver:

        pause()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and not gameOver:
                if event.key == pygame.K_LEFT:
                    hoverx_change += -hoverobjectSpeed
                if event.key == pygame.K_RIGHT:
                    hoverx_change += hoverobjectSpeed
                if event.key == pygame.K_SPACE:
                    Pause = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    hoverx_change = 0

        if hoverx < 0:
            hoverx = 0
        elif hoverx + hoverWidth > screenWidth:
            hoverx = screenWidth - hoverWidth

        hoverx += hoverx_change

        gameWindow.fill(CosmicLatte)

        counter += 1  # it is to add  delay in appending object coodinates in the object list

        drawHover()
        drawObject()
        pushObject()
        popObject()
        checkcollision()

        txtScore = 'score: ' + str(score * 5)
        renderMessage(txtScore, 20, Burgundy, 'Cambria', 0, 0, False)  # render score

        pygame.display.update()
        clock.tick(fps)
        mousePos = pygame.mouse.get_pos()
        mouseClick = pygame.mouse.get_pressed()


start()
pygame.quit()
quit()
