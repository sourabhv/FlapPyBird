import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

def softmaxProb(x, Theta):
    preferences = np.transpose(Theta) @ x
    max_pref = np.max(preferences)
    divisor = np.sum(np.exp(preferences - max_pref))

    probabilities = (np.exp(preferences - max_pref)) / divisor

    return probabilities

def softmaxPolicy(x, Theta):
    probs = softmaxProb(x, Theta)
    
    return np.random.choice(len(probs), p=probs)

def logSoftmaxPolicyGradient(x, a, Theta):
    probs = softmaxProb(x, Theta)
    probs_row = np.reshape(probs, (1,) + probs.shape)

    x_col = np.reshape(x, x.shape + (1,))
    
    action_filter = np.zeros((1,Theta.shape[1]))
    action_filter[0,a] = 1.0
    # action_filter = init_action_filter.at[0,a].set(1.0)
    
    m1 = x_col @ action_filter
    m2 = x_col @ probs_row
    assert m1.shape == m2.shape
    grad = m1 - m2

    assert grad.shape == Theta.shape

    return grad

def log_performance(i, total_reward, log_dict):
    log_dict['episode'].append(i)
    log_dict['total_reward'].append(total_reward)

    if i%100==0:
        avg_reward = np.mean(log_dict['total_reward'][-100:])
        print(f"Episode {i}, Average reward over 100ep: {avg_reward}")

def update_plot(log_dict):
    plt.clf()  # Clear the current figure

    # Plot the reward for each episode
    plt.plot(log_dict['episode'], log_dict['total_reward'], label='Reward per Episode', color='blue')

    # Calculate and plot the average reward every 100 episodes
    avg_rewards = [np.mean(log_dict['total_reward'][max(0, i-100):i+1]) for i in range(len(log_dict['total_reward']))]
    plt.plot(log_dict['episode'], avg_rewards, label='Average Reward per 100 Episodes', color='red', linewidth=2)

    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.title('Reward per Episode and Average Reward per 100 Episodes')
    plt.legend()
    plt.pause(0.001)  # Pause briefly to update the plot

    

def ActorCritic(env,
                featurizer,
                eval_func,
                gamma=0.99,
                actor_step_size=0.005,
                critic_step_size=0.005,
                max_episodes=400,
                evaluate_every=20):
    plt.ion()
    Theta = np.random.rand(featurizer.n_features, env.action_space.n)
    w = np.random.rand(featurizer.n_features)
    eval_returns = []
    log_dict = {'episode':[], 'total_reward':[]}
    for i in range(1, max_episodes+1):
        s, info = env.reset()
        s = featurizer.featurize(s)
        terminated = truncated = False
        actor_discount = 1
        total_reward = 0
        while not (terminated or truncated):

            action = softmaxPolicy(s, Theta)
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward

            new_s = featurizer.featurize(obs)

            # compute TD error, keeping value at terminal states = 0
            td_error = reward + gamma * (1-terminated) * (new_s @ w) - (s @ w)

            # update critic and actor weights
            w += critic_step_size * td_error * s
            Theta += actor_step_size * td_error * actor_discount * logSoftmaxPolicyGradient(s, action, Theta)

            s = new_s
            actor_discount *= gamma

        if i % evaluate_every == 0:
            eval_return = eval_func(env, featurizer, Theta, softmaxPolicy)
            eval_returns.append(eval_return)
        log_performance(i,total_reward, log_dict)
        update_plot(log_dict)
    plt.ioff()
    update_plot(log_dict)
    plt.savefig('ActorCritic.png')
    plt.show()
    return Theta, w, eval_returns

def AdvantageActorCritic(env,
                featurizer,
                eval_func,
                gamma=0.99,
                actor_step_size=0.005,
                critic_step_size=0.005,
                max_episodes=3000,
                evaluate_every=20):
    plt.ion()
    Theta = np.random.rand(featurizer.n_features, env.action_space.n)
    w = np.random.rand(featurizer.n_features)
    eval_returns = []
    log_dict = {'episode':[], 'total_reward':[]}
    for i in range(1, max_episodes+1):
        s, info = env.reset()
        s = featurizer.featurize(s)
        terminated = truncated = False
        episode_rewards = []
        states = []
        actions = []
        # actor_discount = 1.0
        while not (terminated or truncated):

            action = softmaxPolicy(s, Theta)
            obs, reward, terminated, truncated, info = env.step(action)
            states.append(s)
            actions.append(action)
            episode_rewards.append(reward)
            s = featurizer.featurize(obs)

        G_t = 0
        returns = []
        for r in episode_rewards[::-1]:
            G_t = r + gamma * G_t
            returns.append(G_t)

        # # Compute advantages with normalized returns; not used since problem is future learning
        # advantages = [G - (s @ w) for G, s in zip(returns, states)]
        # advantages -= np.mean(advantages)  # Normalize
        # advantages /= (np.std(advantages) + 1e-10)  # Avoid division by zero

        #Actor/critic update with advantage
        for s, a, G in zip(states, actions, returns[::-1]):
            v_s = s @ w #current state value

            w += critic_step_size * (G - v_s) * s #update critic weights
            Theta += actor_step_size * (G - v_s) * logSoftmaxPolicyGradient(s, a, Theta) #update actor weights
        
        total_reward = sum(episode_rewards)
        log_dict['episode'].append(i)
        log_dict['total_reward'].append(total_reward)

        if i % evaluate_every == 0:
            eval_return = eval_func(env, featurizer, Theta, softmaxPolicy)
            eval_returns.append(eval_return)
        log_performance(i,total_reward, log_dict)
        update_plot(log_dict)
    plt.ioff()
    update_plot(log_dict)
    plt.savefig('AdvantageActorCritic.png')
    plt.show()
    return Theta, w, eval_returns

class RbfFeaturizer():
    '''
        This class converts the raw state/obvervation features into
        RBF features. It does a z-score normalization and computes the
        Gaussian kernel values from randomly selected centers.
    '''

    def __init__(self, env, n_features=100):
        centers = np.array([env.observation_space.sample()
                            for _ in range(n_features)])
        self._mean = np.mean(centers, axis=0, keepdims=True)
        self._std = np.std(centers, axis=0, keepdims=True)
        self._centers = (centers - self._mean) / self._std
        self.n_features = n_features

    def featurize(self, state):
        z = state[None, :] - self._mean
        z = z / self._std
        dist = cdist(z, self._centers)
        return np.exp(- (dist) ** 2).flatten()

def evaluate(env, featurizer, W, policy_func, n_runs=10):
    all_returns = np.zeros([n_runs])
    for i in range(n_runs):
        observation, info = env.reset()
        return_to_go = 0
        while True:
            observation = featurizer.featurize(observation)
            action = policy_func(observation, W)

            observation, reward, terminated, truncated, info = env.step(action)
            return_to_go += reward
            if terminated or truncated:
                break
        all_returns[i] = return_to_go

    return np.mean(all_returns)

