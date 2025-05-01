import math
import random
import pygame


class DropItem(pygame.sprite.Sprite):
    images = {}

    @classmethod
    def load_images(cls):
        cls.images['health'] = pygame.transform.scale(
            pygame.image.load('assets/items/health.png').convert_alpha(), (32, 32))

    def __init__(self, x, y, item_type, player=None):
        super().__init__()
        self.item_type = item_type
        self.image = DropItem.images[item_type]
        self.rect = self.image.get_rect(center=(x, y))

        # Knockback away from player
        if player:
            dx = self.rect.centerx - player.rect.centerx
            dy = self.rect.centery - player.rect.centery
            angle = math.atan2(dy, dx)
        else:
            angle = random.uniform(0, 2 * math.pi)

        speed = random.uniform(250, 400)  # พุ่งแรงขึ้น
        self.velocity = [math.cos(angle) * speed, math.sin(angle) * speed]
        self.friction = 0.85

        # Delay before pickup allowed
        self.spawn_time = pygame.time.get_ticks()
        self.pickup_delay = 600  # ms

    def update(self, dt, player):
        self.rect.x += self.velocity[0] * dt
        self.rect.y += self.velocity[1] * dt
        self.velocity[0] *= self.friction
        self.velocity[1] *= self.friction

        now = pygame.time.get_ticks()
        if now - self.spawn_time < self.pickup_delay:
            return  # wait before pickup

        if player and self.rect.colliderect(player.rect):
            if self.item_type == 'health':
                player.health = min(player.health + 20, 100)
                print("[Item] Player picked up health")
            self.kill()