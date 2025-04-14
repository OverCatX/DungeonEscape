import sys

import pygame
from DungeonEscape.config import Config
from DungeonEscape.db.player_data import PlayerDB
from DungeonEscape.entities.player import Player
from DungeonEscape.ui.menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("Dungeon Escape V.1")
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.screen)
        self.game_data = {
            'state': 'home'
        }
        self.running = False

        # Sprites Player
        self.player = Player()
        self.map = None
        self.enemies = []
        self.items = []
        self.traps = []

        # Groups
        self.moving_sprites = pygame.sprite.Group()
        self.moving_sprites.add(self.player)

    def home_screen(self):
        result = self.menu.home_screen()
        if result == 'exit':
            self.running = False
        else:
            self.game_data['state'] = 'player_progress'
            self.player = PlayerDB().player_login(result)
            # print(self.player.name)

    def player_progress(self):
        result = self.menu.show_player_stats(self.player)
        if result == 'continue':
            self.game_data['state'] = 'on_game'
        elif result == 'back':
            self.game_data['state'] = 'home'

    def on_game(self):
        while self.running:
            dt = self.clock.tick(Config.FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill((255, 255, 255))
            self.moving_sprites.update(dt)
            self.moving_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(Config.FPS)
        pygame.quit()

    def run(self):
        self.running = True
        while self.running:
            if self.game_data['state'] == 'home':
                self.home_screen()
            elif self.game_data['state'] == 'player_progress':
                self.player_progress()
            elif self.game_data['state'] == 'on_game':
                self.on_game()
game = Game()
game.run()