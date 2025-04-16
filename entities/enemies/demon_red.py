import math
import pygame
from entities.enemies.enemy import Enemy

class DemonRed(Enemy):
    def __init__(self, x=0, y=0):
        super().__init__(asset_folder='demon_red', x=x, y=y)
        self.health = 40
        self.speed = 1.2
        self.damage = 10
        self.attack_range = 40
        self.attack_cooldown = 1000
        self.last_attack_time = 0

        # Hurt flash effect
        self.hit_flash = False
        self.hit_flash_timer = 0
        self.hit_flash_duration = 400

    def update(self, dt, player=None):
        if not self.alive:
            return

        now = pygame.time.get_ticks()

        # Hurt flash effect
        if self.hit_flash:
            if now - self.hit_flash_timer >= self.hit_flash_duration:
                self.hit_flash = False
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(0 if (now // 100) % 2 == 0 else 255)
        else:
            self.image.set_alpha(255)

        # Reset movement
        self.move_x = 0
        self.move_y = 0

        if player:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)

            if distance > 0:
                self.move_x = (dx / distance) * self.speed
                self.move_y = (dy / distance) * self.speed

                # Face direction
                if abs(dx) > abs(dy):
                    self.direction = 'right' if dx > 0 else 'left'
                else:
                    self.direction = 'down' if dy > 0 else 'up'

                # Avoid overlapping other enemies
                if hasattr(self, 'enemy_group'):
                    for other in self.enemy_group:
                        if other is not self and other.alive:
                            if self.rect.colliderect(other.rect.inflate(-10, -10)):
                                overlap_x = self.rect.centerx - other.rect.centerx
                                overlap_y = self.rect.centery - other.rect.centery
                                if abs(overlap_x) > abs(overlap_y):
                                    self.move_x += 0.5 if overlap_x > 0 else -0.5
                                else:
                                    self.move_y += 0.5 if overlap_y > 0 else -0.5

            # Attack Player if close enough
            if distance <= self.attack_range:
                if now - self.last_attack_time >= self.attack_cooldown:
                    self.last_attack_time = now
                    player.take_enemy_damage(self.damage)
                    print(f"[DemonRed] attacked player for {self.damage} damage")

        super().update(dt)

    def take_damage(self, amount):
        self.health -= amount
        print(f"[DemonRed] took damage: {amount}, HP = {self.health}")
        self.hit_flash = True
        self.hit_flash_timer = pygame.time.get_ticks()

        if self.health <= 0:
            self.die()