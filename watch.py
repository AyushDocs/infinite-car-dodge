import os
os.environ["SDL_VIDEODRIVER"] = "x11"

import time
from stable_baselines3 import DQN

from game.main import CarDodgeEnv


model_path = "ai/models/dqn_car_dodge_final.zip"
env = CarDodgeEnv(render_mode="human")

try:
    model = DQN.load(model_path)
except FileNotFoundError:
    print(f"Model not found at {model_path}. Train first with: python train.py")
    exit(1)

obs, _ = env.reset()
total_reward = 0
step = 0

while True:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    total_reward += reward
    step += 1

    if terminated or truncated:
        print(f"Game over! Steps: {step}, Total reward: {total_reward:.2f}")
        time.sleep(1.5)
        obs, _ = env.reset()
        total_reward = 0
        step = 0

    time.sleep(1 / 60)