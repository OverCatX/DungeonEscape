import pygame

class Hud:
    def __init__(self, screen, player, wave_number=1, total_waves=1):
        self.screen = screen
        self.player = player
        self.wave_number = wave_number
        self.total_waves = total_waves
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 20)

    def draw(self):
        stage_label = self.font.render(f"Stage {self.player.current_stage}", True, (255, 255, 255))
        wave_label = self.font.render(f"Wave {self.wave_number}/{self.total_waves}", True, (200, 200, 255))

        stage_pos = (20, 20)
        wave_pos = (20, 50)

        self.screen.blit(stage_label, stage_pos)
        self.screen.blit(wave_label, wave_pos)

        # Bar positioning
        bar_x = 200
        bar_y = 20
        bar_width = 120
        bar_height = 16
        spacing_y = 22

        # --- Health bar ---
        health_ratio = self.player.health / 100
        health_rect = pygame.Rect(bar_x, bar_y, bar_width * health_ratio, bar_height)
        pygame.draw.rect(self.screen, (200, 0, 0), health_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

        # --- Energy bar ---
        energy_ratio = self.player.energy / self.player.max_energy
        energy_rect = pygame.Rect(bar_x, bar_y + spacing_y, bar_width * energy_ratio, bar_height)
        pygame.draw.rect(self.screen, (0, 200, 0), energy_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y + spacing_y, bar_width, bar_height), 2)

        # --- Text next to bars ---
        hp_text = self.small_font.render(f"HP: {int(self.player.health)}", True, (255, 255, 255))
        en_text = self.small_font.render(f"EN: {int(self.player.energy)}", True, (255, 255, 255))
        self.screen.blit(hp_text, (bar_x + bar_width + 10, bar_y))
        self.screen.blit(en_text, (bar_x + bar_width + 10, bar_y + spacing_y))

    def update_wave_info(self, wave_number, total_waves):
        self.wave_number = wave_number
        self.total_waves = total_waves