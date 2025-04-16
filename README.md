# Dungeon Escape - v0.5 🚪⚔️

**Dungeon Escape** is a procedurally generated action/roguelike/puzzle game made with `pygame`.  
Your mission: survive waves of monsters, collect upgrades, avoid traps, and escape the dungeon!

---

## 🎯 Game Objective

- Survive procedurally generated dungeons filled with traps and enemies.
- Complete **multiple waves** of enemies in each stage before progressing.
- Upgrade your character stats by progressing through stages.

---

## 🌟 Key Features in v0.5

- ✅ **Procedural Map Generation**
- ✅ **Wave-based Enemy Spawning**
- ✅ **Multiple Enemy Types (via `enemy_manager`)**
- ✅ **Player Combat System with Attack Animation**
- ✅ **Enemy AI Movement & Collision Avoidance**
- ✅ **Health, Energy & Dash Mechanics**
- ✅ **Stat HUD (Stage, Wave, HP, Energy, Enemies Left)**
- ✅ **Traps: Spikes, Poison, Timed Spike**
- ✅ **Pause Menu with Continue/Exit**
- ✅ **Wave Popup Notification System**
- ✅ **Stage Completion with Fade Out Transition**
- ✅ **Persistent Player Stats via JSON (e.g., enemies defeated)**

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

2. **ติดตั้ง dependencies** (เช่น `pygame`)

```bash
pip install -r requirements.txt
```

> หากไม่มี `requirements.txt` สามารถติดตั้ง pygame ด้วยคำสั่ง:
```bash
pip install pygame
```

3. **Run the game**

```bash
python game.py
```

4. **Login** ด้วยชื่อตัวละคร หรือสร้าง player ใหม่

5. **เลือกโหมดเกม** และเริ่มเล่นได้เลย!

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

## 📷 Screenshot Suggestion (Optional)

```
[insert_screenshot_1.png]
[insert_screenshot_2.gif]
```

---

## 📂 Directory Structure (Simplified)

```
DungeonEscape/
│
├── game.py
├── config.py
├── requirements.txt
├── assets/
│   └── player, enemies, tiles, ...
├── db/
│   └── player_data.py
├── entities/
│   └── player.py, enemy.py, demon_red.py, ...
├── managers/
│   └── enemy_manager.py
├── map/
│   └── random_map_generator.py
└── ui/
    └── hud.py, menu.py
```

---

## 👨‍💻 Author

- Your Name / Team
- Assignment for [Course Name or Instructor]

