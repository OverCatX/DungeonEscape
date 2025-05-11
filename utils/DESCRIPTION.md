
# 🐉 Dungeon Escape

## 🧭 Overview
**Dungeon Escape** is a procedurally generated top-down roguelike action-puzzle game built using Python and `pygame`. Players take on the role of one of three unique characters and must survive waves of enemies, avoid traps, and reach the dungeon exit. Every session is tracked and visualized using `matplotlib` and `tkinter` for gameplay insights.

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

## 📉 Visualization (Data Component - 20%)

Implemented using `matplotlib` and embedded in `tkinter` UI:

- 📈 **Histogram** – Time spent in dungeon
- 🥧 **Pie Chart** – Character usage
- 🔵 **Scatter Plot** – Enemies defeated vs. survival outcome
- 📊 **Bar Chart** – Avg dashes used per character
- 📈 **Line Graph** – Distance traveled per session

---

## 📂 File Structure

```
DungeonEscape/
├── assets/
├── db/
│   └── players.csv
├── stats/
│   ├── session_log.csv
│   └── players.csv
├── entities/
│   ├── players/
│   ├── enemies/
│   └── items/
├── ui/
│   ├── hud.py
│   ├── menu.py
│   └── charactor_menu.py
├── map/
│   └── random_map_generator.py
├── visualizer/
│   ├── graph_viewer.py
│   └── player_stats_viewer.py
├── game.py
├── config.py
├── requirements.txt
├── README.md
└── DESCRIPTION.md
```

---

## 🧪 Installation & Run

```bash
pip install -r requirements.txt
python main.py
```

---

## 📹 Video Presentation

🎥 [Click to watch](https://youtube.com/your_video_link)

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

## 🔖 Tags

- `v0.5` – 50% progress (April 16)
- `v1.0` – Final submission (May 11)

---

## 💬 Final Note

This project combines gameplay depth with data insights, showing mastery in OOP, procedural design, enemy AI, and statistical analysis. Every mechanic—from dash-based combat to the trap system—was designed for strategic, replayable action.

