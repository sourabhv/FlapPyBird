import numpy as np


class Flappy_QAgent:

    def __init__(self, alpha_start=0.7, alpha_end=0.1, alpha_decay_episodes=20000, gamma=1, epsilon=0.1) -> None:
        self.alpha_start = alpha_start
        self.alpha_end = alpha_end
        self.alpha_decay_episodes = alpha_decay_episodes
        self.gamma = gamma
        self.epsilon = epsilon

        # Dynamic variables
        self.best_score = 0
        self.epsisode_age = 0

        self.action = ""
        self.curr_state = ""

        self._Q_actions_list = ["", "flap"]
        self._Q_table = {}

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

        x_dist_to_first = int(player_pos["x"] - lower_pipes[0]["x"])

        next_pipe = 1 if (x_dist_to_first > 80) else 0
        after_next_pipe = min(next_pipe + 1, len(lower_pipes) - 1)

        x_dist_to_next = int(player_pos["x"] - lower_pipes[next_pipe]["x"])
        y_dist_to_next = int(player_pos["y"] - lower_pipes[next_pipe]["y"])
        if x_dist_to_next < 10:
            y_dist_to_after_next = 1000
        else:
            y_dist_to_after_next = int(player_pos["y"] - lower_pipes[after_next_pipe]["y"])

        # reduce the state space by reducing the distance to multiples
        if x_dist_to_next < -85:
            x_dist_to_next = -85
        elif x_dist_to_next < -30:
            x_dist_to_next = int(x_dist_to_next - x_dist_to_next % 15)
        else:
            x_dist_to_next = int(x_dist_to_next - x_dist_to_next % 5)

        if y_dist_to_next < -150:
            y_dist_to_next = -150
        elif y_dist_to_next < 50:
            y_dist_to_next = int(y_dist_to_next - y_dist_to_next % 20)
        else:
            y_dist_to_next = 50

        if y_dist_to_after_next < -400:
            y_dist_to_after_next = -400
        elif y_dist_to_after_next < 400:
            y_dist_to_after_next = int(y_dist_to_after_next - y_dist_to_after_next % 20)
        else:
            y_dist_to_after_next = 1000

        player_vel = int(player_vel - player_vel % 3)

        state = f"{x_dist_to_next}_{y_dist_to_next}_{y_dist_to_after_next}_{player_vel}"
        # print(state)

        if state not in self._Q_table.keys():
            # print(f"Encountered new state: {state}")
            self._Q_table[state] = np.zeros(len(self._Q_actions_list))

        self.prev_state = self.curr_state
        self.curr_state = state
        # print(f"Player current state: {self.curr_state} \t| previous state : {self.prev_state}")
        return self.curr_state

    def choose_action(self, state) -> str:
        if np.random.uniform() < self.epsilon:
            self.action = self._Q_actions_list[np.random.randint(len(self._Q_actions_list))]
            # print(f"Randomly (with epsilon {self.epsilon}) chose to... {self.action}")
        else:
            self.action = self._Q_actions_list[np.argmax(self._Q_table[state])]
            # print(f"Based on optimality chose to... {self.action}")
        return self.action

    def update_Q(self, reward):
        if self.epsisode_age <= self.alpha_decay_episodes:
            alpha_temp = self.alpha_start - self.epsisode_age * (self.alpha_start - self.alpha_end) / self.alpha_decay_episodes
        else:
            alpha_temp = self.alpha_end

        new_value = self._get_Q(self.prev_state, self.action) + alpha_temp * \
            (reward + self.gamma * self._get_Q_optimal_action(self.curr_state) - self._get_Q(self.prev_state, self.action))

        self._set_Q(self.prev_state, self.action, new_value)
        # print(f"Updating Q value of {self.prev_state, self.action} to {new_value}")

    def _get_Q(self, state, action):
        # print(f"state {state}, action {action}")
        return self._Q_table[state][self._Q_actions_list.index(action)]

    def _set_Q(self, state, action, value):
        # print(f"state {state}, action {action}, value {value}")
        self._Q_table[state][self._Q_actions_list.index(action)] = value

    def _get_Q_optimal_action(self, state):
        # print(f"state {state}")
        return np.max(self._Q_table[state])
