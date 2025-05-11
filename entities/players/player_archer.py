import pygame
from entities.players.player import Player
from entities.projectiles.arrow import Arrow

class PlayerArcher(Player):
    arrow_image = None

    def __init__(self, x=0, y=0, name="Archer", character_type="Archer", **kwargs):
        super().__init__(asset_folder='characters/archer', x=x, y=y, name=name, character_type=character_type, **kwargs)
        self.attack_range = 60
        self.attack_cooldown = 150  # cooldown per shot during burst
        self.damage = 14
        self.speed = 3
        self.attack_direction = 'right'
        self.attack_duration = 200
        self.projectiles = pygame.sprite.Group()
        self.arrow_speed = 7
        self.health = 120
        self.max_health = 120
        # Burst Mode
        self.burst_limit = 3
        self.burst_count = 0
        self.burst_reset_time = 1000  # ms cooldown after full burst
        self.last_burst_time = 0

        if PlayerArcher.arrow_image is None:
            try:
                PlayerArcher.arrow_image = pygame.transform.scale(
                    pygame.image.load('assets/items/arrow.png').convert_alpha(), (16, 16))
                print("[Archer] Arrow image loaded.")
            except Exception as e:
                print(f"[Archer] Failed to load arrow image: {e}")

    def attack_enemies(self, enemy_group):
        now = pygame.time.get_ticks()

        # If reached burst limit, check for cooldown reset
        if self.burst_count >= self.burst_limit:
            if now - self.last_burst_time >= self.burst_reset_time:
                self.burst_count = 0
            else:
                return []  # still cooling down

        if now - self.last_attack_time >= self.attack_cooldown:
            self.attack_direction = self.facing
            self.last_attack_time = now
            self.attack_start_time = now
            self.is_attacking = True
            self.attack_animation = True
            self.burst_count += 1

            if self.burst_count == self.burst_limit:
                self.last_burst_time = now

            offset_map = {
                'right': [(0, -30), (0, 0), (0, 30)],
                'left':  [(0, -30), (0, 0), (0, 30)],
                'up':    [(-30, 0), (0, 0), (30, 0)],
                'down':  [(-30, 0), (0, 0), (30, 0)],
            }

            for dx, dy in offset_map.get(self.facing, [(0, 0)]):
                arrow = Arrow(self.rect.centerx + dx, self.rect.centery + dy, self.facing, self.arrow_speed, self.damage)
                self.projectiles.add(arrow)
                print(f"[Archer] Shot arrow to {self.facing} from offset ({dx},{dy})")

            return []
        return []

    def update(self, dt, tile_group=None):
        super().update(dt, tile_group=tile_group)
        self.projectiles.update()

    def draw(self, surface):
        super().draw(surface)
        self.projectiles.draw(surface)