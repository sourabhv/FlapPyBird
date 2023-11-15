import numpy as np
import pygame
from .flappy import *
import random as rnd

import gymnasium as gym
from gymnasium.spaces import Discrete, Dict, Tuple, Box

class FlappyEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 30}
    episode = 1

    def __init__(self, rendermode=None, size=0):
        self.game = Flappy()
        self.height = int(self.game.config.window.viewport_height)
        self.width = int(self.game.config.window.viewport_width)
        
        # obs space is composed of agent height and position of the gap in the next 2 pipes
        self.observation_space = Dict(
            {
                "bird_y": Discrete(self.height),
                "bird_vel": Discrete(20, start=-9),
                "pipes_y": Box(0, self.height, shape=(2,), dtype=int),
                "pipes_x": Box(0, self.width, shape=(2,), dtype=int),
            }
        )
        # 2 actions: 0 -> no action, 1 -> jump
        self.action_space = Discrete(2)

        assert rendermode is None or rendermode in self.metadata["render_modes"]
        self.render_mode = rendermode

    async def run(self):
        for _ in range(10):
            await self.reset()
            total_reward = 0
            while True:
                action = 1 if rnd.randint(0,10) == 0 else 0
                obs, reward, game_over, _, info = await self.step(action)
                total_reward += reward
                # print(obs)
                if game_over:
                    self.print_episode_data(obs, total_reward)
                    self.episode += 1
                    break           
        self.close()   

    def print_episode_data(self, obs, total_reward):
        print("--------------")
        print(f"Episode: {self.episode}")
        print(obs)
        print(f"Score: {total_reward}")

    def _get_obs(self):
        bird_y = int(self.game.player.cy)
        bird_vel = int(self.game.player.vel_y)
        pipes = self.game.pipes.lower
        pipes_y = []
        pipes_x = []

        if len(pipes) >= 2:
            pipes_y.append(int(pipes[-2].y))
            pipes_x.append(int(pipes[-2].cx))

        pipes_y.append(int(pipes[-1].y))
        pipes_x.append(int(pipes[-1].cx))

        return {"bird_y": bird_y, "bird_vel": bird_vel, "pipes_y": pipes_y, "pipes_x": pipes_x}
        

    async def reset(self, seed=5, options=None):
        # We need the following line to seed self.np_random
        # super().reset(seed=seed)
        # randomize starting height (20-70% of screen height from top)
        start_pos = (self.np_random.choice(51) + 20) / 100.0 
        print(start_pos)
        rnd.seed(seed)
        self.game.reset(start_pos)

        obs = self._get_obs()
        info = [] # TODO: define auxiliary info if needed

        return obs, info

    async def step(self, action):
        
        for event in pygame.event.get():
            # player input
            if self.is_tap_event(event):
                self.game.flap_this_frame = True

            self.check_quit_event(event)

        # random space
        if action:
            self.game.flap_this_frame = True

        terminated = await self.game.tick()
        obs = self._get_obs()
        info = [] # TODO: define auxiliary info if needed
        reward = 1 if not terminated else 0

        return obs, reward, terminated, False, info

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

    def close(self):
        pygame.display.quit()
        pygame.quit()
