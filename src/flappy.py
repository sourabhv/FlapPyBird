import asyncio
import sys

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT

from .entities import (
    Background,
    Floor,
    GameOver,
    Pipes,
    Player,
    PlayerMode,
    Score,
    WelcomeMessage,
)
from .utils import GameConfig, Images, Sounds, Window


class Flappy:
    def __init__(self, speed):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        window = Window(288, 512)
        screen = pygame.display.set_mode((window.width, window.height))
        images = Images()

        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=speed,
            window=window,
            images=images,
            sounds=Sounds(),
        )

    def reset(self, start_pos):
        self.background = Background(self.config)
        self.floor = Floor(self.config)
        self.player = Player(self.config, start_pos)
        self.welcome_message = WelcomeMessage(self.config)
        self.game_over_message = GameOver(self.config)
        self.pipes = Pipes(self.config)
        self.score = Score(self.config)
        self.score.reset()
        self.player.set_mode(PlayerMode.NORMAL)
        
    def tick(self, flap_this_frame):

        # player input
        for event in pygame.event.get():
            if self.is_tap_event(event):
                flap_this_frame = True

            self.check_quit_event(event)

        if self.player.collided(self.pipes, self.floor):
            return True

        for i, pipe in enumerate(self.pipes.upper):
            if self.player.crossed(pipe):
                #print("We added")
                self.score.add()
                
        self.score.add()

        if flap_this_frame:
            self.player.flap()

        self.background.tick()
        self.floor.tick()
        self.pipes.tick()
        self.score.tick()
        self.player.tick()

        pygame.display.update()
        # await asyncio.sleep(0)
        self.config.tick()
        return False
    
    def is_tap_event(self, event):
        m_left, _, _ = pygame.mouse.get_pressed()
        space_or_up = event.type == KEYDOWN and (
            event.key == K_SPACE or event.key == K_UP
        )
        screen_tap = event.type == pygame.FINGERDOWN
        return m_left or space_or_up or screen_tap
    
    def check_quit_event(self, event):
        if event.type == QUIT or (
            event.type == KEYDOWN and event.key == K_ESCAPE
        ):
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    def _draw_observation_points(self, ob):
        for i in range(len(ob["pipes_x"])):
            # bottom pipe, top left corner
            pygame.draw.circle(self.config.screen, (255,0,0), (ob["pipes_x"][i], ob["pipes_y"][i]), 15)
            # top pipe, bottom left corner
            pygame.draw.circle(self.config.screen, (0,0,255), (ob["pipes_x"][i], ob["pipes_y"][i] - ob["pipes_h"][i]), 15)
            # bottom pipe, top right corner
            pygame.draw.circle(self.config.screen, (0,255,0), (ob["pipes_x"][i] + ob["pipes_w"][i], ob["pipes_y"][i]), 15)
        pygame.display.update()
