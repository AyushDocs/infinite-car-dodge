from ai.agent import RandomAgent
from game.main import get_ai_action, main
from matplotlib import pyplot as plt
import csv
from pathlib import Path
from datetime import datetime

LOG_FILE = Path(f"logs/performance-{datetime.now().isoformat(timespec='seconds').replace(':', '-')}.csv")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

if not LOG_FILE.exists():
    with open(LOG_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "agent", "run", "score"])



agent = RandomAgent()
scores = []

for run in range(1,11):
    score = main(get_ai_action)
    scores.append(score)
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            agent.__class__.__name__,
            run,
            score
        ])

print("Scores:", scores)
print("Average survival:", sum(scores) / len(scores))

plt.plot(scores)
plt.xlabel("Game")
plt.ylabel("Survival Time (seconds)")
plt.title("AI Survival Time Over Multiple Games")
plt.show()
