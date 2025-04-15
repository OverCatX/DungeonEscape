import pygame
from DungeonEscape.entities.entity import Entity

class Player(Entity):
    def __init__(self, x=0, y=0, health=100, armor=0, name="Player",
                 time_played=0, enemies_defeated=0, items_collected=0, max_state=0, current_stage=1):
        super().__init__(asset_folder='player' ,x=x, y=y)
        self.name = name
        self.health = health
        self.armor = armor
        self.speed = 3

        # Player Stats
        self.time_played = time_played
        self.enemies_defeated = enemies_defeated
        self.items_collected = items_collected
        self.max_state = max_state
        self.current_stage = current_stage

    def update(self, dt):
        super().update(dt)
        self.handle_input()

    def handle_input(self):
        self.move_x = 0
        self.move_y = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.move_x = -self.speed
        if keys[pygame.K_d]:
            self.move_x = self.speed
        if keys[pygame.K_w]:
            self.move_y = -self.speed
        if keys[pygame.K_s]:
            self.move_y = self.speed

        if keys[pygame.K_SPACE]:
            self.attack()

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

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

    def on_stage_complete(self):
        self.current_stage += 1
        if self.current_stage > self.max_state:
            self.max_state = self.current_stage
        print(f"{self.name} progressed to Stage {self.current_stage}")

    def __str__(self):
        return f'Player: {self.name}, MaxState: {self.max_state}, CurrentStage: {self.current_stage}, TimePlayed: {self.time_played}, EnemiesDefeated: {self.enemies_defeated}, ItemsCollected: {self.items_collected}'