import random

ACTIONS = ["left", "right", "stay"]

class RandomAgent:
    def act(self, state):
        return random.choice(ACTIONS)
