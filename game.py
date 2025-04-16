import sys
import pygame
import random

from DungeonEscape.config import Config
from DungeonEscape.db.player_data import PlayerDB
from DungeonEscape.entities.player import Player
from DungeonEscape.entities.tile import Tile
from DungeonEscape.map.random_map_generator import RandomMapGenerator
from DungeonEscape.managers.enemy_manager import get_enemies_for_stage
from DungeonEscape.ui.hud import Hud
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
        self.last_game_surface = None
        self.running = False

        self.player = Player()
        self.map = None
        self.enemies = []
        self.items = []
        self.traps = []

        self.tile_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        # Wave System
        self.wave_number = 1
        self.total_waves = 3
        self.wave_enemies_remaining = 0

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
        self.enemy_group.empty()
        self.enemies.clear()

        tile_size = Tile.TILE_SIZE
        player_placed = False

        for y, row in enumerate(map_data):
            for x, tile_type in enumerate(row):
                tile = Tile(x, y, tile_type)
                self.tile_group.add(tile)

                if tile_type == 'player':
                    self.player.rect.topleft = (x * tile_size, y * tile_size)
                    self.player.move_x = 0
                    self.player.move_y = 0
                    self.player_group.add(self.player)
                    player_placed = True

        if not player_placed:
            print("[WARNING] Player not placed on map! Defaulting to (0,0)")
            self.player.rect.topleft = (0, 0)
            self.player_group.add(self.player)

    def find_available_enemy_positions(self):
        positions = []
        for tile in self.tile_group:
            if getattr(tile, 'tile_type', '') == 'floor':
                positions.append(tile.rect.topleft)
        random.shuffle(positions)
        return positions[:10]

    def start_stage_mode(self):
        self.load_stage(self.player.current_stage)

        #Wave
        self.wave_number = 1
        self.total_waves = min(3 + self.player.current_stage // 2, 10)

        def prepare_wave(wave):
            self.enemy_group.empty()
            self.enemies.clear()
            positions = self.find_available_enemy_positions()
            wave_enemies = get_enemies_for_stage(self.player.current_stage, positions, wave)
            for e in wave_enemies:
                e.enemy_group = self.enemies
                self.enemies.append(e)
                self.enemy_group.add(e)
            self.wave_enemies_remaining = len(wave_enemies)

        prepare_wave(self.wave_number)

        exit_rect = next((s.rect for s in self.tile_group if getattr(s, 'tile_type', '') == 'exit'), None)
        stage_running = True

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

            for enemy in self.enemy_group:
                enemy.update(dt, player=self.player)
                if not enemy.alive:
                    self.enemy_group.remove(enemy)
                    self.wave_enemies_remaining -= 1

            self.enemy_group.draw(self.screen)

            # Show HUD
            hud = Hud(self.screen, self.player, self.wave_number, self.total_waves)
            hud.update_wave_info(self.wave_number, self.total_waves)
            hud.draw()

            for tile in self.tile_group:
                if tile.tile_type in ["spike", "poison", "timed_spike"]:
                    trap_check_rect = self.player.rect.inflate(-20, -40)
                    if trap_check_rect.colliderect(tile.rect):
                        if tile.tile_type == "timed_spike" and not getattr(tile, 'active', True):
                            continue
                        self.player.trigger_trap(getattr(tile, 'damage', 10))
                        break

            if self.wave_enemies_remaining <= 0:
                if self.wave_number < self.total_waves:
                    self.wave_number += 1
                    prepare_wave(self.wave_number)
                else:
                    if exit_rect and self.player.rect.colliderect(exit_rect):
                        print("Stage complete!")
                        self.player.on_stage_complete()
                        PlayerDB().update_player(self.player)
                        self.load_stage(self.player.current_stage)
                        self.wave_number = 1
                        prepare_wave(self.wave_number)
                        continue

            if not self.player.alive:
                self.last_game_surface = self.screen.copy()
                self.menu.show_game_over_screen(self)
                return

            pygame.display.flip()

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