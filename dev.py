import argparse
import subprocess
import sys

def run_game():
    subprocess.run([sys.executable, "game.py"])

def run_ai():
    subprocess.run([sys.executable, "agent.py"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Infinite Car Dodge Launcher")
    parser.add_argument("--mode", choices=["game", "ai"], required=True, help="Run in game or AI mode")
    args = parser.parse_args()

    if args.mode == "game":
        run_game()
    elif args.mode == "ai":
        run_ai()
