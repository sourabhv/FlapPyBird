import numpy as np
import pygame
from .flappy import *
import random as rnd

import gymnasium as gym
from gymnasium.spaces import Discrete, Dict, Tuple, Box

SPACE_DIVISOR = 50

class FlappyEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 3000}

    def __init__(self, rendermode=None, size=0):
        self.game = Flappy(self.metadata["render_fps"])
        self.height = int(self.game.config.window.viewport_height)
        self.width = 627 # int(self.game.config.window.viewport_width)
        
        # obs space is composed of agent height and position of the gap in the next 2 pipes
        self.observation_space = Dict(
            {
                "bird_y": Discrete(int(self.height / SPACE_DIVISOR)),
                "bird_vel": Discrete(20),
                "pipe1_y": Discrete(int(self.height / SPACE_DIVISOR)),
                "pipe1_x": Discrete(int(self.width / SPACE_DIVISOR)),
                "pipe2_y": Discrete(int(self.height / SPACE_DIVISOR)),
                "pipe2_x": Discrete(int(self.width / SPACE_DIVISOR))
                # "pipes_h": Box(0, self.height, shape=(2,), dtype=int),
                # "pipes_w": Box(0, self.width, shape=(2,), dtype=int)
            }
        )
        # 2 actions: 0 -> no action, 1 -> jump
        self.action_space = Discrete(2)

        assert rendermode is None or rendermode in self.metadata["render_modes"]
        self.render_mode = rendermode

    @property
    def get_state_shape(self):        
        return (int(404 / SPACE_DIVISOR)+1,
                20,
                int(404 / SPACE_DIVISOR)+1,
                int(627 / SPACE_DIVISOR)+1,
                int(404 / SPACE_DIVISOR)+1,                
                int(627 / SPACE_DIVISOR)+1                
        )
    
    @property
    def n_actions(self):
        return 2

    def _get_obs(self):
        bird_y = int(self.game.player.cy / SPACE_DIVISOR)
        bird_vel = int(self.game.player.vel_y) + 9
        pipes = self.game.pipes.lower
        pipes_upper = self.game.pipes.upper
        pipe1_y = pipe1_x = pipe2_y = pipe2_x = pipe_h = pipe_w = 0        

        pipe1_y = int(pipes[0].y / SPACE_DIVISOR)
        pipe1_x = int(pipes[0].x / SPACE_DIVISOR)
        # print(f"pipe1_y: {pipe1_y} || pipe1_x: {pipe1_x}")

        if len(pipes) >= 2:
            pipe2_y = int(pipes[1].y / SPACE_DIVISOR)
            pipe2_x = int(pipes[1].x / SPACE_DIVISOR)
            # print(f"pipe2_y: {pipe2_y} || pipe2_x: {pipe2_x}")

        pipe_h = int(pipes[0].y - (pipes_upper[0].y + pipes_upper[0].h))
        pipe_w = int(pipes[0].w)

        return {"bird_y": bird_y, "bird_vel": bird_vel, "pipe1_y": pipe1_y, "pipe1_x": pipe1_x, "pipe2_y": pipe2_y, "pipe2_x": pipe2_x} # , "pipes_h": pipes_h, "pipes_w": pipes_w}
    
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
        reward = 0 if not terminated else -1000

        # self.game._draw_observation_points(obs)
        return obs, reward, terminated, False, info

    def close(self):
        pygame.display.quit()
        pygame.quit()
