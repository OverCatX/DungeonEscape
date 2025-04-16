import pygame
from DungeonEscape.entities.entity import Entity

class Enemy(Entity):
    def __init__(self, asset_folder, x=0, y=0):
        super().__init__(asset_folder=asset_folder, x=x, y=y)
        self.health = 30
        self.alive = True
        self.move_x = 0
        self.move_y = 0
        self.enemy_group = []

    def update(self, dt):
        self.rect.x += self.move_x
        self.rect.y += self.move_y
        super().update(dt)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        self.alive = False
        print(f"[Enemy] {self.__class__.__name__} died")
        self.kill()  # remove from sprite group