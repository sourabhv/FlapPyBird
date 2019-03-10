from itertools import cycle
import random
import sys
import math

import pygame
from pygame.locals import *


FPS = 30
SCREENWIDTH  = 288
SCREENHEIGHT = 512
# amount by which base can maximum shift to left
PIPEGAPSIZE  = 100 # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}
# True if the user plays the fury mode
FURYMODE = False
# In fury mode, the pipe sapwn system is different than in
# normal mode, we add pipes with a "timer" (a frame counter)
FURYMODE_FRAMES_TO_SPAWN_PIPES = 35
# pipes particles amount (for each pipe)
FURYMODE_PARTICLES = 8
# max particles for each pipe hit
FURYMODE_PARTICLES_MAX = 48

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        # amount by which base can maximum shift to left
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    'assets/sprites/background-day.png',
    'assets/sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
)


try:
    xrange
except NameError:
    xrange = range


def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )

    # game over sprite
    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    # message sprite for welcome screen
    IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
    # base (ground) sprite
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()

    # the "fury mode" button for welcome screen (with the key)
    IMAGES['furymode'] = pygame.image.load('assets/sprites/furymode.png').convert_alpha()
    IMAGES['furymode-key'] = pygame.image.load('assets/sprites/furymode-key.png').convert_alpha()


    # sounds
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die']    = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)

    while True:
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        # select random player sprites
        randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
        )

        # select random pipe sprites
        pipeindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.rotate(
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), 180),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )

        # pipes' particles for fury mode
        # pipes are green
        if pipeindex == 0:
            IMAGES['pipe-particle'] = (
                pygame.image.load('assets/sprites/particles-green-0.png').convert_alpha(),
                pygame.image.load('assets/sprites/particles-green-1.png').convert_alpha(),
                pygame.image.load('assets/sprites/particles-green-2.png').convert_alpha(),
                pygame.image.load('assets/sprites/particles-green-3.png').convert_alpha(),
                pygame.image.load('assets/sprites/particles-green-4.png').convert_alpha(),
                pygame.image.load('assets/sprites/particles-green-5.png').convert_alpha(),
                pygame.image.load('assets/sprites/particles-green-6.png').convert_alpha(),
                pygame.image.load('assets/sprites/particles-green-7.png').convert_alpha(),
            )
        else:
            IMAGES['pipe-particle'] = (
                pygame.image.load('assets/sprites/particles-red-0.png').convert_alpha(),
                pygame.image.load('assets/sprites/particles-red-1.png').convert_alpha(),
                pygame.image.load('assets/sprites/particles-red-2.png').convert_alpha(),
                pygame.image.load('assets/sprites/particles-red-3.png').convert_alpha(),
                pygame.image.load('assets/sprites/particles-red-4.png').convert_alpha(),
                pygame.image.load('assets/sprites/particles-red-5.png').convert_alpha(),
                pygame.image.load('assets/sprites/particles-red-6.png').convert_alpha(),
                pygame.image.load('assets/sprites/particles-red-7.png').convert_alpha(),
            )


        # hismask for pipes
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )

        # hitmask for player
        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
        )

        movementInfo = showWelcomeAnimation()
        crashInfo = mainGame(movementInfo)
        showGameOverScreen(crashInfo)


