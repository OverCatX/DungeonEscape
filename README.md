# Dungeon Escape - v0.5

**Dungeon Escape** is a procedurally generated action/roguelike/puzzle game made with `pygame`.  
Your mission: survive waves of monsters, collect upgrades, avoid traps, and escape the dungeon!

---

## Game Objective

- Survive procedurally generated dungeons filled with traps and enemies.
- Complete **multiple waves** of enemies in each stage before progressing.
- Upgrade your character stats by progressing through stages.

---

## Key Features in v0.5

- **Procedural Map Generation**
- **Wave-based Enemy Spawning**
- **Multiple Enemy Types (via `enemy_manager`)**
- **Player Combat System with Attack Animation**
- **Enemy AI Movement & Collision Avoidance**
- **Health, Energy & Dash Mechanics**
- **Stat HUD (Stage, Wave, HP, Energy, Enemies Left)**
- **Traps: Spikes, Poison, Timed Spike**
- **Pause Menu with Continue/Exit**
- **Wave Popup Notification System**
- **Stage Completion with Fade Out Transition**
- **Persistent Player Stats via JSON (e.g., enemies defeated)**

---

## 🕹 Controls

| Key         | Action               |
|-------------|----------------------|
| `WASD`      | Move character       |
| `Shift`     | Dash (uses energy)   |
| `Space`     | Attack               |
| `Mouse`     | Interact with UI     |

---

## 🚀 How to Run

1. **Clone the repository** (หรือแตกไฟล์ `.zip` ที่ได้จากการดาวน์โหลด)

```bash
git clone https://github.com/your-username/DungeonEscape.git
cd DungeonEscape
```

2. **Install dependencies** (`pygame`)

```bash
pip install -r requirements.txt
```

>You can install `pygame` follow command:
```bash
pip install pygame
```

3. **Run the game**

```bash
python game.py
```

4. **Login** by Charactor name or create new charactor

5. **Select Game Mode** and Start game

---

## 📌 Progress Note

This marks version **v0.5** representing ~50% development milestone.  
The game is functional and demonstrates core gameplay mechanics such as:
- Player control and combat
- Enemy waves
- Trap interaction
- Pause functionality
- Persistent player progress

---
