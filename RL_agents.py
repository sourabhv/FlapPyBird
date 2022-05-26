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

        self._Q_actions_list = ["flap", ""]
        self._Q_states_list = [0]  # init with dummy value
        self._Q_table = np.array([[0 for _ in range(len(self._Q_actions_list) + 1)]])  # init with dummy value (so that .vstack works)

    def _speed_mapping(self, speed):
        return int(speed)

    def _x_distance_mapping(self, distance):
        if abs(distance) <= 50:
            return int((distance // 2) * 2)
        elif abs(distance) <= 170:
            return int((distance // 10) * 10)
        else:
            return int((distance // 500) * 500)

    def _y_distance_mapping(self, distance):
        if abs(distance) <= 50:
            return int((distance // 5) * 5)
        elif abs(distance) <= 100:
            return int((distance // 10) * 10)
        else:
            return int((distance // 500) * 500)

    def update_state(self, player_pos, player_vel, lower_pipes):

        next_pipe = 0 if player_pos["x"] <= (lower_pipes[0]["x"] + 50) else 1

        x_dist = lower_pipes[next_pipe]["x"] - player_pos["x"]
        y0_dist = lower_pipes[next_pipe]["y"] - player_pos["y"]

        if -50 < x_dist <= 0:
            y1_dist = lower_pipes[next_pipe + 1]["y"] - player_pos["y"]
        else:
            y1_dist = 0

        x_dist = self._x_distance_mapping(x_dist)
        y0_dist = self._y_distance_mapping(y0_dist)
        y1_dist = self._y_distance_mapping(y1_dist)
        player_vel = self._speed_mapping(player_vel)

        state = [x_dist, y0_dist, y1_dist, player_vel]

        if state not in self._Q_states_list:
            # new state
            # print(f"Encountered new state: {state}")
            self._Q_states_list.append(state)
            new_state_Q_values = np.random.uniform(size=len(self._Q_actions_list) + 1)
            new_state_Q_values[len(self._Q_actions_list)] = 1  # last element is the state count
            self._Q_table = np.vstack([self._Q_table, new_state_Q_values])
        else:
            # known state encountered again
            self._Q_table[self._Q_states_list.index(state), len(self._Q_actions_list)] += 1

        # print(f"player_vel: {player_vel}, dist to upper: {dist_upp}, dist to lower: {dist_low}")
        self.prev_state = self.curr_state
        self.curr_state = state
        return self.curr_state

    def choose_action(self, state) -> str:
        if np.random.uniform() < self.epsilon:
            self.action = self._Q_actions_list[np.random.randint(len(self._Q_actions_list))]
            # print(f"Randomly chose to... {self.action}")
        else:
            self.action = self._Q_actions_list[np.argmax(self._Q_table[self._Q_states_list.index(state), :len(self._Q_actions_list)])]
            # print(f"Based on optimality chose to... {self.action}")
        return self.action

    def update_Q(self, reward):
        new_value = self._get_Q(self.prev_state, self.action) + self.alpha * \
            (reward + self.gamma * self._get_Q_optimal_action(self.curr_state) - self._get_Q(self.prev_state, self.action))

        self._set_Q(self.prev_state, self.action, new_value)
        # print(f"Updating Q value of {self.prev_state, self.action} to {new_value}")

    def _get_Q(self, state, action):
        # print(f"state {state}, action {action}")
        if state in self._Q_states_list:
            return self._Q_table[self._Q_states_list.index(state), self._Q_actions_list.index(action)]
        else:
            print(f"_get_Q - state {state}, action {action}")
            self._Q_states_list.append(state)
            self._Q_table = np.vstack([self._Q_table, np.random.normal(size=2)])
            return self._get_Q(state=state, action=action)

    def _set_Q(self, state, action, value):
        # print(f"state {state}, action {action}, value {value}")
        if state in self._Q_states_list:
            self._Q_table[self._Q_states_list.index(state), self._Q_actions_list.index(action)] = value
        else:
            print(f"_set_Q - state {state}, action {action}, value {value}")
            self._Q_states_list.append(state)
            self._Q_table = np.vstack([self._Q_table, np.random.normal(size=2)])
            self._set_Q(state=state, action=action, value=value)

    def _get_Q_optimal_action(self, state):
        # print(f"state {state}")
        if state in self._Q_states_list:
            return np.max(self._Q_table[self._Q_states_list.index(state), :len(self._Q_actions_list)])
        else:
            print(f"_get_Q_optimal_action - state {state}")
            self._Q_states_list.append(state)
            self._Q_table = np.vstack([self._Q_table, np.random.normal(size=2)])
            return self._get_Q_optimal_action(state=state)
