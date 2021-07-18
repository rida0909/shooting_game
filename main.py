import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("icon.ico")
pygame.display.set_icon(icon)

spaceship = pygame.image.load("space-invaders.png")
spaceshipX = 370
spaceshipY = 500 
spaceshipChangeX = 0

enemyspaceship = []
enemyX = []
enemyY = []
enemyChangeX = []
enemyChangeY = []
no_enemies = 6

for i in range(no_enemies) :
    enemyspaceship.append(pygame.image.load("ovni.png"))
    enemyX.append(random.randint(0,780))
    enemyY.append(random.randint(50,150))
    enemyChangeX.append(4)
    enemyChangeY.append(40)

bullet = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 500 
bulletChangeX = 0
bulletChangeY = 40
bulletState = "hidden"

score = 0

font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

gofont = pygame.font.Font("freesansbold.ttf", 62)

background = pygame.image.load("space.png")

def score_board(x, y) :
    scoreBoard = font.render("Score : " +str(score), True, (255, 255, 255))
    screen.blit(scoreBoard, (x, y))

def gameOver() :
    goBoard = gofont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(goBoard, (200, 250))

def player(x, y) :
    screen.blit(spaceship, (x, y))

def enemy(x, y, i) :
    screen.blit(enemyspaceship[i], (x, y))

def bulletFire(x, y) :
    global bulletState
    screen.blit(bullet, (x + 12, y + 10))
    bulletState = "show"

def collision(enemyX, enemyY, bulletX, bulletY) :
    dis = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if dis < 27 :
        return True
    else :
        return False

windowRunning = True

while windowRunning :
    screen.fill((0, 0, 0))
    screen.blit(background,(0, 0))

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            windowRunning = False

        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT :
                spaceshipChangeX = -5
            if event.key == pygame.K_RIGHT :
                spaceshipChangeX = 5
            if bulletState is "hidden" :
                if event.key == pygame.K_SPACE :
                    bulletX = spaceshipX
                    bulletFire(bulletX, bulletY)
        
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                spaceshipChangeX = 0

    if spaceshipX < 0 :
        spaceshipX = 0
    if spaceshipX > 740 :
        spaceshipX = 740
    
    spaceshipX += spaceshipChangeX

    for i in range(no_enemies) :
        if enemyY[i] > 440 :
            for j in range(no_enemies) :
                enemyY[j] = 2000
            gameOver()
            break

        enemyX[i] += enemyChangeX[i]
        if enemyX[i] < 0 :
            enemyChangeX[i] = 4
            enemyY[i] += enemyChangeY[i]
        elif enemyX[i] > 740 :
            enemyChangeX[i] = -4
            enemyY[i] += enemyChangeY[i]

        is_collision = collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if is_collision :
            bulletState = "hidden"
            bulletY = 500
            score += 1
            enemyspaceship[i] = pygame.image.load("ovni.png")
            enemyX[i] = random.randint(0,780)
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0 :
        bulletY = 500
        bulletState = "hidden"

    if bulletState is "show" :
        bulletFire(bulletX, bulletY)
        bulletY -= bulletChangeY

    player(spaceshipX, spaceshipY)

    score_board(textX, textY)

    pygame.display.update()
