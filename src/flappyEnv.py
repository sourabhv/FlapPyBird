import numpy as np
import pygame
from .flappy import *
import random as rnd

import gymnasium as gym
from gymnasium.spaces import Discrete, Dict, Tuple, Box

class FlappyEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 30}

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
                "pipes_h": Box(0, self.height, shape=(2,), dtype=int),
                "pipes_w": Box(0, self.width, shape=(2,), dtype=int)
            }
        )
        # 2 actions: 0 -> no action, 1 -> jump
        self.action_space = Discrete(2)

        assert rendermode is None or rendermode in self.metadata["render_modes"]
        self.render_mode = rendermode

    def _get_obs(self):
        bird_y = int(self.game.player.cy)
        bird_vel = int(self.game.player.vel_y)
        pipes = self.game.pipes.lower
        pipes_upper = self.game.pipes.upper
        pipes_y = []
        pipes_x = []
        pipes_h = []
        pipes_w = []

        if len(pipes) >= 2:
            pipes_y.append(int(pipes[-2].y))
            pipes_x.append(int(pipes[-2].x))
            pipes_h.append(int(pipes[-2].y - (pipes_upper[-2].y + pipes_upper[-2].h)))
            pipes_w.append(int(pipes[-2].w))

        pipes_y.append(int(pipes[-1].y))
        pipes_x.append(int(pipes[-1].x))
        pipes_h.append(int(pipes[-1].y - (pipes_upper[-1].y + pipes_upper[-1].h)))
        pipes_w.append(int(pipes[-1].w))

        return {"bird_y": bird_y, "bird_vel": bird_vel, "pipes_y": pipes_y, "pipes_x": pipes_x, "pipes_h": pipes_h, "pipes_w": pipes_w}
    
    def _get_info(self):
        return []
        

    async def reset(self, seed=5, options=None):
        # We need the following line to seed self.np_random
        # super().reset(seed=seed)
        # randomize starting height (20-70% of screen height from top)
        start_pos = (self.np_random.choice(51) + 20) / 100.0 
        rnd.seed(seed)
        self.game.reset(start_pos)

        obs = self._get_obs()
        info = self._get_info()

        return obs, info

    async def step(self, action):

        terminated = await self.game.tick(action == 1)
        obs = self._get_obs()
        info = self._get_info()
        reward = 1 if not terminated else 0

        # self.game._draw_observation_points(obs)
        return obs, reward, terminated, False, info

    def close(self):
        pygame.display.quit()
        pygame.quit()
