import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.monitor import Monitor

from game.main import CarDodgeEnv


TIMESTEPS = 200_000
LOG_DIR = "logs"
MODEL_DIR = "ai/models"
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

env = Monitor(CarDodgeEnv())
eval_env = Monitor(CarDodgeEnv())

model = DQN(
    "MlpPolicy",
    env,
    learning_rate=3e-4,
    buffer_size=100_000,
    learning_starts=5_000,
    batch_size=64,
    tau=1.0,
    gamma=0.99,
    train_freq=4,
    target_update_interval=1_000,
    exploration_fraction=0.3,
    exploration_final_eps=0.05,
    verbose=1,
    seed=42,
    device="cpu",
)

eval_callback = EvalCallback(
    eval_env=eval_env,
    best_model_save_path=MODEL_DIR,
    log_path=LOG_DIR,
    eval_freq=5_000,
    deterministic=True,
    render=False,
    n_eval_episodes=5,
)

model.learn(total_timesteps=TIMESTEPS, callback=eval_callback, log_interval=100)

model.save(f"{MODEL_DIR}/dqn_car_dodge_final.zip")
print(f"Training complete. Model saved to {MODEL_DIR}/dqn_car_dodge_final.zip")
env.close()
eval_env.close()