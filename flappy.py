import random
import sys

import pygame
from pygame.locals import *


FPS = 30
SCREENWIDTH = 288
SCREENHEIGHT = 512
# image and sound object's dicts
IMAGES, SOUNDS = {}, {}

# list of players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
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


def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')

    # sprites
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

    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png')
    IMAGES['message'] = pygame.image.load('assets/sprites/message.png')
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png')

    # sounds
    SOUNDS['die']    = pygame.mixer.Sound('assets/audio/die.ogg')
    SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit.ogg')
    SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point.ogg')
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh.ogg')
    SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing.ogg')

    while True:
        # sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
        )

        pipeindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha()

        showWelcomeAnimation()
        playerCrashInfo = mainGame()
        showGameOverScreen(playerCrashInfo)

def showWelcomeAnimation():
    playerIndex = 0
    loopIter = 0
    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)
    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)
    basex = 0
    basey = int(SCREENHEIGHT * 0.78)
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    while True:
        SCREEN.fill((255,255,255))
        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['player'][playerIndex], (playerx, playery))
        SCREEN.blit(IMAGES['message'], (messagex, messagey))
        SCREEN.blit(IMAGES['base'], (basex, basey))

        if (loopIter + 1) % 5 == 0:
            playerIndex = (playerIndex + 1) % 3
        loopIter = (loopIter + 1) % 30

        basex = -((-basex + 2) % baseShift)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                break

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainGame():
    pass


def showGameOverScreen(playerCrashInfo):
    pass


if __name__ == '__main__':
    main()
