import pygame
import math
from entities.players.player import Player

class PlayerAssassin(Player):
    dagger_image = None

    def __init__(self, x=0, y=0, name="Assassin",character_type="assassin", **kwargs):
        super().__init__(asset_folder = 'characters/assassin', x=x, y=y, name=name, character_type=character_type, **kwargs)
        self.attack_range = 60
        self.max_health = 100
        self.damage = 40
        self.attack_direction = 'right'
        self.dagger_offset = 32
        self.attack_duration = 200

        if PlayerAssassin.dagger_image is None:
            try:
                PlayerAssassin.dagger_image = pygame.transform.scale(
                    pygame.image.load('assets/items/dagger.png').convert_alpha(), (32, 32))
                print("[Assassin] Dagger image loaded.")
            except Exception as e:
                print(f"[Assassin] Failed to load dagger image: {e}")
        if PlayerAssassin.dagger_image:
            print("[Debug] Dagger image size:", PlayerAssassin.dagger_image.get_size())
        else:
            print("[Debug] Dagger image is None")

    def attack_enemies(self, enemy_group):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time >= self.attack_cooldown:
            self.attack_direction = self.facing
            self.last_attack_time = now
            self.attack_start_time = now
            self.is_attacking = True
            self.attack_animation = True

            super().attack_enemies(enemy_group)

            dead_enemies = []
            for enemy in enemy_group:
                if self.in_attack_range(enemy) and enemy.alive:
                    enemy.take_damage(self.damage)
                    dx = enemy.rect.centerx - self.rect.centerx
                    dy = enemy.rect.centery - self.rect.centery
                    direction = pygame.math.Vector2(dx, dy)
                    if direction.length_squared() > 0:
                        direction.normalize_ip()
                        enemy.knockback += direction * 5
                    print(f"[PlayerAssassin] Attacked {enemy.__class__.__name__}")
                    if not enemy.alive:
                        self.enemies_defeated += 1
                        dead_enemies.append(enemy)
            return dead_enemies
        return []

    def in_attack_range(self, enemy):
        dx = enemy.rect.centerx - self.rect.centerx
        dy = enemy.rect.centery - self.rect.centery

        if abs(dx) < 10 and abs(dy) < 10:
            return True

        if self.attack_direction == 'right':
            return 0 <= dx <= self.attack_range and abs(dy) <= 30
        elif self.attack_direction == 'left':
            return -self.attack_range <= dx <= 0 and abs(dy) <= 30
        elif self.attack_direction == 'up':
            return -self.attack_range <= dy <= 0 and abs(dx) <= 30
        elif self.attack_direction == 'down':
            return 0 <= dy <= self.attack_range and abs(dx) <= 30

        return False

    def draw(self, surface):
        super().draw(surface)

        now = pygame.time.get_ticks()
        if self.is_attacking and now - self.attack_start_time <= self.attack_duration:
            if PlayerAssassin.dagger_image:
                dagger = PlayerAssassin.dagger_image
                dagger_rect = dagger.get_rect()
                elapsed = now - self.attack_start_time
                power = math.sin((elapsed / self.attack_duration) * math.pi)
                thrust = int(self.dagger_offset + power * 10)

                if self.attack_direction == 'right':
                    dagger_rotated = pygame.transform.rotate(dagger, 90)
                    dagger_rect.center = (self.rect.centerx + thrust, self.rect.centery)
                elif self.attack_direction == 'left':
                    dagger_rotated = pygame.transform.rotate(dagger, -90)
                    dagger_rect.center = (self.rect.centerx - thrust, self.rect.centery)
                elif self.attack_direction == 'up':
                    dagger_rotated = pygame.transform.rotate(dagger, 180)
                    dagger_rect.center = (self.rect.centerx, self.rect.centery - thrust)
                elif self.attack_direction == 'down':
                    dagger_rotated = dagger
                    dagger_rect.center = (self.rect.centerx, self.rect.centery + thrust)

                rotated_rect = dagger_rotated.get_rect(center=dagger_rect.center)
                surface.blit(dagger_rotated, rotated_rect)
        else:
            self.is_attacking = False
