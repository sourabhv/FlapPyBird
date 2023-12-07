import numpy as np
import random
class LinearQAgent:
    def __init__(self, num_features, learning_rate=0.01, gamma=0.99, epsilon=0.1):
        self.theta = np.random.randn(num_features) * 0.01
        self.alpha = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon

    def extract_features(self, state, action):
        # Assuming state is a dictionary with keys like 'bird_y', 'bird_vel', 'pipe1_x', 'pipe1_y', etc.

        bird_y = state['bird_y']
        bird_vel = state['bird_vel']
        pipe1_x = state['pipe1_x']
        pipe1_y = state['pipe1_y']
        pipe2_x = state['pipe2_x'] if 'pipe2_x' in state else None
        pipe2_y = state['pipe2_y'] if 'pipe2_y' in state else None

        # Normalize features
        height = self.height  # Assuming self.height is the height of the game window
        width = self.width  # Assuming self.width is the width of the game window

        # Feature 1: Normalized bird's vertical position
        f1 = bird_y / height

        # Feature 2: Bird's vertical velocity
        f2 = bird_vel / 10  # Assuming max velocity is around 10

        # Feature 3: Normalized horizontal distance to next pipe
        f3 = pipe1_x / width if pipe1_x is not None else 0

        # Feature 4: Normalized vertical distance to gap in next pipe
        # Assuming the gap is centered around pipe1_y
        f4 = abs(bird_y - pipe1_y) / height if pipe1_y is not None else 0

        # Optionally, you can add more features, such as distance to the second pipe, action, etc.

        return np.array([f1, f2, f3, f4])

    def q_value(self, state, action):
        features = self.extract_features(state, action)
        return np.dot(self.theta, features)

    def choose_action(self, state):
        # Implement epsilon-greedy policy
        if random.random() < self.epsilon:
            # Exploration: choose a random action
            return random.choice([0, 1])  # Assuming actions are 0 (no flap) and 1 (flap)
        else:
            # Exploitation: choose the best action based on the current Q-values
            q_values = [self.q_value(state, action) for action in [0, 1]]
            return np.argmax(q_values)  # Returns the action with the highest Q-value

    def update(self, state, action, reward, next_state, done):
        features = self.extract_features(state, action)
        q_target = reward
        if not done:
            q_target += self.gamma * max(self.q_value(next_state, a) for a in possible_actions)
        q_current = self.q_value(state, action)
        error = q_target - q_current
        self.theta += self.alpha * error * features
