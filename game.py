import pygame
from DungeonEscape.config import Config
from DungeonEscape.ui.menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Dungeon Escape V.1")
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.screen)
        self.game_data = {
            'state': 'home'
        }
        self.running = False
        self.player = None
        self.map = None
        self.enemies = []
        self.items = []
        self.traps = []

    def home_screen(self):
        result = self.menu.home_screen()
        if result == 'enter':
            self.game_data['state'] = 'start_game'
        elif result == 'exit':
            self.running = False

    def start_game(self):
        result = self.menu.start_game()
        print(result,self.game_data['state'])
        if result == 'back':
            self.game_data['state'] = 'home'
        elif result == 'exit':
            self.running = False
        else:
            print(result)

    def run(self):
        self.running = True
        while self.running:
            if self.game_data['state'] == 'home':
                self.home_screen()
            elif self.game_data['state'] == 'start_game':
                self.start_game()
            elif self.game_data['state'] == 'game':
                self.start_game()

game = Game()
game.run()