import pygame
import sys
import random
from time import sleep

BLACK = (0, 0, 0)
padWidth = 480
padHeight = 640
rockImage = ['python 1.png', 'swift.png', 'sode 1.png', 'ball2 1.png', 'kotlin 1.png']
explosionSound = 'aaa.mp3'
missileSound = 'mis.mp3'
startSound = 'start.mp3'
moveSound = 'Coin 1.mp3'

def writeMessage(text):
    global gamePad
    textfont = pygame.font.Font('abc.ttf', 80)
    text = textfont.render(text, True, (255, 0, 0))
    textops = text.get_rect()
    textops.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textops)
    pygame.display.update()
    sleep(2)
    runGame()

def crash():
    global gamePad
    pygame.mixer.music.stop()
    pygame.mixer.Sound(explosionSound).play()
    writeMessage('신민호 파괴!')

def gameOver():
    global gamePad
    pygame.mixer.music.stop()
    pygame.mixer.Sound(explosionSound).play()
    writeMessage('게임 오버!')

def writeScore(count):
    global gamePad
    font = pygame.font.Font('abc.ttf', 20)
    text = font.render('해결한 과제수: ' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

def writePassed(count):
    global gamePad
    font = pygame.font.Font('abc.ttf', 20)
    text = font.render('실패 과제: ' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (360, 0))

def writeGrade(count):
    global gamePad
    font = pygame.font.Font('abc.ttf', 20)
    grade = ''
    
    if count < 50:
        grade = 'F'
    elif count < 70:
        grade = 'D'
    elif count < 100:
        grade = 'C'
    elif count < 150:
        grade = 'B'
    else:
        grade = 'A'
        
    text = font.render('등급: ' + grade, True, (255, 255, 255))
    gamePad.blit(text, (10, 20))

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

def initGame():
    global gamePad, clock, backGround, player, playerWidth, playerHeight, missile, missileXY, explosion
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    
    pygame.display.set_caption('대소고 지키기')
    backGround = pygame.image.load('school.jpg')
    player = pygame.image.load('player.png')
    missile = pygame.image.load('nife.png')
    explosion = pygame.transform.scale(pygame.image.load('boob.png'), (50, 50))
    
    playerWidth = 50
    playerHeight = 50
    player = pygame.transform.scale(player, (playerWidth, playerHeight))
    missile = pygame.transform.scale(missile, (int(playerWidth / 3), playerHeight))
    missileXY = []
    
    pygame.mixer.music.load('aaa.mp3')
    pygame.mixer.music.play(-1)
    
    clock = pygame.time.Clock()

def runGame():
    global gamePad, clock, backGround, player, missile, missileXY, explosion

    isShot = False
    shotCount = 0
    rockPassed = 0

    x = padWidth * 0.45
    y = padHeight * 0.9
    
    playerX = 0
    playerY = 0

    missileXY = []

    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]

    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX -= 7.5
                    pygame.mixer.Sound(moveSound).play()
                elif event.key == pygame.K_RIGHT:
                    playerX += 7.5
                    pygame.mixer.Sound(moveSound).play()
                elif event.key == pygame.K_UP:
                    playerY -= 5
                    pygame.mixer.Sound(moveSound).play()
                elif event.key == pygame.K_DOWN:
                    playerY += 5
                    pygame.mixer.Sound(moveSound).play()
                elif event.key == pygame.K_SPACE:
                    missileX = x + playerWidth / 2
                    missileY = y - playerHeight
                    missileXY.append([missileX, missileY])
                    pygame.mixer.Sound(missileSound).play()  # 미사일 소리 재생

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY = 0

        x += playerX
        y += playerY

        if x < 0:
            x = 0
        elif x > padWidth - playerWidth:
            x = padWidth - playerWidth

        if y < 0:
            y = 0
        elif y > padHeight - playerHeight:
            y = padHeight - playerHeight

        gamePad.fill(BLACK)
        drawObject(backGround, 0, 0)

        if y < rockY + rockHeight:
            if (rockX > x and rockX < x + playerWidth) or \
                    (rockX + rockWidth > x and rockX + rockWidth < x + playerWidth):
                crash()

        drawObject(player, x, y)

        if rockPassed == 3:
            gameOver()

        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]

                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass

        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        writeScore(shotCount)
        
        writeGrade(shotCount)

        rockY += rockSpeed

        if rockY > padHeight:
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        writePassed(rockPassed)

        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass

        if isShot:
            drawObject(explosion, rockX, rockY)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            isShot = False

            rockSpeed += 0.03
            
            if rockSpeed >= 10:
                rockSpeed = 10

        drawObject(rock, rockX, rockY)

        pygame.display.update()
        
        clock.tick(60)

    pygame.quit()

initGame()

pygame.mixer.music.play()  # 스타트 소리 재생

runGame()