import pickle
from datetime import datetime

from RL_flappy import Flappy_Environment
from RL_agents import Flappy_QAgent

AGENT_BACKUP_FNAME = "flappy_agent_backup.dat"


# if __name__ == "__main__":

#     env = Flappy_Environment(1, 10, -100)

#     env.set_up()

#     while True:
#         print(env.take_action(action=""))

def train(n_episodes):

    try:
        with open(AGENT_BACKUP_FNAME, "rb") as f:
            flappy_agent: Flappy_QAgent = pickle.load(f)

        print(f"""Recovered agent from {AGENT_BACKUP_FNAME}\n""" +
              f"""Agent knows {len(flappy_agent._Q_states_list)} states and is {flappy_agent.epsisode_age} episodes old.""" +
              f"""{flappy_agent._Q_table}""")
    except:
        print("""Starting with a new fresh agent...""")

        flappy_agent = Flappy_QAgent(alpha=0.1, gamma=1, epsilon=0.1)

    flappy_env = Flappy_Environment(step_reward=+1, score_reward=0, die_reward=-10000)

    for episode in range(1, n_episodes):

        env_state = flappy_env.set_up()

        flappy_agent.update_state(player_pos=env_state["playerPos"],
                                  player_vel=env_state["playerVelY"],
                                  lower_pipes=env_state["lowerPipes"])

        while not env_state["crashInfo"][0]:

            flappy_agent.choose_action(state=flappy_agent.curr_state)

            env_reward, env_state = flappy_env.take_action(action=flappy_agent.action)

            flappy_agent.update_state(player_pos=env_state["playerPos"],
                                      player_vel=env_state["playerVelY"],
                                      lower_pipes=env_state["lowerPipes"])

            flappy_agent.update_Q(reward=env_reward)

        flappy_agent.epsisode_age += 1
        flappy_agent.best_score = max(flappy_agent.best_score, env_state["score"])

        if (episode) % 25 == 0:
            print(f"------------\nEPISODE {episode} of {n_episodes}")
            print(f"""{datetime.now().strftime("%H:%M:%S.%f")} | """ +
                  f"""score: {env_state["score"]} of best: {flappy_agent.best_score}, final state: {flappy_agent.curr_state}""")

            # save agent to pickle file
            print(f"""Saving agent to {AGENT_BACKUP_FNAME} file.\n""" +
                  f"""Agent knows {len(flappy_agent._Q_states_list)} states and is {flappy_agent.epsisode_age} episodes old.""")
            with open(AGENT_BACKUP_FNAME, "wb") as f:
                pickle.dump(flappy_agent, f)


def play():
    pass


if __name__ == '__main__':
    train(n_episodes=30000)
