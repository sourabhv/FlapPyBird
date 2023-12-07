import asyncio
import random
import gymnasium as gym
from gymnasium.spaces import Discrete, Dict
from src.flappy import Flappy

import numpy as np
from scipy.spatial.distance import cdist

# RBF Featurizer
class RbfFeaturizer:
    def __init__(self, env, n_features=100, n_actions=2):
        centers = np.array([self._flatten_state(env.observation_space.sample()) for _ in range(n_features)])
        self._mean = np.mean(centers, axis=0, keepdims=True)
        self._std = np.std(centers, axis=0, keepdims=True)
        self._centers = (centers - self._mean) / self._std
        self.n_features = n_features
        self.n_actions = n_actions
        self.theta = np.zeros((n_features, n_actions)) 
        self.possible_actions = [0, 1]
    def featurize(self, state):
        state = self._flatten_state(state)
        z = (state - self._mean) / self._std
        z = np.reshape(z, (1, -1))
        dist = cdist(z, self._centers)
        return np.exp(-dist ** 2).flatten()


    def _flatten_state(self, state):
       
        bird_y, bird_vel, pipe1_y, pipe1_x, pipe2_y, pipe2_x = state
        vertical_distance = pipe1_y - bird_y
        horizontal_distance = pipe1_x
        if pipe1_x < 0:  # Switch to second pipe when the first pipe is passed
            vertical_distance = pipe2_y - bird_y
            horizontal_distance = pipe2_x
        else:
            vertical_distance = pipe1_y - bird_y
            horizontal_distance = pipe1_x
            
        return np.array([vertical_distance, horizontal_distance, bird_vel])
    


    
    def q_value(self, features, action):
        return np.dot(features, self.theta[:, action])


    def choose_action(self, features):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.possible_actions)
        else:
            q_values = [self.q_value(features, action) for action in self.possible_actions]
            return np.argmax(q_values)

    def update(self, features, action, reward, next_features, done):
        q_target = reward
        if not done:
            q_target += self.gamma * max(self.q_value(next_features, a) for a in self.possible_actions)
        q_current = self.q_value(features, action)
        error = q_target - q_current
        self.theta[:, action] += self.alpha * error * features  

        new_q_value = self.q_value(features, action)
        print(f"Updated Q-value for action {action}: {new_q_value}")