def showWelcomeAnimation():
    """Shows welcome screen animation of flappy bird"""
    global FURYMODE

    # index of player to blit on screen
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)

    furymodex = int((SCREENWIDTH - IMAGES['furymode'].get_width()) / 2)
    furymodey = int(SCREENHEIGHT * 0.68)
    # just at right of the fury mode button (8 is right padding)
    furymodeKeyX = furymodex + IMAGES['furymode'].get_width() + 8
    furymodeKeyY = furymodey + IMAGES['furymode-key'].get_height() // 2

    basex = 0
    # amount by which base can maximum shift to left
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # player shm for up-down motion on welcome screen
    playerShmVals = {'val': 0, 'dir': 1}

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            # (1) key for fury mode
            if event.type == KEYDOWN and event.key == K_1:
                FURYMODE = True
                # make first flap sound and return values for mainGame
                SOUNDS['wing'].play()
                return {
                    'playery': playery + playerShmVals['val'],
                    'basex': basex,
                    'playerIndexGen': playerIndexGen,
                }
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # make first flap sound and return values for mainGame
                SOUNDS['wing'].play()
                return {
                    'playery': playery + playerShmVals['val'],
                    'basex': basex,
                    'playerIndexGen': playerIndexGen,
                }

        # adjust playery, playerIndex, basex
        if (loopIter + 1) % 5 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 4) % baseShift)
        playerShm(playerShmVals)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['player'][playerIndex],
                    (playerx, playery + playerShmVals['val']))
        SCREEN.blit(IMAGES['message'], (messagex, messagey))
        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        SCREEN.blit(IMAGES['furymode'], (furymodex, furymodey))
        SCREEN.blit(IMAGES['furymode-key'], (furymodeKeyX, furymodeKeyY))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainGame(movementInfo):
    global FURYMODE, FURYMODE_FRAMES_TO_SPAWN_PIPES

    score = playerIndex = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']
    playerx, playery = int(SCREENWIDTH * 0.2), movementInfo['playery']

    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # no need to spawn pipes at start
    if FURYMODE:
        # list of upper pipes
        upperPipes = []

        # list of lowerpipe
        lowerPipes = []

        # list of particles
        # a particle is an object with attributes:
        # {'x': position-x, 'y': position-y,
        # 'vx': velocity-x, 'vy': velocity-y,
        # 'i': index in textures list} 
        particles = []

    else:
        # get 2 new pipes to add to upperPipes lowerPipes list
        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()

        # list of upper pipes
        upperPipes = [
            {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
        ]

        # list of lowerpipe
        lowerPipes = [
            {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
        ]

    pipeVelX = -4

    # player velocity, max velocity, downward accleration, accleration on flap
    playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
    playerMaxVelY =  10   # max vel along Y, max descend speed
    playerMinVelY =  -8   # min vel along Y, max ascend speed
    playerAccY    =   1   # players downward accleration
    playerRot     =  45   # player's rotation
    playerVelRot  =   3   # angular speed
    playerRotThr  =  20   # rotation threshold
    playerFlapAcc =  -9   # players speed on flapping
    playerFlapped = False # True when player flaps


    # The counter to spawn new pipes 
    furymodePipeFrameCounter = 0


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > -2 * IMAGES['player'][0].get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    SOUNDS['wing'].play()

        # check for crash here
        crashTest = checkCrash({'x': playerx, 'y': playery, 'index': playerIndex},
                               upperPipes, lowerPipes)

        if crashTest[0]:
            # the player hits a pipe in fury mode
            if FURYMODE and not crashTest[1]:
                spawnParticles(particles, crashTest[3])

                # remove the pipe
                # it's an upper pipe
                if crashTest[2]:
                    upperPipes.remove(crashTest[3])
                # it's a lower pipe
                else:
                    lowerPipes.remove(crashTest[3])

            else:
                return {
                    'y': playery,
                    'groundCrash': crashTest[1],
                    'basex': basex,
                    'upperPipes': upperPipes,
                    'lowerPipes': lowerPipes,
                    'score': score,
                    'playerVelY': playerVelY,
                    'playerRot': playerRot
                }

        # check for score
        playerMidPos = playerx + IMAGES['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                SOUNDS['point'].play()

        # playerIndex basex change
        if (loopIter + 1) % 3 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)

        # rotate the player
        if playerRot > -90:
            playerRot -= playerVelRot

        # player's movement
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False

            # more rotation to cover the threshold (calculated in visible rotation)
            playerRot = 45

        playerHeight = IMAGES['player'][playerIndex].get_height()
        playery += min(playerVelY, BASEY - playery - playerHeight)

        # move pipes to left
        for uPipe in upperPipes:
            uPipe['x'] += pipeVelX

        for lPipe in lowerPipes:
            lPipe['x'] += pipeVelX

        # update (add / remove) pipes and particles
        if FURYMODE:
            furymodePipeFrameCounter += 1
            # the counter has the max value, we must spawn new pipes
            if furymodePipeFrameCounter == FURYMODE_FRAMES_TO_SPAWN_PIPES:
                # counter reset
                furymodePipeFrameCounter = 0
                
                # pipe spawn
                pipes = getRandomPipe()
                upperPipes.append(pipes[0])
                lowerPipes.append(pipes[1])

            # check if a pipe must be removed from the list
            for uPipe in upperPipes:
                if uPipe['x'] < -IMAGES['pipe'][0].get_width():
                    upperPipes.remove(uPipe)
            for lPipe in lowerPipes:
                if lPipe['x'] < -IMAGES['pipe'][0].get_width():
                    lowerPipes.remove(lPipe)

            # particles
            for particle in particles:
                # speed
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']

                # gravity
                particle['vy'] += playerAccY

                # remove if the particle is under the ground
                if particle['y'] >= BASEY:
                    particles.remove(particle)

        else:
            # add new pipes when first pipe is about to touch left of screen
            if 0 < upperPipes[0]['x'] < 5:
                newPipe = getRandomPipe()
                upperPipes.append(newPipe[0])
                lowerPipes.append(newPipe[1])

            # remove first pipe if its out of the screen
            if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
                lowerPipes.pop(0)
                upperPipes.pop(0)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe in upperPipes:
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))

        for lPipe in lowerPipes:
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        # pipes' particles
        if FURYMODE:
            for particle in particles:
                SCREEN.blit(IMAGES['pipe-particle'][particle['i']], (particle['x'], particle['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))

        # print score so player overlaps the score
        showScore(score)

        # Player rotation has a threshold
        visibleRot = playerRotThr
        if playerRot <= playerRotThr:
            visibleRot = playerRot
        
        playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], visibleRot)
        SCREEN.blit(playerSurface, (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def showGameOverScreen(crashInfo):
    """crashes the player down ans shows gameover image"""
    global FURYMODE

    FURYMODE = False

    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']
    playerHeight = IMAGES['player'][0].get_height()
    playerVelY = crashInfo['playerVelY']
    playerAccY = 2
    playerRot = crashInfo['playerRot']
    playerVelRot = 7

    basex = crashInfo['basex']

    upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

    # play hit and die sounds
    SOUNDS['hit'].play()
    if not crashInfo['groundCrash']:
        SOUNDS['die'].play()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery + playerHeight >= BASEY - 1:
                    return

        # player y shift
        if playery + playerHeight < BASEY - 1:
            playery += min(playerVelY, BASEY - playery - playerHeight)

        # player velocity change
        if playerVelY < 15:
            playerVelY += playerAccY

        # rotate only when it's a pipe crash
        if not crashInfo['groundCrash']:
            if playerRot > -90:
                playerRot -= playerVelRot

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        showScore(score)

        playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
        SCREEN.blit(playerSurface, (playerx,playery))

        FPSCLOCK.tick(FPS)
        pygame.display.update()


def playerShm(playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
         playerShm['val'] += 1
    else:
        playerShm['val'] -= 1


def getRandomPipe():
    """ returns a randomly generated pipe """
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]

def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()

def spawnParticles(particles, pipe):
    """
        Add paticles to the particle list randomly
    generated with pipe's rectangle (hitbox)
    """
    global FURYMODE_PARTICLES, FURYMODE_PARTICLES_MAX, SOUNDS

    pipeW = IMAGES['pipe'][0].get_width()
    pipeH = IMAGES['pipe'][0].get_height()

    for i in range(FURYMODE_PARTICLES_MAX):
        particle = {}
        particle['x'] = random.randint(pipe['x'], pipe['x'] + pipeW)
        particle['y'] = random.randint(pipe['y'], pipe['y'] + pipeH)
        particle['i'] = random.randint(1, FURYMODE_PARTICLES) - 1

        # random angle for a minimum velocity
        vel = random.random() * 10 + 5
        aMin = -math.pi * .35
        aMax = math.pi * .25
        angle = random.random() * (aMax - aMin) + aMin
        particle['vx'] = math.cos(angle) * vel
        particle['vy'] = math.sin(angle) * vel

        particles.append(particle)

    # sound effect
    SOUNDS['hit'].play()



def checkCrash(player, upperPipes, lowerPipes):
    """returns True if player collders with base or pipes."""
    global FURYMODE

    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]

    else:
        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe in upperPipes:
            # pipe rect
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)

            # player and pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]

            # if bird collided with pipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)

            if uCollide:
                # for fury mode we want to break the pipe so we
                # must return which pipe is colliding (lower or upper)
                if FURYMODE:
                    return [True, False, True, uPipe]
                # normal mode
                return [True, False]

        for lPipe in lowerPipes:
            # pipe rect
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            lHitmask = HITMASKS['pipe'][0]

            # if bird collided with pipe
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if lCollide:
                # for fury mode we want to break the pipe so we
                # must return which pipe is colliding (lower or upper)
                if FURYMODE:
                    return [True, False, False, lPipe]
                # normal mode
                return [True, False]



    return [False, False]

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

if __name__ == '__main__':
    main()
