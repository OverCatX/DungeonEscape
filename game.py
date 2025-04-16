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
        self.last_game_surface = self.screen.copy()
        self.running = False

        self.player = Player()
        self.map = None
        self.enemies = []
        self.items = []
        self.traps = []

        self.tile_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.wave_number = 1
        self.total_waves = 3
        self.wave_enemies_remaining = 0
        self.wave_popup_text = None
        self.wave_popup_timer = 0
        self.wave_popup_duration = 1500

        self.clear_popup_shown = False

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
            self.wave_popup_text = f"Wave {wave} Incoming!"
            self.wave_popup_timer = pygame.time.get_ticks()

        prepare_wave(self.wave_number)

        exit_rect = next((s.rect for s in self.tile_group if getattr(s, 'tile_type', '') == 'exit'), None)
        stage_running = True

        hud = Hud(self.screen, self.player)

        while stage_running:
            dt = self.clock.tick(Config.FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                hud.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    dead_enemies = self.player.attack_enemies(self.enemy_group)
                    for enemy in dead_enemies:
                        if enemy in self.enemy_group:
                            self.enemy_group.remove(enemy)
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                        self.wave_enemies_remaining = max(0, self.wave_enemies_remaining - 1)

            if hud.is_paused:
                self.last_game_surface = self.screen.copy()
                while hud.is_paused:
                    cont_btn, exit_btn = hud.show_pause_menu(self.last_game_surface)
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if cont_btn.collidepoint(event.pos):
                                hud.is_paused = False
                            elif exit_btn.collidepoint(event.pos):
                                self.game_data['state'] = 'home'
                                return

            self.screen.fill((20, 20, 20))
            self.tile_group.update(dt)
            self.tile_group.draw(self.screen)

            self.player.update(dt, tile_group=self.tile_group)
            self.player_group.update(dt)
            self.player_group.draw(self.screen)

            for enemy in list(self.enemy_group):
                enemy.update(dt, player=self.player)
                if not enemy.alive:
                    self.enemy_group.remove(enemy)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    self.wave_enemies_remaining = max(0, self.wave_enemies_remaining - 1)

            self.enemy_group.draw(self.screen)

            hud.draw(self.wave_number, self.total_waves, self.wave_enemies_remaining)

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
                    self.clear_popup_shown = True

            if exit_rect and self.player.rect.colliderect(exit_rect):
                if self.wave_number < self.total_waves or self.wave_enemies_remaining > 0:
                    warning_font = pygame.font.Font(None, 30)
                    msg = warning_font.render("Defeat all enemies to proceed!", True, (255, 100, 100))
                    self.screen.blit(msg, (self.screen.get_width() // 2 - msg.get_width() // 2, 100))
                else:
                    print("Stage complete!")
                    self.fade_out()
                    self.on_stage_complete()
                    PlayerDB().update_player(self.player)
                    self.load_stage(self.player.current_stage)
                    self.wave_number = 1
                    self.clear_popup_shown = False
                    prepare_wave(self.wave_number)

            if not self.player.alive:
                self.last_game_surface = self.screen.copy()
                self.menu.show_game_over_screen(self)
                return


            # --- Show wave popup message ---
            now = pygame.time.get_ticks()
            if self.wave_popup_text and now - self.wave_popup_timer < self.wave_popup_duration:
                font = pygame.font.Font(None, 42)
                text = font.render(self.wave_popup_text, True, (255, 255, 0))
                self.screen.blit(text, (
                    self.screen.get_width() // 2 - text.get_width() // 2,
                    60
                ))
            else:
                self.wave_popup_text = None

            if self.clear_popup_shown:
                font = pygame.font.Font(None, 30)
                msg = font.render("All waves cleared! Head to the exit", True, (0, 255, 100))
                self.screen.blit(msg, (
                    self.screen.get_width() // 2 - msg.get_width() // 2,
                    100
                ))

            pygame.display.flip()

    def fade_out(self, duration=1000):
        fade_surface = pygame.Surface(self.screen.get_size())
        fade_surface.fill((0, 0, 0))
        clock = pygame.time.Clock()
        alpha = 0
        start_time = pygame.time.get_ticks()

        while alpha < 255:
            now = pygame.time.get_ticks()
            elapsed = now - start_time
            alpha = min(255, int((elapsed / duration) * 255))
            fade_surface.set_alpha(alpha)

            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            clock.tick(60)

    def on_stage_complete(self):
        self.player.current_stage += 1
        if self.player.current_stage > self.player.max_state:
            self.player.max_state = self.player.current_stage
            #Max Health when changed state
            self.player.health = 100
        print(f"[Player] Stage completed. New stage: {self.player.current_stage}")

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