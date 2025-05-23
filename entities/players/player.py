import pygame
from random import randint
from entities.entity import Entity

class Player(Entity):
    def __init__(self, x=0, y=0, health=100, armor=0, name="Player", character_type='assassin',
                 time_played=0, enemies_defeated=0, items_collected=0, max_state=1,
                 current_stage=1, asset_folder='player'):
        super().__init__(asset_folder=asset_folder, x=x, y=y)
        self.name = name
        self.health = health
        self.max_health = 100
        self.armor = armor
        self.character_type = character_type
        self.setup_stats_by_type()
        self.current_stage = current_stage
        self.alive = True
        self.facing = 'down'
        self.knockback = pygame.math.Vector2(0, 0)

        # Speed
        self.speed = 2
        self.normal_speed = 2
        self.dash_speed = 3

        # Trap system
        self.trap_cooldown = 1000
        self.last_trap_hit_time = 0

        # Enemy damage cooldown
        self.enemy_cooldown = 300
        self.last_enemy_hit_time = 0

        # Attack system
        self.attack_cooldown = 100
        self.last_attack_time = 0
        self.attack_duration = 100
        self.attack_start_time = 0
        self.is_attacking = False

        # Energy system
        self.max_energy = 100
        self.energy = 100
        self.energy_decrease_rate = 30
        self.energy_recover_rate = 3

        # Flash on hurt
        self.hit_flash = False
        self.hit_flash_timer = 0
        self.hit_flash_duration = 500

        # Player Stats
        self.time_played = 0
        self.enemies_defeated = 0
        self.max_state = max_state
        self.traps_triggered = 0
        self.distance_traveled = 0.0
        self.survived = 1
        self.dash_used = 0
        self.was_dashing = False

    def setup_stats_by_type(self):
        if self.character_type == 'assassin':
            self.health = 200
            self.damage = 15
            self.speed = 2
        elif self.character_type == 'archer':
            self.health = 100
            self.damage = 10
            self.speed = 3
        elif self.character_type == 'blink':
            self.health = 60
            self.damage = 10
            self.speed = 4

    def update(self, dt, tile_group=None, enemy_group=None):
        now = pygame.time.get_ticks()
        self.time_played += dt

        old_x, old_y = self.rect.x, self.rect.y

        # Energy
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if self.energy > 0:
                self.energy -= self.energy_decrease_rate * dt
                self.energy = max(0, self.energy)
        else:
            self.energy += self.energy_recover_rate * dt
            self.energy = min(self.max_energy, self.energy)

        #Walkable attack
        self.handle_input()

        # ชน tile
        if tile_group:
            self.handle_tile_collision(tile_group)

        # attack without cooldown
        if keys[pygame.K_SPACE] and enemy_group:
            if now - self.last_attack_time >= self.attack_cooldown:
                self.attack_enemies(enemy_group)

        # reset animation attack
        if self.is_attacking and now - self.attack_start_time >= self.attack_duration:
            self.is_attacking = False
            self.attack_animation = False

        # update animation sprite
        super().update(dt)

        # Travel Distance (Stat)
        dx = abs(self.rect.x - old_x)
        dy = abs(self.rect.y - old_y)
        self.distance_traveled += dx + dy

        # Flash effect when hit
        if self.hit_flash:
            elapsed = now - self.hit_flash_timer
            if elapsed >= self.hit_flash_duration:
                self.hit_flash = False
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(0 if (elapsed // 100) % 2 == 0 else 255)
        else:
            self.image.set_alpha(255)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.move_x = 0
        self.move_y = 0

        is_dashing = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        can_dash = self.energy > 0

        #Detect dash start (Stat)
        if is_dashing and can_dash and not self.was_dashing:
            self.dash_used += 1
            print(f"[Stat] Dash used: {self.dash_used}")
        self.was_dashing = is_dashing and can_dash

        self.speed = self.dash_speed if is_dashing and can_dash else self.normal_speed

        if keys[pygame.K_a]:
            self.move_x = -self.speed
            self.facing = 'left'
        elif keys[pygame.K_d]:
            self.move_x = self.speed
            self.facing = 'right'
        if keys[pygame.K_w]:
            self.move_y = -self.speed
            self.facing = 'up'
        elif keys[pygame.K_s]:
            self.move_y = self.speed
            self.facing = 'down'

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def handle_tile_collision(self, tiles):
        self.rect.x += self.move_x
        for tile in tiles:
            if tile.blocked and self.rect.colliderect(tile.rect):
                if self.move_x > 0:
                    self.rect.right = tile.rect.left
                elif self.move_x < 0:
                    self.rect.left = tile.rect.right

        self.rect.y += self.move_y
        for tile in tiles:
            if tile.blocked and self.rect.colliderect(tile.rect):
                if self.move_y > 0:
                    self.rect.bottom = tile.rect.top
                elif self.move_y < 0:
                    self.rect.top = tile.rect.bottom

    def attack_enemies(self, enemy_group):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time >= self.attack_cooldown:
            self.attack()
            self.last_attack_time = now
            self.attack_start_time = now
            self.is_attacking = True
            dead_enemies = []
            for enemy in enemy_group:
                if self.rect.colliderect(enemy.rect.inflate(-20, -20)) and enemy.alive:
                    enemy.take_damage(15)
                    print(f"[Player] Attacked {enemy.__class__.__name__}")
                    if not enemy.alive:
                        self.enemies_defeated += 1
                        dead_enemies.append(enemy)
            return dead_enemies
        return []

    def take_trap_damage(self, amount):
        now = pygame.time.get_ticks()
        if now - self.last_trap_hit_time >= self.trap_cooldown:
            self.health -= amount
            self.last_trap_hit_time = now
            self.hit_flash = True
            self.hit_flash_timer = now
            self.traps_triggered += 1
            print(self.traps_triggered)
            print(f"[Trap] {self.name} took damage: {amount}, HP = {self.health}")
            if self.health <= 0:
                self.die()

    def take_enemy_damage(self, amount, source):
        now = pygame.time.get_ticks()
        if now - self.last_enemy_hit_time >= self.enemy_cooldown:
            self.health -= amount
            self.last_enemy_hit_time = now
            self.hit_flash = True
            self.hit_flash_timer = now
            print(f"[Enemy] {self.name} took damage: {amount}, HP = {self.health}")
            if self.health <= 0:
                self.die()

    def trigger_trap(self, damage):
        self.take_trap_damage(randint(3, damage))

    def die(self):
        print(f"{self.name} has died.")
        self.alive = False

    def reset_stats(self):
        self.time_played = 0
        self.enemies_defeated = 0
        self.traps_triggered = 0
        self.dash_used = 0
        self.distance_traveled = 0
        self.survived = 0

    def __str__(self):
        return (f'Player: {self.name}, State: {self.current_stage}, MaxState: {self.max_state}, '
                f'TimePlayed: {self.time_played}, EnemiesDefeated: {self.enemies_defeated}, '
                f'Dash: {self.dash_used}, Distance: {self.distance_traveled}')