import random # for generating random numbers
import sys # we will use sys.exit to exit the program
import pygame
from pygame.locals import * # basic pygame imports

# global Variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_IMGS = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/imgs/bird.png'
BACKGROUND = 'gallery/imgs/background.png'
PIPE = 'gallery/imgs/pipe.png'

def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_IMGS['player'].get_height())/2)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_IMGS['background'], (0, 0))    
                SCREEN.blit(GAME_IMGS['player'], (playerx, playery))    
                SCREEN.blit(GAME_IMGS['base'], (basex, GROUNDY))    
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # create 2 pipes for blitting on the screen
    pipe1 = getRandomPipe()
    pipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':pipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':pipe2[0]['y']},
    ]
    # list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':pipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':pipe2[1]['y']},
    ]

    pipeVelX = -4
    
    playerVelY = -9

    playerMaxVelY = 10
    playerMinVelY = -8

    playerAcc = 1

    playerFlapVel = -8 # velocity while flapping
    playerFlapped = False # it is true only when the bird is flapping


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapVel
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        checkCrash = isCollide(playerx, playery, upperPipes, lowerPipes) # check for collision
        if checkCrash:
            return     

        #check for score
        playerPos = playerx + GAME_IMGS['player'].get_width()/2
        for pipe in upperPipes:
            pipePos = pipe['x'] + GAME_IMGS['pipe'][0].get_width()/2
            if pipePos <= playerPos < pipePos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAcc

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_IMGS['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_IMGS['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # use blit for drawing images
        SCREEN.blit(GAME_IMGS['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_IMGS['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_IMGS['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_IMGS['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_IMGS['player'], (playerx, playery))
        digits = [int(x) for x in list(str(score))]
        width = 0
        
        for digit in digits:
            width += GAME_IMGS['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in digits:
            SCREEN.blit(GAME_IMGS['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_IMGS['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_IMGS['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_IMGS['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_IMGS['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_IMGS['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    # generate positions of two pipes (one bottom straight and one top rotated) for blitting on the screen
    pipeHeight = GAME_IMGS['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_IMGS['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},		# upper Pipe
        {'x': pipeX, 'y': y2}	# lower Pipe
    ]
    return pipe

if __name__ == "__main__":
    # main function
    pygame.init() # initialize all pygame's modules

    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Desktop Pet')
    GAME_IMGS['numbers'] = ( 
        pygame.image.load('gallery/imgs/0.png').convert_alpha(),
        pygame.image.load('gallery/imgs/1.png').convert_alpha(),
        pygame.image.load('gallery/imgs/2.png').convert_alpha(),
        pygame.image.load('gallery/imgs/3.png').convert_alpha(),
        pygame.image.load('gallery/imgs/4.png').convert_alpha(),
        pygame.image.load('gallery/imgs/5.png').convert_alpha(),
        pygame.image.load('gallery/imgs/6.png').convert_alpha(),
        pygame.image.load('gallery/imgs/7.png').convert_alpha(),
        pygame.image.load('gallery/imgs/8.png').convert_alpha(),
        pygame.image.load('gallery/imgs/9.png').convert_alpha(),
    )

    GAME_IMGS['base'] =pygame.image.load('gallery/imgs/base.png').convert_alpha()
    GAME_IMGS['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )

    # game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_IMGS['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_IMGS['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() # shows welcome screen to the user until they press a button
        mainGame() # game loop