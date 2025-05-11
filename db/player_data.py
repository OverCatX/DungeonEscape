import os
import csv
import pandas as pd
from entities.players.player import Player

SAVE_FOLDER = "stats"
SESSION_FILE = os.path.join(SAVE_FOLDER, "session_log.csv")
SUMMARY_FILE = os.path.join(SAVE_FOLDER, "players.csv")
PLAYER_FILE = os.path.join("db", "players.csv")

os.makedirs(SAVE_FOLDER, exist_ok=True)

class PlayerDB:
    def __init__(self):
        self.file_path = PLAYER_FILE
        self.fieldnames = ['name', 'max_state', 'current_stage', 'time_played', 'enemies_defeated']

        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()

    def player_login(self, name):
        players = self.load_all_players()
        for row in players:
            if row['name'] == name:
                return Player(
                    name=row['name'],
                    max_state=int(row['max_state']),
                    current_stage=int(row.get('current_stage', 1)),
                    time_played=float(row['time_played']),
                    enemies_defeated=int(row['enemies_defeated']),
                )

        new_player = Player(name=name)
        self.save_player(new_player)
        return new_player

    def load_all_players(self):
        with open(self.file_path, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def save_player(self, player):
        players = self.load_all_players()
        updated = False

        for row in players:
            if row['name'] == player.name:
                row['max_state'] = max(player.max_state, int(row['max_state']))
                row['current_stage'] = max(player.current_stage, int(row.get('current_stage', 1)))
                row['time_played'] = round(float(row['time_played']) + player.time_played, 2)
                row['enemies_defeated'] = int(row['enemies_defeated']) + player.enemies_defeated
                updated = True
                break

        if not updated:
            players.append({
                'name': player.name,
                'max_state': player.max_state,
                'current_stage': player.current_stage,
                'time_played': round(player.time_played, 2),
                'enemies_defeated': player.enemies_defeated
            })

        with open(self.file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(players)

    def update_player(self, player):
        self.save_player(player)

def save_session(player):
    log = {
        "name": player.name,
        "character": player.character_type,
        "time_played": round(player.time_played, 2),
        "enemies_defeated": player.enemies_defeated,
        "dash_used": player.dash_used,
        "traps_triggered": player.traps_triggered,
        "distance_traveled": round(player.distance_traveled, 2),
        "survived": player.survived
    }

    file_exists = os.path.exists(SESSION_FILE)
    with open(SESSION_FILE, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=log.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(log)
    print(f'(Session) Saved Player: {player.name} with {log}')

def generate_player_summary():
    if not os.path.exists(SESSION_FILE):
        print("No session data to summarize.")
        return

    df = pd.read_csv(SESSION_FILE)
    grouped = df.groupby("name").agg({
        "time_played": "mean",
        "enemies_defeated": "mean",
        "dash_used": "mean",
        "traps_triggered": "mean",
        "distance_traveled": "mean",
        "survived": "mean",
        "name": "count"
    }).rename(columns={"name": "total_sessions"})

    grouped = grouped.reset_index()
    grouped = grouped.round(2)
    grouped.to_csv(SUMMARY_FILE, index=False)
    print(f"Player summary saved to {SUMMARY_FILE}")
