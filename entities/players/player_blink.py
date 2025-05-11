import pygame
from entities.players.player import Player

class PlayerBlink(Player):
    def __init__(self, x=0, y=0, name="BlinkAssassin", character_type="blink", **kwargs):
        super().__init__(asset_folder='characters/blink', x=x, y=y, name=name, character_type=character_type, **kwargs)
        self.health = 60
        self.speed *= 1.5
        self.damage = 60
        self.max_health = 60

        # Dash System
        self.max_dash_stack = 2
        self.dash_stack = 2
        self.dash_cooldown = 300  # ms
        self.last_dash_refill = pygame.time.get_ticks()
        self.energy_per_dash = 15  # energy cost per dash

        # Warp Attack
        self.warp_range = 120
        self.attack_cooldown = 200  # faster blink attack
        self.attack_duration = 200

    def update(self, dt, tile_group=None):
        super().update(dt, tile_group=tile_group)

        # Refill dash stack
        now = pygame.time.get_ticks()
        if self.dash_stack < self.max_dash_stack:
            if now - self.last_dash_refill >= self.dash_cooldown:
                self.dash_stack += 1
                self.last_dash_refill = now

    def handle_dash(self):
        if self.dash_stack > 0 and not self.is_dashing and self.energy >= self.energy_per_dash:
            self.start_dash()
            self.dash_stack -= 1
            self.energy -= self.energy_per_dash
            self.last_dash_refill = pygame.time.get_ticks()
            print(f"[Blink] Dash used. Energy: {self.energy}/{self.max_energy}")

    def attack_enemies(self, enemy_group):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = now
            self.attack_start_time = now
            self.is_attacking = True
            self.attack_animation = True

            # warp behind nearest enemy in facing direction
            target = self.find_target(enemy_group)
            if target:
                self.warp_behind(target)
                target.take_damage(self.damage)

                # Heal on successful blink attack
                self.health = min(self.health + 20, self.max_health)
                print(f"[Blink] Healed 5 HP → {self.health}/{self.max_health}")

                if not target.alive:
                    self.enemies_defeated += 1
                print(f"[BlinkAssassin] Warp attacked {target.__class__.__name__}")
                return [target] if not target.alive else []
        return []

    def find_target(self, enemy_group):
        closest = None
        min_dist = float('inf')
        for enemy in enemy_group:
            if not enemy.alive:
                continue
            dx = enemy.rect.centerx - self.rect.centerx
            dy = enemy.rect.centery - self.rect.centery
            dist = (dx**2 + dy**2)**0.5
            if dist <= self.warp_range and self.in_facing(enemy):
                if dist < min_dist:
                    min_dist = dist
                    closest = enemy
        return closest

    def in_facing(self, enemy):
        if self.facing == 'right': return enemy.rect.centerx > self.rect.centerx
        if self.facing == 'left': return enemy.rect.centerx < self.rect.centerx
        if self.facing == 'up': return enemy.rect.centery < self.rect.centery
        if self.facing == 'down': return enemy.rect.centery > self.rect.centery
        return False

    def warp_behind(self, enemy):
        offset = 32
        if self.facing == 'right':
            self.rect.centerx = enemy.rect.centerx + offset
            self.rect.centery = enemy.rect.centery
        elif self.facing == 'left':
            self.rect.centerx = enemy.rect.centerx - offset
            self.rect.centery = enemy.rect.centery
        elif self.facing == 'up':
            self.rect.centery = enemy.rect.centery - offset
            self.rect.centerx = enemy.rect.centerx
        elif self.facing == 'down':
            self.rect.centery = enemy.rect.centery + offset
            self.rect.centerx = enemy.rect.centerx