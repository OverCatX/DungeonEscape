# DungeonEscape/game.py
import sys
import pygame
from DungeonEscape.config import Config
from DungeonEscape.db.player_data import PlayerDB
from DungeonEscape.entities.player import Player
from DungeonEscape.entities.tile import Tile
from DungeonEscape.map.random_map_generator import RandomMapGenerator
from DungeonEscape.ui.menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        pygame.display.set_caption("Dungeon Escape V.1")

        Tile.load_images()

        self.clock = pygame.time.Clock()
        self.menu = Menu(self.screen)
        self.game_data = {
            'state': 'home',
            'mode': None
        }
        self.running = False

        self.player = Player()
        self.map = None
        self.enemies = []
        self.items = []
        self.traps = []

        self.tile_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()

    def home_screen(self):
        result = self.menu.home_screen()
        if result == 'exit':
            self.running = False
        else:
            self.game_data['state'] = 'player_progress'
            self.player = PlayerDB().player_login(result)

    def player_progress(self):
        result = self.menu.show_player_stats(self.player)
        if result == 'continue':
            self.game_data['state'] = 'game_mode_selection'
        elif result == 'back':
            self.game_data['state'] = 'home'

    def game_mode_selection(self):
        selected_mode = self.menu.game_selection_screen()
        if selected_mode == "back":
            self.game_data['state'] = 'player_progress'
        elif selected_mode:
            self.game_data['mode'] = selected_mode
            self.game_data['state'] = 'on_game'

    def on_game(self):
        print(f"Starting game in mode: {self.game_data['mode']}")

        if self.game_data['mode'] == 'Stage Mode':
            self.start_stage_mode()
        elif self.game_data['mode'] == 'Hardcore Endless':
            pass

    def load_stage(self, stage_number):
        tile_w = self.screen.get_width() // Tile.TILE_SIZE
        tile_h = self.screen.get_height() // Tile.TILE_SIZE
        generator = RandomMapGenerator(tile_w, tile_h)
        map_data = generator.generate()

        self.tile_group.empty()
        self.player_group.empty()
        self.enemies.clear()

        tile_size = Tile.TILE_SIZE
        player_placed = False

        for y, row in enumerate(map_data):
            for x, val in enumerate(row):
                if val == 1:
                    tile_type = 'wall'
                elif val == 2:
                    tile_type = 'trap'
                elif val == 5:
                    tile_type = 'exit'
                else:
                    tile_type = 'floor'

                tile = Tile(x, y, tile_type)
                self.tile_group.add(tile)

                if val == 4:
                    self.player.rect.topleft = (x * tile_size, y * tile_size)
                    self.player.move_x = 0
                    self.player.move_y = 0
                    self.player_group.add(self.player)
                    player_placed = True

        if not player_placed:
            print("[WARNING] Player not placed on map! Defaulting to (0,0)")
            self.player.rect.topleft = (0, 0)
            self.player_group.add(self.player)

    def start_stage_mode(self):
        self.load_stage(self.player.current_stage)
        stage_running = True

        exit_rect = None
        for sprite in self.tile_group:
            if hasattr(sprite, 'tile_type') and sprite.tile_type == 'exit':
                exit_rect = sprite.rect
                break

        while stage_running:
            dt = self.clock.tick(Config.FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((20, 20, 20))

            self.tile_group.update(dt)
            self.tile_group.draw(self.screen)

            self.player.update(dt, tile_group=self.tile_group)
            self.player_group.update(dt)
            self.player_group.draw(self.screen)

            # --- Stage Label + HUD ---
            font = pygame.font.Font(None, 32)
            stage_label = font.render(f"Stage {self.player.current_stage}", True, (255, 255, 255))
            stage_pos = (20, 20)
            self.screen.blit(stage_label, stage_pos)

            bar_x = stage_pos[0] + stage_label.get_width() + 30
            bar_y = stage_pos[1]
            bar_width = 100
            bar_height = 16
            spacing_y = 22

            health_ratio = self.player.health / 100
            health_rect = pygame.Rect(bar_x, bar_y, bar_width * health_ratio, bar_height)
            pygame.draw.rect(self.screen, (200, 0, 0), health_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

            energy_ratio = self.player.energy / self.player.max_energy
            energy_rect = pygame.Rect(bar_x, bar_y + spacing_y, bar_width * energy_ratio, bar_height)
            pygame.draw.rect(self.screen, (0, 200, 0), energy_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y + spacing_y, bar_width, bar_height), 2)

            hud_font = pygame.font.Font(None, 20)
            hp_text = hud_font.render(f"HP: {int(self.player.health)}", True, (255, 255, 255))
            en_text = hud_font.render(f"EN: {int(self.player.energy)}", True, (255, 255, 255))
            self.screen.blit(hp_text, (bar_x + bar_width + 10, bar_y))
            self.screen.blit(en_text, (bar_x + bar_width + 10, bar_y + spacing_y))

            # --- Trap check ---
            for tile in self.tile_group:
                if tile.tile_type == "trap":
                    trap_check_rect = self.player.rect.inflate(-20, -40)
                    if trap_check_rect.colliderect(tile.rect):
                        self.player.trigger_trap()
                        break

            pygame.display.flip()

            if exit_rect and self.player.rect.colliderect(exit_rect):
                print("Player reached exit!")
                self.player.on_stage_complete()
                PlayerDB().update_player(self.player)
                self.load_stage(self.player.current_stage)
                for sprite in self.tile_group:
                    if hasattr(sprite, 'tile_type') and sprite.tile_type == 'exit':
                        exit_rect = sprite.rect
                        break

    def run(self):
        self.running = True
        while self.running:
            if self.game_data['state'] == 'home':
                self.home_screen()
            elif self.game_data['state'] == 'player_progress':
                self.player_progress()
            elif self.game_data['state'] == 'game_mode_selection':
                self.game_mode_selection()
            elif self.game_data['state'] == 'on_game':
                self.on_game()

game = Game()
game.run()