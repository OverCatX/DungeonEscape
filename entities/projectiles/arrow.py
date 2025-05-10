import pygame
import math

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed, damage):
        super().__init__()
        self.image = pygame.image.load("assets/items/arrow.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect(center=(x, y))

        self.direction = direction
        self.speed = speed
        self.damage = damage

        angle_map = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0),
            'up_left': (-1, -1),
            'up_right': (1, -1),
            'down_left': (-1, 1),
            'down_right': (1, 1)
        }

        dx, dy = angle_map.get(direction, (0, 0))
        length = math.hypot(dx, dy) or 1
        self.velocity = (dx / length * speed, dy / length * speed)

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # out frame let kill
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()

    def deal_damage(self, enemy):
        enemy.take_damage(self.damage)
        dx = enemy.rect.centerx - self.rect.centerx
        dy = enemy.rect.centery - self.rect.centery
        direction = pygame.math.Vector2(dx, dy).normalize()
        enemy.knockback += direction * 6
        self.kill()