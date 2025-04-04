import sys

import pygame
from DungeonEscape.config import Config

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.color = (255, 255, 255)
        self.player_name = ""
        self.input_box = pygame.Rect(200, 200, 400, 40)
        self.enter_button = pygame.Rect(200, 280, 400, 40)
        self.start_button = pygame.Rect(200, 280, 400, 40)
        self.back_button = pygame.Rect(200, 340, 400, 40)
        self.exit_button = pygame.Rect(200, 340, 400, 40)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color_rect = self.color_inactive
        self.active = False

    def home_screen(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.screen.fill(self.color)
            self.draw_home_buttons()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.enter_button.collidepoint(event.pos):
                        return 'enter'
                    elif self.exit_button.collidepoint(event.pos):
                        running = False
                        return 'exit'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            pygame.display.flip()
            clock.tick(30)

    def start_game(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.screen.fill(self.color)
            self.draw_start_game_buttons()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos) and self.player_name != "":
                        running = False
                        return self.player_name
                    elif self.back_button.collidepoint(event.pos):
                        running = False
                        return 'back'
                elif event.type == pygame.KEYDOWN:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        elif event.key == pygame.K_RETURN and self.player_name.strip():
                            self.player_name = "home"
                        elif len(self.player_name) < 15:
                            self.player_name += event.unicode

            self.draw_input_box()
            pygame.display.flip()
            clock.tick(60)

    def draw_home_buttons(self):
        # Enter Game
        pygame.draw.rect(self.screen, Config.COLORS['green'], self.enter_button)
        enter_text = self.font.render("Enter Game", True, (0, 0, 0))
        self.screen.blit(enter_text, (self.enter_button.x + self.enter_button.width // 2 - enter_text.get_width() // 2,
                                      self.enter_button.y + self.enter_button.height // 2 - enter_text.get_height() // 2))
        # Exit
        pygame.draw.rect(self.screen, Config.COLORS['red'], self.exit_button)
        exit_text = self.font.render("Exit", True, (0, 0, 0))
        self.screen.blit(exit_text, (self.exit_button.x + self.exit_button.width // 2 - exit_text.get_width() // 2,
                                     self.exit_button.y + self.exit_button.height // 2 - exit_text.get_height() // 2))

    def draw_start_game_buttons(self):
        self.draw_input_box()
        # Start Game
        pygame.draw.rect(self.screen, Config.COLORS['green'], self.start_button)
        start_text = self.font.render("Start Game", True, (0, 0, 0))
        self.screen.blit(start_text, (self.start_button.x + self.start_button.width // 2 - start_text.get_width() // 2,
                                      self.start_button.y + self.start_button.height // 2 - start_text.get_height() // 2))
        # Back
        pygame.draw.rect(self.screen, pygame.Color('#808080'), self.back_button)
        back_text = self.font.render("Back", True, (0, 0, 0))
        self.screen.blit(back_text, (self.back_button.x + self.back_button.width // 2 - back_text.get_width() // 2,
                                     self.back_button.y + self.back_button.height // 2 - back_text.get_height() // 2))

    def draw_input_box(self):
        """ วาดช่องกรอกชื่อ """
        txt_surface = self.font.render(self.player_name, True, Config.COLORS['black'])
        width = max(300, txt_surface.get_width() + 10)
        self.input_box.w = width
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.screen, self.color_rect, self.input_box, 2)
        pygame.draw.rect(self.screen, self.color_rect, self.start_button, 2)

    def handle_input_events(self):
        mouse = pygame.mouse.get_pos()
        if self.input_box.collidepoint(mouse):
            self.active = True
            self.color_rect = self.color_active
        else:
            self.active = False
            self.color_rect = self.color_inactive