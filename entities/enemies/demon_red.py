from collections import deque
import pygame
import math
from DungeonEscape.entities.enemies.enemy import Enemy

class DemonRed(Enemy):
    def __init__(self, x=0, y=0):
        super().__init__(asset_folder='demon_red', x=x, y=y)
        self.health = 40
        self.speed = 1.2
        self.damage = 10
        self.attack_range = 40
        self.attack_cooldown = 1000  # ms
        self.last_attack_time = 0

    def update(self, dt, player=None):
        if not self.alive or player is None:
            return

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)

        if abs(dx) > abs(dy):
            self.direction = 'right' if dx > 0 else 'left'
        else:
            self.direction = 'down' if dy > 0 else 'up'

        hitbox = self.rect.inflate(-10, -10)
        if hitbox.colliderect(player.rect):
            self.move_x = 0
            self.move_y = 0
            now = pygame.time.get_ticks()
            if now - self.last_attack_time >= self.attack_cooldown:
                self.last_attack_time = now
                player.take_enemy_damage(self.damage)
                print(f"[DemonRed] Attacked player for {self.damage} damage")
        else:
            self.move_x = (dx / distance) * self.speed
            self.move_y = (dy / distance) * self.speed

        if hasattr(self, 'enemy_group'):
            future_rect = self.rect.copy()
            future_rect.x += self.move_x
            future_rect.y += self.move_y

            for other in self.enemy_group:
                if other != self and future_rect.colliderect(other.rect):
                    overlap_x = future_rect.centerx - other.rect.centerx
                    overlap_y = future_rect.centery - other.rect.centery
                    if abs(overlap_x) > abs(overlap_y):
                        self.move_x += 0.5 if overlap_x > 0 else -0.5
                    else:
                        self.move_y += 0.5 if overlap_y > 0 else -0.5
                    break

        super().update(dt)