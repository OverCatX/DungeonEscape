import pygame

class Hud:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font(None, 32)
        self.hud_font = pygame.font.Font(None, 20)

    def draw(self):
        # Stage label
        stage_label = self.font.render(f"Stage {self.player.current_stage}", True, (255, 255, 255))
        stage_pos = (20, 20)
        self.screen.blit(stage_label, stage_pos)

        # Bar positions
        bar_x = stage_pos[0] + stage_label.get_width() + 30
        bar_y = stage_pos[1]
        bar_width = 100
        bar_height = 16
        spacing_y = 22

        # Health bar
        health_ratio = self.player.health / 100
        health_rect = pygame.Rect(bar_x, bar_y, bar_width * health_ratio, bar_height)
        pygame.draw.rect(self.screen, (200, 0, 0), health_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

        # Energy bar
        energy_ratio = self.player.energy / self.player.max_energy
        energy_rect = pygame.Rect(bar_x, bar_y + spacing_y, bar_width * energy_ratio, bar_height)
        pygame.draw.rect(self.screen, (0, 200, 0), energy_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y + spacing_y, bar_width, bar_height), 2)

        # HUD Text
        hp_text = self.hud_font.render(f"HP: {int(self.player.health)}", True, (255, 255, 255))
        en_text = self.hud_font.render(f"EN: {int(self.player.energy)}", True, (255, 255, 255))
        self.screen.blit(hp_text, (bar_x + bar_width + 10, bar_y))
        self.screen.blit(en_text, (bar_x + bar_width + 10, bar_y + spacing_y))