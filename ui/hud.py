import pygame

class Hud:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font(None, 28)
        self.pause_button = pygame.Rect(screen.get_width() - 110, 20, 90, 30)
        self.is_paused = False

    def draw(self, wave_number=None, total_waves=None):
        spacing_x = 140
        top_y = 20

        # Stage
        stage_text = self.font.render(f"Stage {self.player.current_stage}", True, (255, 255, 255))
        self.screen.blit(stage_text, (20, top_y))

        # Wave
        if wave_number is not None and total_waves is not None:
            wave_text = self.font.render(f"Wave {wave_number}/{total_waves}", True, (255, 255, 255))
            self.screen.blit(wave_text, (20 + spacing_x, top_y))

        # Health Bar
        bar_x = 20 + spacing_x * 2
        bar_width = 100
        bar_height = 16

        health_ratio = self.player.health / 100
        health_rect = pygame.Rect(bar_x, top_y, bar_width * health_ratio, bar_height)
        pygame.draw.rect(self.screen, (200, 0, 0), health_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, top_y, bar_width, bar_height), 2)

        # Energy Bar
        energy_ratio = self.player.energy / self.player.max_energy
        energy_rect = pygame.Rect(bar_x, top_y + 20, bar_width * energy_ratio, bar_height)
        pygame.draw.rect(self.screen, (0, 200, 0), energy_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, top_y + 20, bar_width, bar_height), 2)

        # HP / EN Labels
        small_font = pygame.font.Font(None, 20)
        hp_text = small_font.render(f"HP: {int(self.player.health)}", True, (255, 255, 255))
        en_text = small_font.render(f"EN: {int(self.player.energy)}", True, (255, 255, 255))
        self.screen.blit(hp_text, (bar_x + bar_width + 10, top_y))
        self.screen.blit(en_text, (bar_x + bar_width + 10, top_y + 20))

        # Pause button (ขวาบน)
        pygame.draw.rect(self.screen, (50, 50, 50), self.pause_button)
        pygame.draw.rect(self.screen, (255, 255, 255), self.pause_button, 2)
        text = self.font.render("Pause", True, (255, 255, 255))
        self.screen.blit(text, (self.pause_button.centerx - text.get_width() // 2,
                                self.pause_button.centery - text.get_height() // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.pause_button.collidepoint(event.pos):
            self.is_paused = True

    def show_pause_menu(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 36)

        pause_label = font.render("Game Paused", True, (255, 255, 255))
        self.screen.blit(pause_label, (self.screen.get_width() // 2 - pause_label.get_width() // 2, 200))

        continue_btn = pygame.Rect(self.screen.get_width() // 2 - 100, 300, 200, 50)
        exit_btn = pygame.Rect(self.screen.get_width() // 2 - 100, 380, 200, 50)

        pygame.draw.rect(self.screen, (80, 80, 80), continue_btn)
        pygame.draw.rect(self.screen, (200, 0, 0), exit_btn)

        pygame.draw.rect(self.screen, (255, 255, 255), continue_btn, 2)
        pygame.draw.rect(self.screen, (255, 255, 255), exit_btn, 2)

        self.screen.blit(small_font.render("Continue", True, (255, 255, 255)), (continue_btn.centerx - 50, continue_btn.centery - 15))
        self.screen.blit(small_font.render("Exit to Menu", True, (255, 255, 255)), (exit_btn.centerx - 70, exit_btn.centery - 15))

        return continue_btn, exit_btn