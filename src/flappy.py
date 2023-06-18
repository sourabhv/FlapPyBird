import asyncio
import sys

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT

from .sprites import (
    Background,
    Floor,
    GameOver,
    Pipes,
    Player,
    PlayerMode,
    Score,
    WelcomeMessage,
)
from .utils import HitMask, Images, Sounds, Window


class Flappy:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        self.window = Window(288, 512)
        self.fps = 30
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.window.width, self.window.height)
        )
        self.images = Images()
        self.sounds = Sounds()
        self.hit_mask = HitMask(self.images)

        self.sprite_args = (
            self.screen,
            self.clock,
            self.fps,
            self.window,
            self.images,
            self.sounds,
            self.hit_mask,
        )

    async def start(self):
        while True:
            self.background = Background(*self.sprite_args)
            self.floor = Floor(*self.sprite_args)
            self.player = Player(*self.sprite_args)
            self.welcome_message = WelcomeMessage(*self.sprite_args)
            self.game_over_message = GameOver(*self.sprite_args)
            self.pipes = Pipes(*self.sprite_args)
            self.score = Score(*self.sprite_args)
            await self.splash()
            await self.play()
            await self.game_over()

    async def splash(self):
        """Shows welcome splash screen animation of flappy bird"""

        self.player.set_mode(PlayerMode.SHM)

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    return

            self.background.tick()
            self.floor.tick()
            self.player.tick()
            self.welcome_message.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.clock.tick(self.fps)

    def check_quit_event(self, event):
        if event.type == QUIT or (
            event.type == KEYDOWN and event.key == K_ESCAPE
        ):
            pygame.quit()
            sys.exit()

    def is_tap_event(self, event):
        m_left, _, _ = pygame.mouse.get_pressed()
        space_or_up = event.type == KEYDOWN and (
            event.key == K_SPACE or event.key == K_UP
        )
        screen_tap = event.type == pygame.FINGERDOWN
        return m_left or space_or_up or screen_tap

    async def play(self):
        self.score.reset()
        self.player.set_mode(PlayerMode.NORMAL)

        while True:

            if self.player.collided(self.pipes, self.floor):
                return

            for pipe in self.pipes.upper:
                if self.player.crossed(pipe):
                    self.score.add()

            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    if self.player.y > -2 * self.images.player[0].get_height():
                        self.player.flap()

            # draw sprites
            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.clock.tick(self.fps)

    async def game_over(self):
        """crashes the player down and shows gameover image"""

        self.player.set_mode(PlayerMode.CRASH)
        self.pipes.stop()
        self.floor.stop()

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    if self.player.y + self.player.height >= self.floor.y - 1:
                        return

            # draw sprites
            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()
            self.game_over_message.tick()
            # self.screen.blit(self.images.gameover, (50, 180))

            self.clock.tick(self.fps)
            pygame.display.update()
            await asyncio.sleep(0)
