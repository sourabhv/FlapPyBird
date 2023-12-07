from src.RFB import RbfFeaturizer
import numpy as np
import asyncio
import matplotlib.pyplot as plt
from src.flappyEnv import FlappyEnv
from src.flappyEnv2 import FlappyEnv2
from src.models.QLearning import qlearning
from src.models import DQN, ActorCritic
from datetime import datetime

def linear_regression():
    env = FlappyEnv2()
    featurizer = RbfFeaturizer(env)
    
    # try:
    #     featurizer.theta = np.load('theta_matrix.npy')
    # except FileNotFoundError:
    #     pass  # If the file does not exist, continue with initialization

    
    # Hyperparameters
    featurizer.alpha = 0.005
    featurizer.gamma = 0.9
    featurizer.epsilon = 0.9 
    epsilon_decay = 0.995
    num_episodes = 10000
    alpha_decay = 0.9995
    min_alpha = 0.005
    min_epsilon = 0.01
    rewards = [] 
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot(rewards)
    plt.xlabel('Episode')
    plt.ylabel('Reward')

    for episode in range(num_episodes):
        state, _ = env.reset()
        features = featurizer.featurize(state)
        episode_Score = 0
        total_q_value_change = 0
        num_steps = 0
        total_Score = 0

        done = False
        while not done:
            action = featurizer.choose_action(features)
            next_state, reward, done, info = env.step(action)
            #print(next_state)
            next_features = featurizer.featurize(next_state)
            featurizer.update(features, action, reward, next_features, done)
            num_steps += 1
            features = next_features
            episode_Score += reward
            if done:
                break
        rewards.append(episode_Score)
        
        x_data = list(range(1, episode + 2)) 
        y_data = rewards
        
        line.set_xdata(x_data)
        line.set_ydata(y_data)
        
        ax.relim() 
        ax.autoscale_view() 

        plt.draw()
        plt.pause(0.001)

        featurizer.epsilon = max(featurizer.epsilon * epsilon_decay, min_epsilon)
        featurizer.alpha = max(featurizer.alpha * alpha_decay, min_alpha)

    plt.ioff() 
    plt.savefig('LINEARQAGENTGRAPH.png')
    plt.show() 
    np.save('theta_matrix.npy', featurizer.theta)
    
    env.close()

def run():
    env = FlappyEnv()

    # model = qlearning.QLearner()
    # Pi, Q = await model.run(env, gamma=0.9, step_size=0.1, epsilon=0.1, max_episode=60000, callback_step=100, callback=callback)
    # Pi.tofile('output/Pi.csv', sep=",")

    for episode in range(10):
        env.reset()
        total_reward = 0
        while True:
            action = env.action_space.sample()
            action = 0 if env.np_random.choice(20) == 0 else 0
            obs, reward, game_over, _, info = env.step(action)
            total_reward += reward
            # print(obs)
            if game_over:
                callback(episode+1, total_reward)
                break           
    env.close()

def callback(episode:int=None, score:float=None, Q=None):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # print("--------------")
    print(f"{current_time}  --  Episode: {episode} || Score: {score}")
    # possibly save Q to file

def run_dqn():
    env = FlappyEnv2()
    # print(env.observation_space)

    model = DQN.DQN_Model(env)
    # print(model.device)

    model.train(500, 9)

def run_ac():
    env = FlappyEnv2()
    featurizer = ActorCritic.RbfFeaturizer(env, 100)

    Theta, w, eval_returns = ActorCritic.ActorCritic(env, featurizer, ActorCritic.evaluate, max_episodes=1000)

    print(eval_returns)

if __name__ == "__main__":
    run_ac()
