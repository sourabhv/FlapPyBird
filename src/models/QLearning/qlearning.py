import numpy as np
from .A2helpers import *

class QLearner:
    async def run(self, env, gamma, step_size, epsilon, max_episode):

        def epsilon_greedy_select(q):
            # with small chance, select a random action
            if np.random.uniform() < epsilon:
                return np.random.randint(len(q))
            else:
                # otherwise just get the most popular
                return np.argmax(q)

        Q = np.zeros(env.get_state_shape + (env.n_actions,))
        print(Q.shape)

        for _ in range(max_episode):

            # reset world and get initial state        
            obs, _ = await env.reset()

            state = list(obs.values())

            terminated = False
            while not terminated:
                
                # select action
                # print(state)
                action = epsilon_greedy_select(self._lookup(Q, state))
                
                # take action and observe outcome:
                obs, reward, terminated, _, _ = await env.step(action)

                # update Q value
                new_state = list(obs.values())
                # print(new_state)
                self._lookup(Q,state)[action] = self._lookup(Q, state)[action] + step_size * (reward + gamma * max(self._lookup(Q,new_state)) - self._lookup(Q, state)[action])
            
                # update state
                state = new_state
        print("reached pi!!!!!")
        Q_2D = np.reshape(Q, (-1, 2))
        Pi = np.zeros_like(Q_2D)
        
        for i in range(len(Q_2D)):
            Pi[i, np.argmax(Q_2D[i])] = 1

        # Pi = diagonalization(Pi, np.prod(list(env.get_state_shape)), env.n_actions)

        return Pi, np.reshape(Q_2D, (np.prod(list(env.get_state_shape)) * env.n_actions, 1))

    def _lookup(self, dict, indexers):
        if len(indexers) == 0:
            return dict
        
        return self._lookup(dict[indexers[0]], indexers[1:])

    def DynaQ(env, gamma, step_size, epsilon, max_episode, max_model_step):

        Q = np.zeros((env.n_states,env.n_actions))
        Model = np.zeros((env.n_states, env.n_actions, 2))

        def epsilon_greedy_select(q):
            # with small chance, select a random action
            if np.random.uniform() < epsilon:
                return np.random.randint(len(q))
            else:
                # otherwise just get the most popular
                return np.argmax(q)
            
        def planning_update():
            for _ in range(max_model_step):
                # find all non-zero items
                rows = []
                cols = []

                for i in range(len(Model)):
                    for j in range(len(Model[i])):
                        if len(Model[i,j]) > 0:
                            rows.append(i)
                            cols.append(j)

                # select a random state-action
                ind = np.random.randint(len(rows))
                
                s = rows[ind]
                a = cols[ind]
                Q[s,a] = Q[s,a] + step_size * (Model[s,a][0] + gamma * max(Q[int(Model[s,a,1])]) - Q[s,a])


        for _ in range(max_episode):

            # reset world and get initial state        
            state, _ = env.reset()

            terminated = False

            while not terminated:
                
                # select action
                action = epsilon_greedy_select(Q[state])
                
                # take action and observe outcome:
                new_state, reward, terminated, _, _ = env.step(action)
                
                # update Q value
                Q[state, action] = Q[state, action] + step_size * (reward + gamma * max(Q[new_state]) - Q[state, action])
            
                # add state and action to list of tried states/actions
                Model[state, action] = (reward, new_state)

                planning_update()
                
                # update state
                state = new_state

        Pi = np.zeros_like(Q)
        
        for i in range(len(Q)):
            Pi[i, np.argmax(Q[i])] = 1

        Pi = diagonalization(Pi, env.n_states, env.n_actions)

        return Pi, np.reshape(Q, (env.n_states * env.n_actions, 1))