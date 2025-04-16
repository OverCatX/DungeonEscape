import pygame

class Hud:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font(None, 28)
        self.pause_button = pygame.Rect(screen.get_width() - 110, 20, 90, 30)
        self.is_paused = False

    def draw(self, wave_number=None, total_waves=None, enemies_remaining=None):
        bar_x = 20
        bar_y = 20
        bar_width = 100
        bar_height = 16
        spacing_y = 22

        # Health
        health_ratio = self.player.health / 100
        health_rect = pygame.Rect(bar_x, bar_y, bar_width * health_ratio, bar_height)
        pygame.draw.rect(self.screen, (200, 0, 0), health_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

        # Energy
        energy_ratio = self.player.energy / self.player.max_energy
        energy_rect = pygame.Rect(bar_x, bar_y + spacing_y, bar_width * energy_ratio, bar_height)
        pygame.draw.rect(self.screen, (0, 200, 0), energy_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y + spacing_y, bar_width, bar_height), 2)

        # Labels
        small_font = pygame.font.Font(None, 20)
        hp_text = small_font.render(f"HP: {int(self.player.health)}", True, (255, 255, 255))
        en_text = small_font.render(f"EN: {int(self.player.energy)}", True, (255, 255, 255))
        self.screen.blit(hp_text, (bar_x + bar_width + 10, bar_y))
        self.screen.blit(en_text, (bar_x + bar_width + 10, bar_y + spacing_y))

        # Stage, Wave, Enemy Left
        y_offset = bar_y + spacing_y * 2 + 10
        stage_text = self.font.render(f"Stage {self.player.current_stage}", True, (255, 255, 255))
        self.screen.blit(stage_text, (bar_x, y_offset))

        if wave_number is not None and total_waves is not None:
            wave_text = self.font.render(f"Wave {wave_number}/{total_waves}", True, (255, 255, 255))
            self.screen.blit(wave_text, (bar_x, y_offset + spacing_y))

        if enemies_remaining is not None:
            enemy_text = self.font.render(f"Enemies Left: {enemies_remaining}", True, (255, 255, 255))
            self.screen.blit(enemy_text, (bar_x, y_offset + spacing_y * 2))

        # Pause button
        pygame.draw.rect(self.screen, (50, 50, 50), self.pause_button)
        pygame.draw.rect(self.screen, (255, 255, 255), self.pause_button, 2)
        text = self.font.render("Pause", True, (255, 255, 255))
        self.screen.blit(text, (self.pause_button.centerx - text.get_width() // 2,
                                self.pause_button.centery - text.get_height() // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.pause_button.collidepoint(event.pos):
            self.is_paused = True

    def show_pause_menu(self, background=None):
        if background:
            self.screen.blit(background, (0, 0))  # แสดงพื้นหลังเดิม

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 36)

        # Title
        pause_label = font.render("Game Paused", True, (255, 255, 255))
        self.screen.blit(pause_label, (
            self.screen.get_width() // 2 - pause_label.get_width() // 2, 200))

        # Buttons
        continue_btn = pygame.Rect(0, 0, 220, 55)
        exit_btn = pygame.Rect(0, 0, 220, 55)
        continue_btn.center = (self.screen.get_width() // 2, 300)
        exit_btn.center = (self.screen.get_width() // 2, 380)

        mouse_pos = pygame.mouse.get_pos()

        # Hover สี
        continue_color = (100, 100, 100) if continue_btn.collidepoint(mouse_pos) else (80, 80, 80)
        exit_color = (220, 0, 0) if exit_btn.collidepoint(mouse_pos) else (200, 0, 0)

        # Draw Rects
        pygame.draw.rect(self.screen, continue_color, continue_btn)
        pygame.draw.rect(self.screen, exit_color, exit_btn)
        pygame.draw.rect(self.screen, (255, 255, 255), continue_btn, 2)
        pygame.draw.rect(self.screen, (255, 255, 255), exit_btn, 2)

        # Text
        continue_text = small_font.render("Continue", True, (255, 255, 255))
        exit_text = small_font.render("Exit to Menu", True, (255, 255, 255))
        self.screen.blit(continue_text, (
            continue_btn.centerx - continue_text.get_width() // 2,
            continue_btn.centery - continue_text.get_height() // 2))
        self.screen.blit(exit_text, (
            exit_btn.centerx - exit_text.get_width() // 2,
            exit_btn.centery - exit_text.get_height() // 2))

        return continue_btn, exit_btn