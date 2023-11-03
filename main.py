import asyncio
from src.flappyEnv import FlappyEnv

if __name__ == "__main__":
    process = FlappyEnv()
    asyncio.run(process.run())
