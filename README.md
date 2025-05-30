
# 🐉 Dungeon Escape V1.0

## 🧭 Overview
**Dungeon Escape** is a fast-paced, top-down roguelike built with Python and Pygame.
Fight through procedurally generated dungeons, survive waves of enemies, avoid deadly traps, and make your way to the glowing exit.

Choose from 3 distinct characters — each with their own combat style — and challenge yourself to survive as many stages as possible. Every session is tracked, visualized, and saved for analysis.

## 🚀 Game Concept
Escape the dungeon by defeating enemies and evading deadly traps. Use character-specific mechanics to survive increasingly difficult stages. Data is collected and visualized after each session to understand player performance.

---

## 🧙‍♂️ Characters

- **Assassin**: Agile melee specialist. Strong against isolated enemies. High mobility but low durability.
- **Archer**: Long-range damage dealer. Effective from a distance but fragile in close combat.
- **Blink**: Blink-slash attacker with high burst and mobility. Can dash and reposition rapidly but requires strategic timing.

---

## ⚔️ Game Features

- 🔁 **Procedural Generation** – Unique dungeon every run
- 🧠 **Smart Enemies** – Pathfinding and AI behavior
- 💥 **Combat System** – Attacks, damage, hit flashing, and cooldowns
- 🕹️ **Traps** – Spikes, poison, timed triggers
- 💾 **Stat Tracking** – Save session data in `CSV`
- 📊 **Visualizer** – View performance through multiple graph types
- 📁 **Data Summary** – Player summaries stored in `players.csv`

Dungeon Escape is a wave-based action roguelike where the player must survive procedurally generated dungeons, defeat monsters, avoid traps, and collect power-ups. The main loop is centered around a **wave system** and **escalating difficulty** through continuous dungeon progression.

### 🌀 Wave-Based Combat
- Each stage consists of **multiple enemy waves**, with each wave increasing in difficulty.
- Players must clear all enemies in a wave before the next one spawns.
- After clearing all waves, the player must reach the **exit point (trap hole)** to complete the stage.
- The challenge lies in surviving longer and pushing through as many stages as possible in a single run.

### 🗺️ Procedural Stages
- Every dungeon is uniquely generated, ensuring high replayability.
- Exit points, traps, and enemies are placed in randomized but reachable positions.

### 🎯 Strategic Character Roles
- Each character excels in different scenarios:
  - Assassin: Close-range burst damage.
  - Archer: Long-range control.
  - Blink: Hit-and-run warp attacks with lifesteal.

### 💥 Traps & Survival
- Traps are randomized and trigger upon stepping over.
- Players gain stats based on trap triggers, damage dealt, dashes used, and more.

### 📈 Progression & Challenge
- No traditional upgrade system — it's all about mastering your skills, map awareness, and adapting to enemy waves.
- The more stages you complete, the more difficult the dungeon becomes.
---

## 📊 Statistical Features Tracked

| Feature | Description |
|--------|-------------|
| Time Spent | Duration per session |
| Enemies Defeated | Total enemies killed |
| Dash Used | Dash mechanics per run |
| Traps Triggered | How many traps were stepped on |
| Distance Traveled | Movement across map |
| Character Used | Selected class |
| Survival | Whether the player exited or died |

---

---
## 🖥️ Gameplay Example
![Gameplay1](https://github.com/OverCatX/DungeonEscape/blob/main/screenshots/gameplay/1_home_screen.png?raw=true)
![Gameplay2](https://github.com/OverCatX/DungeonEscape/blob/main/screenshots/gameplay/6_charactor_blink.png?raw=true)
![Gameplay3](https://github.com/OverCatX/DungeonEscape/blob/main/screenshots/gameplay/9_blink_playing.png?raw=true)
![Gameplay4](https://github.com/OverCatX/DungeonEscape/blob/main/screenshots/gameplay/8_archer_playing.png?raw=true)
![Gameplay5](https://github.com/OverCatX/DungeonEscape/blob/main/screenshots/gameplay/11_health_item.png?raw=true)
![Gameplay6](https://github.com/OverCatX/DungeonEscape/blob/main/screenshots/gameplay/2_individual_player_stat_overview.png?raw=true)
---

## 📉 Visualization (Data Component)

Implemented using `matplotlib` and embedded in `tkinter` UI:

- 📈 **Histogram** – Time spent in dungeon
- 🥧 **Pie Chart** – Character usage
- 🔵 **Scatter Plot** – Enemies defeated vs. survival outcome
- 📊 **Bar Chart** – Avg dashes used per character
- 📈 **Line Graph** – Distance traveled per session

![Data1](https://github.com/OverCatX/DungeonEscape/blob/main/screenshots/visualization/Histogram_Time_Spending.png?raw=true)
![Data2](https://github.com/OverCatX/DungeonEscape/blob/main/screenshots/visualization/Bar_Average_Dash_by_Charactor.png?raw=true)
![Data3](https://github.com/OverCatX/DungeonEscape/blob/main/screenshots/visualization/Line_Distance_Traveled.png?raw=true)
![Data4](https://github.com/OverCatX/DungeonEscape/blob/main/screenshots/visualization/Pie_Chart_Charactor_Used.png?raw=true)
![Data5](https://github.com/OverCatX/DungeonEscape/blob/main/screenshots/visualization/Scatter_Enemies_vs_Survival.png?raw=true)
---

## 🧪 Installation & Run

**1. Clone the project from GitHub**
```bash
git clone https://github.com/OverCatX/DungeonEscape.git
cd DungeonEscape
```

**2. Create a virtual environment (Optional)**
```bash
python -m venv venv
source venv/bin/activate  # on Unix/macOS
venv\Scripts\activate     # on Windows
```

⚠️ **Important Notes Before Running the Game**

Please make sure the following Python packages are installed:

- `pygame` – for game engine and rendering
- `matplotlib` – for data visualization graphs
- `pandas` – for player statistics processing
- `numpy` – used in visual analysis and random data jittering

To install all required packages at once, run:

**3. Install required packages**
```bash
pip install -r requirements.txt
```

**4. Run the game**
```bash
python game.py
```

---

## 📹 Video Presentation

🎥 [Click to watch](https://youtu.be/QCp5Ip2avjc?feature=shared)

- Game overview
- Character and enemy design
- Data collection and visualization
- OOP architecture + UML class diagram
- GUI and responsiveness
- Extra features beyond requirement

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more info.

---

