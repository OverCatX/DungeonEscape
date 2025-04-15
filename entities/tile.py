# DungeonEscape/entities/tile.py
import pygame
import os

class Tile(pygame.sprite.Sprite):
    TILE_SIZE = 64
    tile_images = {}

    @staticmethod
    def load_images():
        if Tile.tile_images:
            return

        Tile.tile_images = {
            "floor": pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "tiles", "floor_1.png")).convert_alpha(),
                (Tile.TILE_SIZE, Tile.TILE_SIZE)
            ),
            "wall": pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "tiles", "wall_1.png")).convert_alpha(),
                (Tile.TILE_SIZE, Tile.TILE_SIZE)
            ),
            "trap": pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "tiles", "trap_1.png")).convert_alpha(),
                (Tile.TILE_SIZE, Tile.TILE_SIZE)
            ),
            "exit": pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "tiles", "exit_1.png")).convert_alpha(),
                (Tile.TILE_SIZE, Tile.TILE_SIZE)
            )
        }

    def __init__(self, x, y, tile_type):
        super().__init__()

        self.image = Tile.tile_images.get(tile_type)
        if self.image is None:
            print(f"[Tile Warning] Unknown tile type: {tile_type}, fallback to 'floor'")
            self.image = Tile.tile_images['floor']

        self.rect = self.image.get_rect(topleft=(x * Tile.TILE_SIZE, y * Tile.TILE_SIZE))
        self.tile_type = tile_type
        self.blocked = tile_type == "wall"
