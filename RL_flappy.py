from itertools import cycle

import random
import sys
from typing import Dict, Tuple

import pygame
from pygame.locals import *

from RL_agents import Flappy_QAgent

FPS = 30
SCREENWIDTH  = 288
SCREENHEIGHT = 512
PIPEGAPSIZE  = 100  # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

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

FPSCLOCK = pygame.time.Clock()

playerHeight = pygame.image.load(PLAYERS_LIST[0][0]).get_height()
playerWidth = pygame.image.load(PLAYERS_LIST[0][0]).get_width()
pipesHeight = pygame.image.load(PIPES_LIST[0]).get_height()
pipesWidth = pygame.image.load(PIPES_LIST[0]).get_width()


def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask


# player and upper/lower pipe hitmasks
pHitMask = getHitmask(pygame.image.load(PLAYERS_LIST[0][0]))
uHitmask = getHitmask(pygame.image.load(PIPES_LIST[0]))
lHitmask = getHitmask(pygame.transform.flip(pygame.image.load(PIPES_LIST[0]), False, True))


def main(QAgent=None):
    global SCREEN
    pygame.init()

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
            pygame.transform.flip(
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), False, True),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )

        # hitmask for pipes
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
        crashInfo = mainGame(movementInfo, QAgent=QAgent)
        showGameOverScreen(crashInfo)


def showWelcomeAnimation():
    """Shows welcome screen animation of flappy bird"""
    # index of player to blit on screen
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)

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
        SCREEN.blit(IMAGES['background'], (0, 0))
        SCREEN.blit(IMAGES['player'][playerIndex],
                    (playerx, playery + playerShmVals['val']))
        SCREEN.blit(IMAGES['message'], (messagex, messagey))
        SCREEN.blit(IMAGES['base'], (basex, BASEY))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainGame(movementInfo, QAgent: Flappy_QAgent = None, gui: bool = True):
    score = playerIndex = 0  # loopIter = 0
    # playerIndexGen = movementInfo['playerIndexGen']
    playerx, playery = int(SCREENWIDTH * 0.2), movementInfo['playery']

    basex = movementInfo['basex']
    baseShift = pygame.image.load('assets/sprites/base.png').get_width() - pygame.image.load(BACKGROUNDS_LIST[0]).get_width()

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

    # player velocity, max velocity, downward acceleration, acceleration on flap
    playerVelY = -9        # player's velocity along Y, default same as playerFlapped
    playerMaxVelY = 10     # max vel along Y, max descend speed
    playerAccY = 1         # players downward acceleration
    playerFlapAcc = -9     # players speed on flapping
    playerFlapped = False  # True when player flaps

    if QAgent:
        QAgent.update_state(player_pos={"x": playerx, "y": playery},
                            player_vel=playerVelY,
                            lower_pipes=lowerPipes)

    while True:
        if QAgent:
            QAgent.choose_action(state=QAgent.curr_state)
            if QAgent.action == "flap":
                if playery > -2 * pygame.image.load(PLAYERS_LIST[0][0]).get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    if gui:
                        SOUNDS['wing'].play()

            QAgent.update_state(player_pos={"x": playerx, "y": playery},
                                player_vel=playerVelY,
                                lower_pipes=lowerPipes)
        else:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if playery > -2 * IMAGES['player'][0].get_height():
                        playerVelY = playerFlapAcc
                        playerFlapped = True
                        SOUNDS['wing'].play()

        # print(f"player (x, y) to pipe: ({playerx - lowerPipes[0]['x']}, {playery - lowerPipes[0]['y']}), pipes x {[pipe['x'] for pipe in lowerPipes]}")

        # check for crash here
        crashTest = checkCrash(player={'x': playerx, 'y': playery},
                               upperPipes=upperPipes, lowerPipes=lowerPipes)
        if crashTest[0]:
            return {
                'y': playery,
                'pos': [playerx, playery],
                'groundCrash': crashTest[1],
                'basex': basex,
                'upperPipes': upperPipes,
                'lowerPipes': lowerPipes,
                'score': score,
                'playerVelY': playerVelY,
                'playerRot': 0
            }

        # check for score
        playerMidPos = playerx + pygame.image.load(PLAYERS_LIST[0][0]).get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + pygame.image.load(PIPES_LIST[0]).get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                if gui:
                    SOUNDS['point'].play()

        # playerIndex basex change
        # if (loopIter + 1) % 3 == 0:
        #     playerIndex = next(playerIndexGen)
        # loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)

        # rotate the player
        # if playerRot > -90:
        #     playerRot -= playerVelRot

        # player's movement
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False
            # more rotation to cover the threshold (calculated in visible rotation)
            # playerRot = 45

        playerHeight = pygame.image.load(PLAYERS_LIST[0][0]).get_height()
        playery += min(playerVelY, BASEY - playery - playerHeight)

        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 3 > len(upperPipes) and -50 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if len(upperPipes) > 0 and upperPipes[0]['x'] < -pygame.image.load(PIPES_LIST[0]).get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # add new

        # draw sprites
        if gui:
            SCREEN.blit(IMAGES['background'], (0, 0))

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

            SCREEN.blit(IMAGES['base'], (basex, BASEY))
            # print score so player overlaps the score
            showScore(score)

            playerSurface = IMAGES['player'][playerIndex]
            SCREEN.blit(playerSurface, (playerx, playery))

            pygame.display.update()
            FPSCLOCK.tick(FPS)


