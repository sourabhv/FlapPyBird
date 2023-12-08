import numpy as np
import pygame
from .flappy import *
import random as rnd

import gymnasium as gym
from gymnasium.spaces import Discrete, Box

class FlappyEnv2(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, rendermode=None, size=0):

        # action_interval=5
        # self.action_interval = action_interval  # Number of frames to wait before deciding on a new action
        # self.frames_since_last_action = 0
        
        self.game = Flappy(self.metadata["render_fps"])
        self.height = int(self.game.config.window.viewport_height)
        print(self.height)
        self.width = 627 # int(self.game.config.window.viewport_width)
        self.pipe_count = 0
        #self.pipe_speed = 5 * self.metadata["render_fps"]
        
        # obs space is composed of bird_y, bird_vel, pipe1_y, pipe1_x, pipe2_y, pipe2_x
        self.observation_space = Box(
            low=0,
            high=np.array([self.height, 20, self.height, self.width, self.height, self.width]),
            shape=(6,),
            dtype=np.int32
        )
        
        # 2 actions: 0 -> no action, 1 -> jump
        self.action_space = Discrete(2)

        assert rendermode is None or rendermode in self.metadata["render_modes"]
        self.render_mode = rendermode

    @property
    def get_state_shape(self):        
        return (404+1,
                20,
                404+1,
                627+1,
                404+1,                
                627+1                
        )
    
    @property
    def n_actions(self):
        return 2

    def _get_obs(self):
        bird_y = min(int(self.game.player.cy), self.height)
        bird_vel = int(self.game.player.vel_y) + 9
        pipes = self.game.pipes.lower
        pipes_upper = self.game.pipes.upper
        pipe1_y = pipe1_x = pipe2_y = pipe2_x = pipe_h = pipe_w = 0        

        pipe1_y = int(pipes[0].y)
        pipe1_x = int(pipes[0].x)
        # print(f"pipe1_y: {pipe1_y} || pipe1_x: {pipe1_x}")

        if len(pipes) >= 2:
            pipe2_y = int(pipes[1].y)
            pipe2_x = int(pipes[1].x)
            # print(f"pipe2_y: {pipe2_y} || pipe2_x: {pipe2_x}")

        pipe_h = int(pipes[0].y - (pipes_upper[0].y + pipes_upper[0].h))
        pipe_w = int(pipes[0].w)
        
        #pipe_speed = 5 * self.metadata["render_fps"]

        return np.array([bird_y, bird_vel, pipe1_y, pipe1_x, pipe2_y, pipe2_x]) # , pipes_h, pipes_w])
    
    def _get_info(self):
        return []
        

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)
        # randomize starting height (20-70% of screen height from top)
        start_pos = (self.np_random.choice(51) + 20) / 100.0 
        rnd.seed(seed)
        self.game.reset(start_pos)
        self.pipe_count = 0

        obs = self._get_obs()
        info = self._get_info()

        return obs, info

    def step(self, action):

        # self.frames_since_last_action += 1

        terminated = self.game.tick(action == 1)
        obs = self._get_obs()
        info = self._get_info()
        
        reward = 1
        if self.game.player.collided_pipe(self.game.pipes):
            reward -= 10 
        if self.game.player.collided_floor(self.game.floor):
            reward -= 10
        if self.game.player.cy <= 0:
             reward -= 5
        for i, pipe in enumerate(self.game.pipes.upper):
            if self.game.player.crossed(pipe):
                reward += 50  # Reward for passing a pipe
                self.pipe_count += 1
                print(f"Passed pipe: {self.pipe_count}")

        # self.game._draw_observation_points(obs)
        return obs, reward, terminated, False, info

    def close(self):
        pygame.display.quit()
        pygame.quit()
