import csv
import os
from datetime import datetime

from DungeonEscape.entities.Player import Player

DATABASE_FILE = 'db/players.csv'

class PlayerDB:
    def __init__(self, db_file=DATABASE_FILE):
        self.players_db = db_file
        if not os.path.exists(self.players_db):
            with open(self.players_db, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Username', 'MaxState', 'TimePlayed', 'EnemiesDefeated', 'ItemsCollected', 'LastLogin'])
                writer.writeheader()
        self.data = []

    def player_exists(self, username) -> bool:
        username = username.lower()
        with open(self.players_db, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Username'] == username:
                    return True
        return False

    def player_login(self, username):
        username = username.lower()
        if not self.player_exists(username):
            with open(self.players_db, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Username', 'MaxState', 'TimePlayed', 'EnemiesDefeated', 'ItemsCollected', 'LastLogin'])
                writer.writerow({'Username': username, 'MaxState': 0, 'TimePlayed': 0, 'EnemiesDefeated': 0, 'ItemsCollected': 0, 'LastLogin': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            print(f'{username} was added to Database')
            return Player(name=username, max_state=0, time_played=0,enemies_defeated=0, items_collected=0)
        else:
            with open(self.players_db, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Username'] == username:
                        return Player(name=row['Username'], max_state=(row['MaxState']), time_played=(row['TimePlayed']),
                                      enemies_defeated=(row['EnemiesDefeated']), items_collected=(row['ItemsCollected']))

    def update_player_stats(self, username, max_state, time_played, enemies_defeated, items_collected):
        data = []
        with open(self.players_db, mode='r', encoding="utf-8") as file:
            reader = csv.DictReader(file)
            header = reader.fieldnames
            for row in reader:
                if row['Username'] == username:
                    row['MaxState'] = max_state
                    row['TimePlayed'] = time_played
                    row['EnemiesDefeated'] = enemies_defeated
                    row['ItemsCollected'] = items_collected
                    row['LastLogin'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data.append(row)

        with open(self.players_db, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            writer.writerows(data)

    def get_leaderboard(self):
        data = []
        with open(self.players_db, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return sorted(data, key=lambda x: int(x["MaxState"]), reverse=True)