def showGameOverScreen(crashInfo):
    """crashes the player down and shows gameover image"""
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
        SCREEN.blit(IMAGES['background'], (0, 0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        showScore(score)

        playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
        SCREEN.blit(playerSurface, (playerx, playery))
        SCREEN.blit(IMAGES['gameover'], (50, 180))

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
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    # pipeHeight = pygame.image.load(PIPES_LIST[0]).get_height()  # pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipesHeight},   # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE},  # lower pipe
    ]


def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0  # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperPipes, lowerPipes):
    """returns True if player collides with base or pipes."""
    player['w'] = playerWidth
    player['h'] = playerHeight

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                                 player['w'], player['h'])
        pipeW = pipesWidth
        pipeH = pipesHeight

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
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
            if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                return True
    return False


class Flappy_Environment:
    """Environment abstraction of the game. No gui not visuals, just the basics to train an agent.

    The state is composed of a dict with all relevant information:
    - playerPos : dict with {"x", "y"} position of the player
    - playerVelY : int with the y velocity of the player
    - upperPipes : list of dicts with {"x", "y"} position of the pipes
    - lowerPipes : list of dicts with {"x", "y"} position of the pipes
    - crashInfo : bool array with [crash, groundCrash]
    - score

    The agent should process this state information to optimize the state space.
    """

    def __init__(self, step_reward, score_reward, die_reward) -> None:

        self.step_reward = step_reward
        self.score_reward = step_reward + score_reward
        self.die_reward = die_reward

        print(f"Flappy_Environment initated with size ({SCREENWIDTH}x{SCREENHEIGHT}) and gap size {PIPEGAPSIZE}\n" +
              f"Player has size ({playerWidth}x{playerHeight}) and the pipes are {pipesWidth} wide.")

        self.action_space = ["flap", ""]

        return

    def _return_state(self):
        return {
            "playerPos": {"x": self.playerx, "y": self.playery},
            "playerVelY": self.playerVelY,
            "upperPipes": self.upperPipes,
            "lowerPipes": self.lowerPipes,
            "crashInfo": self.crashTest,
            "score": self.score
        }

    def set_up(self) -> Dict:
        """Set up the environment with default values
        """
        self.score = self.playerIndex = 0
        self.crashTest = [False, False]
        self.playerx, self.playery = int(SCREENWIDTH * 0.2), 308

        # get 2 new pipes to add to upperPipes lowerPipes list
        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()

        # list of upper pipes
        self.upperPipes = [
            {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
        ]

        # list of lower pipes
        self.lowerPipes = [
            {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
        ]

        self.pipeVelX = -4  # NOTE: adjust

        # player velocity, max velocity, downward acceleration, acceleration on flap
        self.playerVelY = -9        # player's velocity along Y, default same as playerFlapped
        self.playerMaxVelY = 10     # max vel along Y, max descend speed
        self.playerAccY = 1         # players downward acceleration
        self.playerFlapAcc = -9     # players speed on flapping
        self.playerFlapped = False  # True when player flaps

        return self._return_state()

    def take_action(self, action) -> Tuple[int, Dict]:
        """Take an action and return the reward and new state of the environment

        Args:
            action (_type_): action to take

        Returns:
            Tuple[int, Dict]: reward and new state. See class docstring for definiton of state.
        """

        if action not in self.action_space:
            print(f"ERROR: Passed action ({action}) not in action space {self.action_space}. Please ensure action is valid.")
            exit()

        if action == "flap":
            if self.playery > -2 * playerHeight:
                self.playerVelY = self.playerFlapAcc
                self.playerFlapped = True

        # check for crash here
        self.crashTest = checkCrash(player={'x': self.playerx, 'y': self.playery},
                                    upperPipes=self.upperPipes, lowerPipes=self.lowerPipes)
        if self.crashTest[0]:
            return self.die_reward, self._return_state()

        # check for score
        scored_point = False
        playerMidPos = self.playerx + playerWidth / 2
        for pipe in self.upperPipes:
            pipeMidPos = pipe['x'] + pipesWidth / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                self.score += 1
                scored_point = True

        # player's movement
        if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
            self.playerVelY += self.playerAccY
        if self.playerFlapped:
            self.playerFlapped = False

        self.playery += min(self.playerVelY, BASEY - self.playery - playerHeight)

        # move pipes to left
        for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
            uPipe['x'] += self.pipeVelX
            lPipe['x'] += self.pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 3 > len(self.upperPipes) and -50 < self.upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            self.upperPipes.append(newPipe[0])
            self.lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if len(self.upperPipes) > 0 and self.upperPipes[0]['x'] < -pipesWidth:
            self.upperPipes.pop(0)
            self.lowerPipes.pop(0)

        if scored_point:
            return self.score_reward, self._return_state()
        else:
            return self.step_reward, self._return_state()


if __name__ == '__main__':
    main()
