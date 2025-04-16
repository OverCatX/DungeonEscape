import csv
import os
from entities.player import Player

class PlayerDB:
    def __init__(self):
        self.file_path = os.path.join("db", "players.csv")
        self.fieldnames = ['name', 'max_state', 'current_stage', 'time_played', 'enemies_defeated', 'items_collected']

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
                    items_collected=int(row['items_collected'])
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
                row['max_state'] = player.max_state
                row['current_stage'] = player.current_stage
                row['time_played'] = player.time_played
                row['enemies_defeated'] = player.enemies_defeated
                row['items_collected'] = player.items_collected
                updated = True
                break

        if not updated:
            players.append({
                'name': player.name,
                'max_state': player.max_state,
                'current_stage': player.current_stage,
                'time_played': player.time_played,
                'enemies_defeated': player.enemies_defeated,
                'items_collected': player.items_collected
            })

        with open(self.file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(players)

    def update_player(self, player):
        self.save_player(player)
