from ai.agent import RandomAgent
from game.main import get_ai_action, main
from matplotlib import pyplot as plt
agent = RandomAgent()
scores = []

for _ in range(5):
    score = main(get_ai_action)
    scores.append(score)

print("Scores:", scores)
print("Average survival:", sum(scores) / len(scores))

plt.plot(scores)
plt.xlabel("Game")
plt.ylabel("Survival Time (seconds)")
plt.title("AI Survival Time Over Multiple Games")
plt.show()
