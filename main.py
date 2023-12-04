from src.flappyEnv import FlappyEnv
from src.RFB import RbfFeaturizer
import numpy as np
import asyncio

async def main():
    env = FlappyEnv()
    featurizer = RbfFeaturizer(env)
    
    # Hyperparameters
    featurizer.alpha = 0.1  # Increased learning rate
    featurizer.gamma = 0.95  # Adjusted discount factor
    featurizer.epsilon = 0.9  # Reduced initial exploration rate
    epsilon_decay = 0.05
    num_episodes = 10000
    min_epsilon = 0.01

    for episode in range(num_episodes):
        state, _ = await env.reset()
        features = featurizer.featurize(state)
        episode_Score = 0
        total_q_value_change = 0
        num_steps = 0
        total_Score = 0

        done = False
        while not done:
            action = featurizer.choose_action(features)
            next_state, reward, done, info = await env.step(action)
            #print(next_state)
            next_features = featurizer.featurize(next_state)
            old_q_value = featurizer.q_value(features, action)
            featurizer.update(features, action, reward, next_features, done)
            new_q_value = featurizer.q_value(features, action)
            total_q_value_change += abs(new_q_value - old_q_value)
            num_steps += 1
            features = next_features
            episode_Score += reward
            if done:
                break
        print(f"Score for episode {episode}: {episode_Score}")
        average_q_value_change = total_q_value_change / num_steps
        print(f"Average Q-value change in episode {episode}: {average_q_value_change}")

        # Update epsilon
        featurizer.epsilon = max(featurizer.epsilon - epsilon_decay, min_epsilon)
        print(f"epsilon: {featurizer.epsilon}")

    env.close()

# Run the main function
asyncio.run(main())
