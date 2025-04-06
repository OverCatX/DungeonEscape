from DungeonEscape.db.player_data import PlayerDB
from DungeonEscape.entities.Player import Player

class SaveManager:
    def __init__(self):
        self.db = PlayerDB()

    def save_player(self, player: Player):
        self.db.update_player_stats(
            player.name,
            int(player.max_state),
            float(player.time_played),
            int(player.enemies_defeated),
            int(player.items_collected)
        )