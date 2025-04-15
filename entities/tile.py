import random
from random import randrange

import pygame
from os.path import join

class Tile(pygame.sprite.Sprite):
    TILE_SIZE = 64
    tile_images = {}

    @staticmethod
    def load_images():
        base = join("assets", "tiles")
        def load(name):
            return pygame.transform.scale(
                pygame.image.load(join(base, f"{name}.png")).convert_alpha(),
                (Tile.TILE_SIZE, Tile.TILE_SIZE)
            )

        Tile.tile_images['floor'] = load('floor')
        Tile.tile_images['wall'] = load('wall')
        Tile.tile_images['exit'] = load('exit')
        Tile.tile_images['trap'] = load('trap')
        Tile.tile_images['spike'] = load('spike')
        Tile.tile_images['poison'] = load('poison')
        Tile.tile_images['timed_spike'] = load('spike')  # reuse spike img

    def __init__(self, x, y, tile_type):
        super().__init__()
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.image = Tile.tile_images.get(tile_type, Tile.tile_images['floor'])
        self.blocked = False
        self.rect = pygame.Rect(x * Tile.TILE_SIZE, y * Tile.TILE_SIZE, Tile.TILE_SIZE, Tile.TILE_SIZE)

        if tile_type == 'wall':
            self.blocked = True
        elif tile_type == 'spike':
            self.damage = random.randint(5,10)
        elif tile_type == 'poison':
            self.damage = random.randint(5,10)
        elif tile_type == 'timed_spike':
            self.damage = 15
            self.timer = 0
            self.cycle_time = 1000
            self.active = True

    def update(self, dt):
        if self.tile_type == 'timed_spike':
            self.timer += dt * 1000
            if self.timer >= self.cycle_time:
                self.timer = 0
                self.active = not self.active
            self.image = Tile.tile_images['spike'] if self.active else Tile.tile_images['floor']
