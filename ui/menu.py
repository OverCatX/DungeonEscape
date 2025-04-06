import sys

import pygame
from DungeonEscape.config import Config


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.color = (255, 255, 255)
        self.player_name = ""
        screen_width, screen_height = self.screen.get_size()
        input_box_width = 400
        input_box_height = 40
        input_x = screen_width // 2 - input_box_width // 2
        self.input_box = pygame.Rect(input_x, 100, input_box_width, input_box_height)

        self.start_button = pygame.Rect(input_x, 280, input_box_width, input_box_height)
        self.back_button = pygame.Rect(input_x, 340, input_box_width, input_box_height)
        self.exit_button = pygame.Rect(200, 340, 400, 40)

        self.progressive_button = pygame.Rect(input_x, 200, input_box_width, input_box_height)
        self.hard_mode_button = pygame.Rect(input_x, 260, input_box_width, input_box_height)
        self.back_button = pygame.Rect(input_x, 320, input_box_width, input_box_height)

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
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos) and self.player_name != "":
                        running = False
                        return self.player_name
                    elif self.exit_button.collidepoint(event.pos):
                        running = False
                        return 'exit'
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
        title_text = self.font.render("Dungeon Escape", True, Config.COLORS['black'])
        title_x = self.screen.get_width() // 2 - title_text.get_width() // 2
        title_y = 20
        self.screen.blit(title_text, (title_x, title_y))

        label_text = self.font.render("Enter your name:", True, Config.COLORS['black'])
        label_width = label_text.get_width()
        label_height = label_text.get_height()
        spacing = 10
        input_width = max(300, self.font.size(self.player_name)[0] + 20)
        input_height = self.input_box.height

        total_width = label_width + spacing + input_width
        screen_center_x = self.screen.get_width() // 2

        label_x = screen_center_x - total_width // 2
        input_x = label_x + label_width + spacing
        y = 150
        self.input_box.x = input_x
        self.input_box.y = y
        self.input_box.w = input_width

        # label
        label_y = y + (input_height // 2 - label_height // 2)
        self.screen.blit(label_text, (label_x, label_y))

        #input box
        self.draw_input_box()

        #Start button
        self.start_button.x = self.screen.get_width() // 2 - self.start_button.width // 2
        pygame.draw.rect(self.screen, Config.COLORS['green'], self.start_button)
        start_text = self.font.render("Start Game", True, (0, 0, 0))
        self.screen.blit(start_text, (
            self.start_button.x + self.start_button.width // 2 - start_text.get_width() // 2,
            self.start_button.y + self.start_button.height // 2 - start_text.get_height() // 2
        ))

        #Exit button
        self.exit_button.x = self.screen.get_width() // 2 - self.exit_button.width // 2
        pygame.draw.rect(self.screen, Config.COLORS['red'], self.exit_button)
        exit_text = self.font.render("Exit", True, (0, 0, 0))
        self.screen.blit(exit_text, (
            self.exit_button.x + self.exit_button.width // 2 - exit_text.get_width() // 2,
            self.exit_button.y + self.exit_button.height // 2 - exit_text.get_height() // 2
        ))

    def select_mode(self, player_name):
        """หน้าเลือกโหมดเกม"""
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.fill(Config.COLORS['white'])
            self.draw_select_mode_buttons(player_name)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.progressive_button.collidepoint(event.pos):
                        return "progressive"
                    elif self.hard_mode_button.collidepoint(event.pos):
                        return "hard"
                    elif self.back_button.collidepoint(event.pos):
                        return 'back'

            pygame.display.flip()
            clock.tick(60)

        return None

    def draw_select_mode_buttons(self, player_name):
        # Select Mode
        title_text = self.font.render("Select Mode", True, Config.COLORS['black'])
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)


        #Welcome Text
        welcome_text = self.font.render(f"Welcome: {player_name}", True, Config.COLORS['black'])
        welcome_rect = welcome_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(welcome_text, welcome_rect)

        # Progressive Mode
        pygame.draw.rect(self.screen, pygame.Color('#0097A7'), self.progressive_button)
        progressive_text = self.font.render("Progressive", True, Config.COLORS['white'])
        progressive_rect = progressive_text.get_rect(center=self.progressive_button.center)
        self.screen.blit(progressive_text, progressive_rect)

        # ปุ่มโหมดยาก
        pygame.draw.rect(self.screen, Config.COLORS['red'], self.hard_mode_button)
        hard_text = self.font.render("Hard", True, Config.COLORS['white'])
        hard_rect = hard_text.get_rect(center=self.hard_mode_button.center)
        self.screen.blit(hard_text, hard_rect)

        # ปุ่มกลับ
        pygame.draw.rect(self.screen, Config.COLORS['gray'], self.back_button)
        back_text = self.font.render("Back", True, Config.COLORS['white'])
        back_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_rect)

        # เส้นขอบปุ่ม
        pygame.draw.rect(self.screen, Config.COLORS['black'], self.progressive_button, 2)
        pygame.draw.rect(self.screen, Config.COLORS['black'], self.hard_mode_button, 2)
        pygame.draw.rect(self.screen, Config.COLORS['black'], self.back_button, 2)

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