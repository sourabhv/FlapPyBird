import asyncio
from src.flappyEnv import FlappyEnv
from src.models.QLearning import qlearning

async def run():
    env = FlappyEnv()

    model = qlearning.QLearner()
    Pi, Q = await model.run(env, 0.9, 0.1, 0.1, 1000)
    Pi.tofile('output/Pi.csv', sep=",")

    # for episode in range(10):
    #     await env.reset()
    #     total_reward = 0
    #     while True:
    #         action = env.action_space.sample()
    #         action = 0 if env.np_random.choice(20) == 0 else 0
    #         obs, reward, game_over, _, info = await env.step(action)
    #         total_reward += reward
    #         # print(obs)
    #         if game_over:
    #             print_episode_data(episode+1, total_reward)
    #             break           
    env.close()

def print_episode_data(episode, total_reward):
    print("--------------")
    print(f"Episode: {episode}")
    print(f"Score: {total_reward}")

if __name__ == "__main__":
    asyncio.run(run())
