import numpy as np
import pygame
from .flappy import *

import gymnasium as gym
from gymnasium.spaces import Discrete, Dict, Tuple, Box

class FlappyEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, rendermode=None, size=0):
        self.game = Flappy()
        self.height = self.game.config.window.height
        self.width = self.game.config.window.width
        
        # obs space is composed of agent height and position of the gap in the next 2 pipes
        self.observation_space = Dict(
            {
                "bird": Discrete(self.height),
                "pipes_y": Box(0, self.height, shape=(2,), dtype=int),
                "pipes_x": Box(0, self.width, shape=(2,), dtype=int),
            }
        )
        # 2 actions: 0 -> no action, 1 -> jump
        self.action_space = Discrete(2)

        assert rendermode is None or rendermode in self.metadata["render_modes"]
        self.render_mode = rendermode

    async def run(self):
        while True:
            self.game.reset()
            game_over = await self.step([])
            if game_over: break

        self.close()

    def _get_obs(self):
        pass

    async def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        self.game.reset()

    async def step(self, action):
        # action here
        return await self.game.tick()

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
            self.window = None  # type: ignore  # window is None after pygame.quit()
