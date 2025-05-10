import pygame
from entities.entity import Entity

class Enemy(Entity):
    def __init__(self, asset_folder, x=0, y=0):
        super().__init__(asset_folder=asset_folder, x=x, y=y)
        self.health = 30
        self.alive = True
        self.move_x = 0
        self.move_y = 0
        self.enemy_group = []
        self.knockback = pygame.math.Vector2(0, 0)

    def update(self, dt):
        velocity = pygame.Vector2(self.move_x, self.move_y)
        if self.knockback.length() > 0.5:
            velocity = self.knockback
            self.knockback *= 0.85
        self.rect.x += velocity.x
        self.rect.y += velocity.y
        super().update(dt)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        self.alive = False
        print(f"[Enemy] {self.__class__.__name__} died", self.alive)
        self.kill()  # remove from sprite group