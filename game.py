import pygame.display

from DungeonEscape.config import Config


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = False

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()