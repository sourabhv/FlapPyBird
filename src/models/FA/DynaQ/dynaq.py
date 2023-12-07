import numpy as np
from ...A2Helpers import *
import matplotlib.pyplot as plt
from queue import PriorityQueue

# credits:
# https://arxiv.org/ftp/arxiv/papers/1206/1206.3285.pdf


def DynaQFA(env, 
            featurizer, 
            gamma=0.99,
            step_size=0.005,
            epsilon=0.1,
            max_episode=400,
            max_model_step=20):
    start_epsilon = epsilon
    n_actions = 3
    taken_actions = []

    Q = np.zeros((featurizer.n_features, n_actions))
    F = np.zeros((n_actions, featurizer.n_features, featurizer.n_features))
    b = np.zeros((n_actions, featurizer.n_features))

    def epsilon_greedy_select(s):
        # with small chance, select a random action
        if np.random.uniform() < epsilon:
            a = np.random.choice(n_actions)
        else:
            # otherwise just get the most popular
            a = np.argmax([b[ac].T @ s + gamma * Q.T[ac] @ F[ac] @ s for ac in range(n_actions)])
        if a not in taken_actions: taken_actions.append(a)
        return a
    
    max_reward = None
    all_rewards = []


    tiling_particulars = [[(100,100,2),(10,10,0.2)],[(100,100,2),(0.0,0.0,0.0)],[(100,100,2),(-10,-10,-0.2)]] #[(#ofHorizontalPartition,#ofVerticalPartition),(horizontalShift, verticalShift)]
    # ts = featurizer.create_tilings_6d(tiling_particulars)
    
    
    plt.ion()
    plt.figure(1)

    for current_ep in range(max_episode):
        if current_ep % 100 == 0: epsilon = 0
        # epsilon = start_epsilon / (current_ep * 100 / max_episode + 1) ** 2
        # reset world and get initial state        
        state, _ = env.reset()  
        state = featurizer.featurize(state) # _6d(state, ts) / 100
        terminated = truncated = False
        
        total_reward = 0
        while not (terminated or truncated):
            
            # select action
            a = epsilon_greedy_select(state)
            # take action and observe outcome:
            new_state, reward, terminated, truncated, _ = env.step(a)
            total_reward += reward
            new_state = featurizer.featurize(new_state) # _6d(new_state, ts) / 100            

            delta = reward + gamma * (Q.T[a] @ new_state) - Q.T[a] @ state
            new_q = Q[:,a] + step_size * delta * state
            Q[:,a] = new_q
            F[a] = F[a] + step_size * (np.subtract(new_state, F[a] @ state)) @ state
            b[a] = b[a] + step_size * (reward - b[a].T @ state) * state
            
            # pqueue = PriorityQueue()
            # for i in range(len(state)):
            #     if state[i] != 0:
            #         pqueue.put((abs(delta * state[i]), i))

            # while pqueue.qsize() > 0:
                
            #     for p in range(max_model_step):                    
            #         i = pqueue.get()[1]
            #         nonzero = [x for x in range(len(state)) if (F[:,i,x] != 0).any()]
            #         print(len(nonzero))
            #         for j in nonzero:
            #             e_j = np.zeros_like(state)
            #             e_j[j] = 1
            #             delta = np.max(b[:,j] + gamma * Q.T @ F[:] @ e_j) - Q.T[j]
            #             Q[j] = Q[j] + step_size * delta
            #             pqueue.put((abs(delta), j))
            # state = new_state
            # continue

            temp = new_state
            
            for p in range(max_model_step):
                state = np.random.sample(featurizer.n_features)
                a = np.random.choice(taken_actions)

                new_state = F[a] @ state                
                r = b[a].T @ state  
                
                # print(np.max([Q.T[i] * new_state for i in range(n_actions)], axis=1))
                new_q = Q[:,a] + step_size * (r + (gamma * Q.T[a] @ new_state) - (Q.T[a] @ state)) * state
                Q[:,a] = new_q

            state = temp
            
        if not max_reward or max_reward < total_reward:
            max_reward = total_reward
        if current_ep % 100 == 0: 
            epsilon = start_epsilon
            print(f"GREEDY SELECT STEP: {total_reward}")
            
        all_rewards = all_rewards[:min(len(all_rewards), 99)]   
        all_rewards.append(total_reward)
        plt.plot(all_rewards)   
        
    # Pi = np.zeros_like(Q)
    
    # for i in range(len(Q)):
    #     Pi[i, np.argmax(Q[i])] = 1

    # Pi = diagonalization(Pi, env.n_states, env.n_actions)
    print(f"maximum reward: {max_reward}")
    plt.plot(all_rewards)
    return Q # Pi, np.reshape(Q, (env.n_states * env.n_actions, 1))
