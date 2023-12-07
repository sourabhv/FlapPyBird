from src.flappyEnv2 import FlappyEnv2
from src.RFB import RbfFeaturizer
import numpy as np
import asyncio
import matplotlib.pyplot as plt

def main():
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
    
main()
