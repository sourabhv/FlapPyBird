import numpy as np
from ...A2Helpers import *
from queue import PriorityQueue

# credits:
# https://arxiv.org/ftp/arxiv/papers/1206/1206.3285.pdf


async def DynaQFA(env, 
            featurizer, 
            gamma=0.99,
            step_size=0.005,
            epsilon=0.1,
            max_episode=400,
            max_model_step=20):
    start_epsilon = epsilon
    n_actions = 2

    Q = np.zeros((featurizer.n_features, n_actions))
    F = np.zeros( (featurizer.n_features, featurizer.n_features))
    b = np.zeros((featurizer.n_features))

    def epsilon_greedy_select(s, W):
        # with small chance, select a random action
        if np.random.uniform() < epsilon:
            return np.random.choice(n_actions)
        else:
            # otherwise just get the most popular
            return np.argmax(np.sum(np.transpose(W) * s, axis=1))
    max_reward = None
    recent_rewards = [0,0,0,0,0,0,0,0,0,0]
    for current_ep in range(max_episode):

        # epsilon = start_epsilon / (current_ep * 100 / max_episode + 1) ** 2
        print(epsilon)
        # reset world and get initial state        
        state, _ = await env.reset()        
        state = featurizer.featurize(state)

        terminated = truncated = False
        
        total_reward = 0
        while not (terminated or truncated):
            
            # select action
            a = epsilon_greedy_select(state, Q)
            # take action and observe outcome:
            new_state, reward, terminated, truncated, _ = await env.step(a)
            total_reward += reward
            new_state = featurizer.featurize(new_state)
            try:
                Q[:,a] = Q[:,a] + step_size * (reward + gamma * (Q.T[a] @ new_state) - Q.T[a] @ state) * state
                F = F + step_size * (new_state - F @ state) @ state
                b = b + step_size * (reward - b.T @ state) * state
                temp = new_state
                
                for i in range(max_model_step):
                    state = np.random.sample(featurizer.n_features)
                    new_state = F @ state                
                    r = b.T @ state               

                    Q[:,a] = Q[:,a] + step_size * (r + gamma * (Q.T[a] @ new_state) - (Q.T[a] @ state)) * state
            except RuntimeWarning:
                print("oopsie")
            state = temp
            
        if not max_reward or max_reward < total_reward:
            max_reward = total_reward
        recent_rewards = recent_rewards[1:] + [total_reward]
        print(f"{current_ep}: {recent_rewards[-1]} | {np.average(recent_rewards)}")
    # Pi = np.zeros_like(Q)
    
    # for i in range(len(Q)):
    #     Pi[i, np.argmax(Q[i])] = 1

    # Pi = diagonalization(Pi, env.n_states, env.n_actions)
    print(f"maximum reward: {max_reward}")
    return Q # Pi, np.reshape(Q, (env.n_states * env.n_actions, 1))
