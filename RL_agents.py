import numpy as np


class Flappy_QAgent:

    def __init__(self, alpha=0.7, gamma=1, epsilon=0.15) -> None:
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        # Dynamic variables
        self.best_score = 0
        self.epsisode_age = 0

        self.action = ""
        self.curr_state = [10, 10, 0]

        self._Q_actions_list = ["", "flap"]
        self._Q_states_list = [0]  # init with dummy value
        self._Q_table = np.array([[0 for _ in range(len(self._Q_actions_list))]])  # init with dummy value (so that .vstack works)

    def _speed_mapping(self, speed):
        return int(speed - speed % 2)

    def _x_distance_mapping(self, distance):
        if abs(distance) <= 50:
            return int(distance - distance % 10)
        elif abs(distance) <= 150:
            return int(distance - distance % 25)
        else:
            return int(distance - distance % 100)

    def _y_distance_mapping(self, distance):
        if abs(distance) <= 50:
            return int(distance - distance % 10)
        elif abs(distance) <= 100:
            return int(distance - distance % 25)
        else:
            return int(distance - distance % 500)

    def update_state(self, player_pos, player_vel, lower_pipes):

        # next_pipe = 0 if player_pos["x"] <= (lower_pipes[0]["x"] + 50) else 1

        # x_dist = lower_pipes[next_pipe]["x"] - player_pos["x"]
        # y0_dist = lower_pipes[next_pipe]["y"] - player_pos["y"]

        # if x_dist < 50:
        #     y1_dist = lower_pipes[next_pipe + 1]["y"] - player_pos["y"]
        # else:
        #     y1_dist = 1000

        # x_dist = self._x_distance_mapping(x_dist)
        # y0_dist = self._y_distance_mapping(y0_dist)
        # y1_dist = self._y_distance_mapping(y1_dist)
        # player_vel = self._speed_mapping(player_vel)

        # Get pipe coordinates
        pipe0, pipe1 = lower_pipes[0], lower_pipes[1]
        if player_pos["x"] - lower_pipes[0]["x"] >= 50:
            pipe0 = lower_pipes[1]
            if len(lower_pipes) > 2:
                pipe1 = lower_pipes[2]

        x0 = pipe0["x"] - player_pos["x"]
        y0 = pipe0["y"] - player_pos["y"]
        if -50 < x0 <= 0:
            y1 = pipe1["y"] - player_pos["y"]
        else:
            y1 = 0

        # Evaluate player position compared to pipe
        if x0 < -40:
            x0 = int(x0)
        elif x0 < 140:
            x0 = int(x0) - (int(x0) % 10)
        else:
            x0 = int(x0) - (int(x0) % 70)

        if -180 < y0 < 180:
            y0 = int(y0) - (int(y0) % 10)
        else:
            y0 = int(y0) - (int(y0) % 60)

        if -180 < y1 < 180:
            y1 = int(y1) - (int(y1) % 10)
        else:
            y1 = int(y1) - (int(y1) % 60)

        state = [x0, y0, y1, player_vel]

        if state not in self._Q_states_list:
            # new state
            # print(f"Encountered new state: {state}")
            self._Q_states_list.append(state)
            self._Q_table = np.vstack([self._Q_table, np.random.uniform(size=len(self._Q_actions_list))])

        # print(f"player_vel: {player_vel}, dist to upper: {dist_upp}, dist to lower: {dist_low}")
        self.prev_state = self.curr_state
        self.curr_state = state
        return self.curr_state

    def choose_action(self, state) -> str:
        if np.random.uniform() < self.epsilon:
            self.action = self._Q_actions_list[np.random.randint(len(self._Q_actions_list))]
            # print(f"Randomly chose to... {self.action}")
        else:
            self.action = self._Q_actions_list[np.argmax(self._Q_table[self._Q_states_list.index(state)])]
            # print(f"Based on optimality chose to... {self.action}")
        return self.action

    def update_Q(self, reward):
        new_value = self._get_Q(self.prev_state, self.action) + self.alpha * \
            (reward + self.gamma * self._get_Q_optimal_action(self.curr_state) - self._get_Q(self.prev_state, self.action))

        self._set_Q(self.prev_state, self.action, new_value)
        # print(f"Updating Q value of {self.prev_state, self.action} to {new_value}")

    def _get_Q(self, state, action):
        # print(f"state {state}, action {action}")
        return self._Q_table[self._Q_states_list.index(state), self._Q_actions_list.index(action)]

    def _set_Q(self, state, action, value):
        # print(f"state {state}, action {action}, value {value}")
        self._Q_table[self._Q_states_list.index(state), self._Q_actions_list.index(action)] = value

    def _get_Q_optimal_action(self, state):
        # print(f"state {state}")
        return np.max(self._Q_table[self._Q_states_list.index(state)])
