import asyncio
import sys

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT

from .ai.game_observation import GameObservation
from .ai.genetic_algorithm import GeneticAlgorithm
from .ai.model import GameAction, Model
from .ai.bird import Bird
from .ai.entities import (
    Background,
    Floor,
    GameOver,
    Pipes,
    PlayerMode,
    Score,
    WelcomeMessage,
)
from ai.utils import GameConfig, Images, Sounds, Window


class Flappy:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        window = Window(288, 512)
        screen = pygame.display.set_mode((window.width, window.height))
        images = Images()

        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=30,
            window=window,
            images=images,
            sounds=Sounds(),
        )

        self.human_player = (
            False if len(sys.argv) > 1 and sys.argv[1] == "ai" else True
        )
        if not self.human_player:
            self.ga = GeneticAlgorithm()
            self.ga.set_population([Bird(self.config) for _ in range(10)])
            self.model_results = []

    async def start(self):
        while True:
            self.background = Background(self.config)
            self.floor = Floor(self.config)
            self.player = Bird(self.config)
            self.population = self.ga.get_population()
            self.death_population = []
            
            self.welcome_message = WelcomeMessage(self.config)
            self.game_over_message = GameOver(self.config)
            self.pipes = Pipes(self.config)
            self.score = Score(self.config)

            if not self.human_player:
                print("Starting in AI mode")
                await self.agent_play()
                await self.game_over()
            else:
                await self.splash()
                await self.play()
                await self.game_over()

    async def agent_play(self):
        # self.score.reset()
        for bird in self.population:
            bird.set_mode(PlayerMode.NORMAL)
            bird.start_flying()

        while True:
            for bird in self.population:
            
                # the observation we will pass to the AI agent
                observation = GameObservation(
                    bird_y_pos=bird.y,
                    y_dist_to_bot_pipe=self.pipes.upper[0].y - bird.y,
                    y_dist_to_top_pipe=self.pipes.lower[0].y - bird.y,
                    x_dist_to_pipe_pair=self.pipes.upper[0].x - bird.x,
                    bird_y_vel=bird.vel_y,
                )

                # Get agent decision
                action = bird.model.predict(observation)

                # Perform action
                if action == GameAction.JUMP and len(pygame.event.get()) == 0:
                    jump_event = pygame.event.Event(
                        pygame.KEYDOWN, {"key": pygame.K_SPACE}
                    )
                    pygame.event.post(jump_event)
                elif (
                    action == GameAction.DO_NOTHING and len(pygame.event.get()) > 0
                ):
                    pygame.event.clear()

                if bird.collided(self.pipes, self.floor):
                    bird.stop_flying()
                    # Remove bird from population
                    self.population.remove(bird)
                    self.death_population.append(bird)
                    
                    # If all birds are dead, restart the game
                    if len(self.population) == 0:
                        return

                for i, pipe in enumerate(self.pipes.upper):
                    if bird.crossed(pipe):
                        bird.score.add()
                        self.score.add()

                for event in pygame.event.get():
                    self.check_quit_event(event)
                    if self.is_tap_event(event):
                        bird.flap()

                self.background.tick()
                self.floor.tick()
                self.pipes.tick()
                self.score.tick()
                for bird in self.population:
                    bird.tick()

                pygame.display.update()
                await asyncio.sleep(0)
                self.config.tick()

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
            self.config.tick()

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

            for i, pipe in enumerate(self.pipes.upper):
                if self.player.crossed(pipe):
                    self.score.add()

            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    self.player.flap()

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def game_over(self):
        """crashes the player down and shows gameover image"""

        self.player.set_mode(PlayerMode.CRASH)
        self.pipes.stop()
        self.floor.stop()

        if self.human_player:
            while True:
                for event in pygame.event.get():
                    self.check_quit_event(event)
                    if self.is_tap_event(event):
                        if self.player.y + self.player.h >= self.floor.y - 1:
                            return

                self.background.tick()
                self.floor.tick()
                self.pipes.tick()
                self.score.tick()
                self.player.tick()
                self.game_over_message.tick()

                self.config.tick()
                pygame.display.update()
                await asyncio.sleep(0)
        else:
            # AI player
            print("AI agent lost. Restarting...")
            
            self.ga.set_population(self.death_population)
            self.ga.get_new_generation()
            
            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            for bird in self.population:
                bird.tick()
            self.game_over_message.tick()

            self.config.tick()
            pygame.display.update()
            await asyncio.sleep(1)
