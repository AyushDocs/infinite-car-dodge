# 🚗 Infinite Car Dodge – Project Roadmap

## 🎯 Goal
Build a 2D top-down game where a player dodges an infinite stream of evenly spaced cars coming from the top of the screen.  
Train an autonomous AI to play and master the game using machine learning.  
The final deliverable should demonstrate the AI improving from beginner-level to high-performance play.

---

## 📋 Game Specification

### Overview
- Player stays at the bottom of the screen, moves left/right.
- Cars spawn from the top in fixed lanes, moving downward at constant speed.
- Player must avoid collisions for as long as possible.
- Cars spawn in evenly spaced intervals.
- Game difficulty increases over time by gradually increasing car speed.

### Rules
1. **Movement**
   - Player can move left or right within bounds.
   - No acceleration, fixed speed.

2. **Obstacles**
   - Cars appear at fixed intervals in random lanes.
   - Cars move straight down until off-screen.

3. **Scoring**
   - Score increases with time survived.
   - Optional: bonus for near misses.

4. **Game Over**
   - Collision with any car ends the game.

5. **Replayability**
   - Game starts identically each run for consistent AI training.

---

## 🗂 Planning Process

1. **Goal Definition**
   - Build a game + AI agent to demonstrate ML learning in real-time.
   - Showcase as a professional, planned project.

2. **User Stories**
   - As a player, I can move left/right to dodge cars.
   - As a player, I can see my score increase as I survive.
   - As a player, I lose if I hit a car.
   - As an AI, I can observe the game state and decide moves automatically.
   - As a developer, I can track AI performance over many games.

3. **Data Models**
   - Player: position (x), speed.
   - Car: lane (x), position (y), speed.
   - Game state: player pos, car positions, score, speed level.
   - AI state: game state vector, chosen action.

4. **MVP**
   - Game loop with:
     - Player rectangle
     - Cars spawning & moving
     - Collision detection
     - Score system
   - Basic AI that randomly chooses moves.

5. **Future Vision**
   - More lanes, variable speeds, patterns.
   - AI using reinforcement learning or genetic algorithms.
   - Web deployment for interactive demos.

---

## 🗓 Weekly Roadmap

### **Week 1 – Planning & Setup**
- Finalize game concept and rules (**done**).
- Create `docs/PROJECT_PLAN.md` with full planning details.
- Set up repo with basic folder structure:
/docs
/game
/ai
/assets

- Initialize version control (Git + GitHub).
- Choose stack (Python + Pygame for game, Python ML libraries for AI).
- Create development environment & requirements file.
- Write placeholder main loop printing “Game starting…” for sanity check.

---

### **Week 2 – Core Game MVP**
- Implement game window with Pygame.
- Draw static player rectangle at bottom.
- Implement movement controls (left/right).
- Define lanes & car spawn positions.
- Spawn cars at fixed intervals (deterministic RNG).
- Move cars downward each frame.
- Detect collisions.
- Display score (time survived).
- Test until gameplay works reliably.

---

### **Week 3 – AI Hook & Random Agent**
- Define structured game state representation (array/vector).
- Replace manual controls with AI agent hook (reads state, outputs move).
- Implement simple random-action AI.
- Ensure AI can play many games in sequence automatically.
- Log score for each AI game.
- Produce simple performance chart over 100 games.

---

### **Week 4 – Learning AI v1**
- Choose first learning method (e.g., Q-learning or genetic algorithm).
- Implement training loop:
- Play many games
- Adjust AI based on performance
- Track score improvement over generations/episodes.
- Save & load AI models.
- Produce chart showing improvement trend.

---

### **Week 5 – Visualization & Demonstration**
- Create split-screen mode:
- Left: AI’s early games.
- Right: AI’s later, improved games.
- Add scoreboard & performance dashboard.
- Record short demo video of AI evolution.
- Write `README.md` explaining:
- How to run the game.
- How to train the AI.
- Key results.

---

### **Week 6 – Polish & Optional Features**
- Optional: add more lanes & car patterns.
- Optional: near-miss bonus points.
- Optional: difficulty ramp (speed increases over time).
- Optional: deploy game + AI as web app using Pyodide or WebAssembly.
- Clean code & finalize documentation.
- Tag release as **v1.0**.

---

## 📦 Final Deliverables
1. **Game source code** (`/game` folder)
2. **AI code & models** (`/ai` folder)
3. **Documentation** (`docs/PROJECT_PLAN.md`, `README.md`)
4. **Training logs** & performance charts
5. **Demo video** showing AI improvement
6. **Release build** ready to run

---

## 📈 Success Criteria
- **Game** runs smoothly with deterministic mechanics.
- **AI** starts as random and improves noticeably.
- **Performance logs** clearly show learning curve.
- **Demo video** is clear and compelling.
- **Documentation** proves this was a highly planned project.
