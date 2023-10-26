import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces


class FlappyEnv(gym.Env):
    metadata = {}

    def __init__(self, rendermode=None, size=0):
        pass

    def _get_obs(self):
        pass

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        pass

    def step(self, action):
        pass

    def render(self):
        pass

    def close(self):
        pass

