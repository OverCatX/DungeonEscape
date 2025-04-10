import pygame

from DungeonEscape.db.player_data import PlayerDB
from DungeonEscape.entities.Entity import Entity

class Player(Entity):
    def __init__(self, x=0, y=0, sprite=None, health=100, armor=0, name="Player",
                 time_played=0, enemies_defeated=0, items_collected=0, max_state=0):
        super().__init__(x, y, sprite, health, armor)
        self.name = name
        self.speed = 5
        self.attack_animation = False
        self.sprites_up = []
        self.sprites_down = []
        self.sprites_left = []
        self.sprites_right = []
        self.time_played = time_played
        self.enemies_defeated = enemies_defeated
        self.items_collected = items_collected
        self.max_state = max_state

    def update(self):
        self.handle_input()
        super().update()

    def handle_input(self):
        pass

    def draw(self, screen):
        pass

    def take_damage(self, amount):
        pass

    def die(self):
        print(f"{self.name} has died.")

    def update_max_state(self, max_state):
        self.max_state = max_state
        print(f'Updated {self.name} MaxState to {self.max_state}')

    def update_time_played(self, time_played):
        self.time_played = time_played
        print(f'Updated {self.name} TimePlayed to {self.time_played}')

    def update_enemies_defeated(self, enemies_defeated):
        self.enemies_defeated = enemies_defeated
        print(f'Updated {self.name} EnemiesDefeated to {self.enemies_defeated}')

    def update_items_collected(self, items_collected):
        self.items_collected = items_collected
        print(f'Updated {self.name} ItemsCollected to {self.items_collected}')

    def __str__(self):
        return f'Player: {self.name}, MaxState: {self.max_state}, TimePlayed: {self.time_played}, EnemiesDefeated: {self.enemies_defeated}, ItemsCollected: {self.items_collected}'