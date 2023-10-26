import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces

import flappy

class FlappyEnv(gym.Env):
    metadata = {}

    def __init__(self, rendermode=None, size=0):
        pass

    def _get_obs(self):
        pass
    
    async def reset(self):
        self.player.set_mode(flappy.PlayerMode.CRASH)
        self.pipes.stop()
        self.floor.stop()