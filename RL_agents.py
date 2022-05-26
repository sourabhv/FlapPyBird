import pickle
from itertools import cycle
from datetime import datetime

import numpy as np
# from tqdm import tqdm

AGENT_BACKUP_FNAME = "agent_backup.dat"


class Flappy_QAgent:

    def __init__(self, alpha=0.7, gamma=1, epsilon=0.15, step_reward=0, die_reward=-1000) -> None:
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.step_reward = step_reward
        self.die_reward = die_reward

        # Dynamic variables
        self.best_score = 0
        self.epsisode_age = 0

        self.action = ""
        self.curr_state = [10, 10, 0]

        self._Q_actions_list = ["flap", ""]
        self._Q_states_list = [0]  # init with dummy value
        self._Q_table = np.array([[0 for _ in range(len(self._Q_actions_list) + 1)]])  # init with dummy value (so that .vstack works)

    def _speed_mapping(self, speed):
        return int((speed // 3) * 3)

    def _distance_mapping(self, distance):
        if abs(distance) <= 50:
            return int((distance // 5) * 5)
        elif abs(distance) <= 150:
            return int((distance // 20) * 20)
        else:
            return int((distance // 100) * 100)

    def update_state(self, player_pos, player_vel, lower_pipes):

        next_pipe = 0 if player_pos[0] <= (lower_pipes[0]["x"] + 50) else 1

        player_vel = self._speed_mapping(player_vel)
        x_dist = self._distance_mapping(lower_pipes[next_pipe]['x'] - player_pos[0])
        y_dist = self._distance_mapping(lower_pipes[next_pipe]['y'] - player_pos[1])

        state = [x_dist, y_dist, player_vel]

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
        self.curr_state = [x_dist, y_dist, player_vel]

    def choose_action(self, state) -> str:
        if np.random.uniform() < self.epsilon:
            self.action = self._Q_actions_list[np.random.randint(len(self._Q_actions_list))]
            # print(f"Randomly chose to... {self.action}")
        else:
            self.action = self._Q_actions_list[np.argmax(self._Q_table[self._Q_states_list.index(state), :len(self._Q_actions_list)])]
            # print(f"Based on optimality chose to... {self.action}")

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


if __name__ == '__main__':

    import flappy

    info = {'playery': 300 + 8,
            'basex': 12,
            'playerIndexGen': cycle([0, 1, 2, 1]),
            }

    try:
        with open(AGENT_BACKUP_FNAME, "rb") as f:
            flappy_agent: Flappy_QAgent = pickle.load(f)

        flappy_agent.epsilon = 0.05
        flappy_agent.alpha = 0.7

        print(f"""Recovered agent from {AGENT_BACKUP_FNAME}\n""" +
              f"""Agent knows {len(flappy_agent._Q_states_list)} states and is {flappy_agent.epsisode_age} episodes old.""" +
              f"""{flappy_agent._Q_table}""")

    except:
        print("""Starting with a new fresh agent...""")
        flappy_agent = Flappy_QAgent()

    for episode in range(30000):
        print(f"------------\nEPISODE {episode}")

        if True:
            crashInfo = flappy.mainGame(movementInfo=info, QAgent=flappy_agent, gui=False, speed_up=True)

            flappy_agent.update_state(player_pos=crashInfo["pos"],
                                      player_vel=crashInfo["playerVelY"],
                                      lower_pipes=crashInfo["lowerPipes"])

            print(f"""{datetime.now().strftime("%H:%M:%S")} | score: {crashInfo["score"]} of best: {flappy_agent.best_score}, final state: {flappy_agent.curr_state}""")

            flappy_agent.update_Q(reward=flappy_agent.die_reward)
            flappy_agent.epsisode_age += 1
            flappy_agent.best_score = max(flappy_agent.best_score, crashInfo["score"])

            if (episode + 0) % 25 == 0:
                # save agent to pickle file
                print(f"""Saving agent to {AGENT_BACKUP_FNAME} file.\n""" +
                      f"""Agent knows {len(flappy_agent._Q_states_list)} states and is {flappy_agent.epsisode_age} episodes old.""")
                with open(AGENT_BACKUP_FNAME, "wb") as f:
                    pickle.dump(flappy_agent, f)
        else:
            flappy.main(QAgent=flappy_agent, speed_up=True)
