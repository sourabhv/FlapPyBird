import numpy as np
from scipy.spatial.distance import cdist

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

def ActorCritic(env,
                featurizer,
                eval_func,
                gamma=0.99,
                actor_step_size=0.005,
                critic_step_size=0.005,
                max_episodes=400,
                evaluate_every=20):
    Theta = np.random.rand(featurizer.n_features, env.action_space.n)
    w = np.random.rand(featurizer.n_features)
    eval_returns = []
    for i in range(1, max_episodes+1):
        s, info = env.reset()
        s = featurizer.featurize(s)
        terminated = truncated = False
        actor_discount = 1
        while not (terminated or truncated):

            action = softmaxPolicy(s, Theta)
            obs, reward, terminated, truncated, info = env.step(action)

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

