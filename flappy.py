import asyncio
import random
import sys
from itertools import cycle
from typing import Dict, Tuple, Union

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height


# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        "assets/sprites/redbird-upflap.png",
        "assets/sprites/redbird-midflap.png",
        "assets/sprites/redbird-downflap.png",
    ),
    # blue bird
    (
        "assets/sprites/bluebird-upflap.png",
        "assets/sprites/bluebird-midflap.png",
        "assets/sprites/bluebird-downflap.png",
    ),
    # yellow bird
    (
        "assets/sprites/yellowbird-upflap.png",
        "assets/sprites/yellowbird-midflap.png",
        "assets/sprites/yellowbird-downflap.png",
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    "assets/sprites/background-day.png",
    "assets/sprites/background-night.png",
)

# list of pipes
PIPES_LIST = (
    "assets/sprites/pipe-green.png",
    "assets/sprites/pipe-red.png",
)


class Flappy:
    screen: pygame.Surface
    clock: pygame.time.Clock
    fps = 30
    window: Window
    pipe_gap: int
    base_y: float
    images: Dict[str, Union[pygame.Surface, Tuple[pygame.Surface, ...]]]
    sounds: Dict[str, pygame.mixer.Sound]
    hit_masks: Dict[str, Union[Tuple[Tuple[int, ...], ...], Tuple[int, ...]]]

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        self.window = Window(288, 512)
        self.pipe_gap = 100
        self.base_y = self.window.height * 0.79
        self.fps = 30
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.window.width, self.window.height)
        )
        self.images = self.load_images()
        self.sounds = self.load_sounds()
        self.hit_masks = self.load_hit_masks()

    def load_images(self):
        return {
            "numbers": list(
                (
                    pygame.image.load(
                        f"assets/sprites/{num}.png"
                    ).convert_alpha()
                    for num in range(10)
                )
            ),
            # game over sprite
            "gameover": pygame.image.load(
                "assets/sprites/gameover.png"
            ).convert_alpha(),
            # message sprite for welcome screen
            "message": pygame.image.load(
                "assets/sprites/message.png"
            ).convert_alpha(),
            # base (ground) sprite
            "base": pygame.image.load(
                "assets/sprites/base.png"
            ).convert_alpha(),
            **self.randomize_images(),
        }

    def randomize_images(self):
        # select random background sprites
        rand_bg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        # select random player sprites
        rand_player = random.randint(0, len(PLAYERS_LIST) - 1)
        # select random pipe sprites
        rand_pipe = random.randint(0, len(PIPES_LIST) - 1)

        return {
            "background": pygame.image.load(
                BACKGROUNDS_LIST[rand_bg]
            ).convert(),
            "player": (
                pygame.image.load(PLAYERS_LIST[rand_player][0]).convert_alpha(),
                pygame.image.load(PLAYERS_LIST[rand_player][1]).convert_alpha(),
                pygame.image.load(PLAYERS_LIST[rand_player][2]).convert_alpha(),
            ),
            "pipe": (
                pygame.transform.flip(
                    pygame.image.load(PIPES_LIST[rand_pipe]).convert_alpha(),
                    False,
                    True,
                ),
                pygame.image.load(PIPES_LIST[rand_pipe]).convert_alpha(),
            ),
        }

    def load_sounds(self):
        if "win" in sys.platform:
            ext = "wav"
        else:
            ext = "ogg"
        return {
            "die": pygame.mixer.Sound(f"assets/audio/die.{ext}"),
            "hit": pygame.mixer.Sound(f"assets/audio/hit.{ext}"),
            "point": pygame.mixer.Sound(f"assets/audio/point.{ext}"),
            "swoosh": pygame.mixer.Sound(f"assets/audio/swoosh.{ext}"),
            "wing": pygame.mixer.Sound(f"assets/audio/wing.{ext}"),
        }

    def load_hit_masks(self):
        return {
            # hitmask for pipes
            "pipe": (
                self.get_hit_mask(self.images["pipe"][0]),
                self.get_hit_mask(self.images["pipe"][1]),
            ),
            # hitmask for player
            "player": (
                self.get_hit_mask(self.images["player"][0]),
                self.get_hit_mask(self.images["player"][1]),
                self.get_hit_mask(self.images["player"][2]),
            ),
        }

    def get_hit_mask(self, image):
        """returns a hitmask using an image's alpha."""
        mask = []
        for x in range(image.get_width()):
            mask.append([])
            for y in range(image.get_height()):
                mask[x].append(bool(image.get_at((x, y))[3]))
        return mask

    async def start(self):
        while True:
            movement_info = await self.splash()
            crash_info = await self.play(movement_info)
            await self.game_over(crash_info)

    async def splash(self):
        """Shows welcome splash screen animation of flappy bird"""
        # index of player to blit on screen
        player_index = 0
        player_index_gen = cycle([0, 1, 2, 1])
        # iterator used to change player_index after every 5th iteration
        loop_iter = 0

        player_x = int(self.window.width * 0.2)
        player_y = int(
            (self.window.height - self.images["player"][0].get_height()) / 2
        )

        message_x = int(
            (self.window.width - self.images["message"].get_width()) / 2
        )
        message_y = int(self.window.height * 0.12)

        base_x = 0
        # amount by which base can maximum shift to left
        baseShift = (
            self.images["base"].get_width()
            - self.images["background"].get_width()
        )

        # player shm for up-down motion on welcome screen
        player_shm_vals = {"val": 0, "dir": 1}

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    pygame.quit()
                    sys.exit()
                if self.is_tap_event(event):
                    # make first flap sound and return values for mainGame
                    self.sounds["wing"].play()
                    return {
                        "player_y": player_y + player_shm_vals["val"],
                        "base_x": base_x,
                        "player_index_gen": player_index_gen,
                    }

            # adjust player_y, player_index, base_x
            if (loop_iter + 1) % 5 == 0:
                player_index = next(player_index_gen)
            loop_iter = (loop_iter + 1) % 30
            base_x = -((-base_x + 4) % baseShift)
            self.player_shm(player_shm_vals)

            # draw sprites
            self.screen.blit(self.images["background"], (0, 0))
            self.screen.blit(
                self.images["player"][player_index],
                (player_x, player_y + player_shm_vals["val"]),
            )
            self.screen.blit(self.images["message"], (message_x, message_y))
            self.screen.blit(self.images["base"], (base_x, self.base_y))

            pygame.display.update()
            await asyncio.sleep(0)
            self.clock.tick(self.fps)

    def is_tap_event(self, event):
        left, _, _ = pygame.mouse.get_pressed()
        space_or_up = event.type == KEYDOWN and (
            event.key == K_SPACE or event.key == K_UP
        )
        screen_tap = event.type == pygame.FINGERDOWN
        return left or space_or_up or screen_tap

    def player_shm(self, shm):
        """oscillates the value of shm['val'] between 8 and -8"""
        if abs(shm["val"]) == 8:
            shm["dir"] *= -1

        if shm["dir"] == 1:
            shm["val"] += 1
        else:
            shm["val"] -= 1

    async def play(self, movement_nfo):
        score = playerIndex = loopIter = 0
        player_index_gen = movement_nfo["player_index_gen"]
        player_x, player_y = (
            int(self.window.width * 0.2),
            movement_nfo["player_y"],
        )

        base_x = movement_nfo["base_x"]
        baseShift = (
            self.images["base"].get_width()
            - self.images["background"].get_width()
        )

        # get 2 new pipes to add to upperPipes lowerPipes list
        newPipe1 = self.get_random_pipe()
        newPipe2 = self.get_random_pipe()

        # list of upper pipes
        upperPipes = [
            {"x": self.window.width + 200, "y": newPipe1[0]["y"]},
            {
                "x": self.window.width + 200 + (self.window.width / 2),
                "y": newPipe2[0]["y"],
            },
        ]

        # list of lowerpipe
        lowerPipes = [
            {"x": self.window.width + 200, "y": newPipe1[1]["y"]},
            {
                "x": self.window.width + 200 + (self.window.width / 2),
                "y": newPipe2[1]["y"],
            },
        ]

        dt = self.clock.tick(self.fps) / 1000
        pipeVelX = -128 * dt

        # player velocity, max velocity, downward acceleration, acceleration on flap
        playerVelY = (
            -9
        )  # player's velocity along Y, default same as playerFlapped
        playerMaxVelY = 10  # max vel along Y, max descend speed
        # playerMinVelY = -8  # min vel along Y, max ascend speed
        playerAccY = 1  # players downward acceleration
        playerRot = 45  # player's rotation
        playerVelRot = 3  # angular speed
        playerRotThr = 20  # rotation threshold
        playerFlapAcc = -9  # players speed on flapping
        playerFlapped = False  # True when player flaps

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    pygame.quit()
                    sys.exit()
                if self.is_tap_event(event):
                    if player_y > -2 * self.images["player"][0].get_height():
                        playerVelY = playerFlapAcc
                        playerFlapped = True
                        self.sounds["wing"].play()

            # check for crash here
            crashTest = self.check_crash(
                {"x": player_x, "y": player_y, "index": playerIndex},
                upperPipes,
                lowerPipes,
            )
            if crashTest[0]:
                return {
                    "y": player_y,
                    "groundCrash": crashTest[1],
                    "base_x": base_x,
                    "upperPipes": upperPipes,
                    "lowerPipes": lowerPipes,
                    "score": score,
                    "playerVelY": playerVelY,
                    "playerRot": playerRot,
                }

            # check for score
            playerMidPos = player_x + self.images["player"][0].get_width() / 2
            for pipe in upperPipes:
                pipeMidPos = pipe["x"] + self.images["pipe"][0].get_width() / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    score += 1
                    self.sounds["point"].play()

            # playerIndex base_x change
            if (loopIter + 1) % 3 == 0:
                playerIndex = next(player_index_gen)
            loopIter = (loopIter + 1) % 30
            base_x = -((-base_x + 100) % baseShift)

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

            playerHeight = self.images["player"][playerIndex].get_height()
            player_y += min(playerVelY, self.base_y - player_y - playerHeight)

            # move pipes to left
            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                uPipe["x"] += pipeVelX
                lPipe["x"] += pipeVelX

            # add new pipe when first pipe is about to touch left of screen
            if 3 > len(upperPipes) > 0 and 0 < upperPipes[0]["x"] < 5:
                newPipe = self.get_random_pipe()
                upperPipes.append(newPipe[0])
                lowerPipes.append(newPipe[1])

            # remove first pipe if its out of the screen
            if (
                len(upperPipes) > 0
                and upperPipes[0]["x"] < -self.images["pipe"][0].get_width()
            ):
                upperPipes.pop(0)
                lowerPipes.pop(0)

            # draw sprites
            self.screen.blit(self.images["background"], (0, 0))

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                self.screen.blit(
                    self.images["pipe"][0], (uPipe["x"], uPipe["y"])
                )
                self.screen.blit(
                    self.images["pipe"][1], (lPipe["x"], lPipe["y"])
                )

            self.screen.blit(self.images["base"], (base_x, self.base_y))
            # print score so player overlaps the score
            self.show_score(score)

            # Player rotation has a threshold
            visibleRot = playerRotThr
            if playerRot <= playerRotThr:
                visibleRot = playerRot

            playerSurface = pygame.transform.rotate(
                self.images["player"][playerIndex], visibleRot
            )
            self.screen.blit(playerSurface, (player_x, player_y))

            pygame.display.update()
            await asyncio.sleep(0)
            self.clock.tick(self.fps)

    async def game_over(self, crashInfo):
        """crashes the player down and shows gameover image"""
        score = crashInfo["score"]
        playerx = self.window.width * 0.2
        player_y = crashInfo["y"]
        playerHeight = self.images["player"][0].get_height()
        playerVelY = crashInfo["playerVelY"]
        playerAccY = 2
        playerRot = crashInfo["playerRot"]
        playerVelRot = 7

        base_x = crashInfo["base_x"]

        upperPipes, lowerPipes = (
            crashInfo["upperPipes"],
            crashInfo["lowerPipes"],
        )

        # play hit and die sounds
        self.sounds["hit"].play()
        if not crashInfo["groundCrash"]:
            self.sounds["die"].play()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ):
                    pygame.quit()
                    sys.exit()
                if self.is_tap_event(event):
                    if player_y + playerHeight >= self.base_y - 1:
                        return

            # player y shift
            if player_y + playerHeight < self.base_y - 1:
                player_y += min(
                    playerVelY, self.base_y - player_y - playerHeight
                )

            # player velocity change
            if playerVelY < 15:
                playerVelY += playerAccY

            # rotate only when it's a pipe crash
            if not crashInfo["groundCrash"]:
                if playerRot > -90:
                    playerRot -= playerVelRot

            # draw sprites
            self.screen.blit(self.images["background"], (0, 0))

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                self.screen.blit(
                    self.images["pipe"][0], (uPipe["x"], uPipe["y"])
                )
                self.screen.blit(
                    self.images["pipe"][1], (lPipe["x"], lPipe["y"])
                )

            self.screen.blit(self.images["base"], (base_x, self.base_y))
            self.show_score(score)

            playerSurface = pygame.transform.rotate(
                self.images["player"][1], playerRot
            )
            self.screen.blit(playerSurface, (playerx, player_y))
            self.screen.blit(self.images["gameover"], (50, 180))

            self.clock.tick(self.fps)
            pygame.display.update()
            await asyncio.sleep(0)

    def get_random_pipe(self):
        """returns a randomly generated pipe"""
        # y of gap between upper and lower pipe
        gapY = random.randrange(0, int(self.base_y * 0.6 - self.pipe_gap))
        gapY += int(self.base_y * 0.2)
        pipeHeight = self.images["pipe"][0].get_height()
        pipeX = self.window.width + 10

        return [
            {"x": pipeX, "y": gapY - pipeHeight},  # upper pipe
            {"x": pipeX, "y": gapY + self.pipe_gap},  # lower pipe
        ]

    def show_score(self, score):
        """displays score in center of screen"""
        scoreDigits = [int(x) for x in list(str(score))]
        totalWidth = 0  # total width of all numbers to be printed

        for digit in scoreDigits:
            totalWidth += self.images["numbers"][digit].get_width()

        x_offset = (self.window.width - totalWidth) / 2

        for digit in scoreDigits:
            self.screen.blit(
                self.images["numbers"][digit],
                (x_offset, self.window.height * 0.1),
            )
            x_offset += self.images["numbers"][digit].get_width()

    def check_crash(self, player, upperPipes, lowerPipes):
        """returns True if player collides with base or pipes."""
        pi = player["index"]
        player["w"] = self.images["player"][0].get_width()
        player["h"] = self.images["player"][0].get_height()

        # if player crashes into ground
        if player["y"] + player["h"] >= self.base_y - 1:
            return [True, True]
        else:

            playerRect = pygame.Rect(
                player["x"], player["y"], player["w"], player["h"]
            )
            pipeW = self.images["pipe"][0].get_width()
            pipeH = self.images["pipe"][0].get_height()

            for uPipe, lPipe in zip(upperPipes, lowerPipes):
                # upper and lower pipe rects
                uPipeRect = pygame.Rect(uPipe["x"], uPipe["y"], pipeW, pipeH)
                lPipeRect = pygame.Rect(lPipe["x"], lPipe["y"], pipeW, pipeH)

                # player and upper/lower pipe hitmasks
                pHitMask = self.hit_masks["player"][pi]
                uHitmask = self.hit_masks["pipe"][0]
                lHitmask = self.hit_masks["pipe"][1]

                # if bird collided with upipe or lpipe
                uCollide = self.pixel_collision(
                    playerRect, uPipeRect, pHitMask, uHitmask
                )
                lCollide = self.pixel_collision(
                    playerRect, lPipeRect, pHitMask, lHitmask
                )

                if uCollide or lCollide:
                    return [True, False]

        return [False, False]

    def pixel_collision(self, rect1, rect2, hitmask1, hitmask2):
        """Checks if two objects collide and not just their rects"""
        rect = rect1.clip(rect2)

        if rect.width == 0 or rect.height == 0:
            return False

        x1, y1 = rect.x - rect1.x, rect.y - rect1.y
        x2, y2 = rect.x - rect2.x, rect.y - rect2.y

        for x in range(rect.width):
            for y in range(rect.height):
                if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                    return True
        return False


if __name__ == "__main__":
    asyncio.run(Flappy().start())
