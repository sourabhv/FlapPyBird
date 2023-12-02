import asyncio
from src.flappyEnv import FlappyEnv
from src.models.QLearning import qlearning
from datetime import datetime

async def run():
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
            obs, reward, game_over, _, info = await env.step(action)
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

if __name__ == "__main__":
    asyncio.run(run())
