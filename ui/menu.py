import os
import sys

import pygame
from DungeonEscape.config import Config


class Menu:
    def __init__(self, screen):
        self.screen = screen
        head_path = os.path.join("assets", "fonts", "Balthazar.ttf")
        self.head_font = pygame.font.Font(head_path, 100)
        self.font = pygame.font.Font(None, 36)
        self.color = (255, 255, 255)
        self.player_name = ""
        screen_width, screen_height = self.screen.get_size()

        #Home UI
        input_box_width = 400
        input_box_height = 40
        input_x = screen_width // 2 - input_box_width // 2
        self.input_box = pygame.Rect(input_x, 100, input_box_width, input_box_height)
        self.start_button = pygame.Rect(input_x, 320, input_box_width, input_box_height)
        self.exit_button = pygame.Rect(200, 340, 400, 40)

        #Warning Box (Name is Null)
        self.show_warning = False
        self.warning_timer = 0
        self.warning_duration = 1 * 1000

        #Player_Progress UI
        self.next_button = pygame.Rect(
            self.screen.get_width() // 2 - 140,
            self.screen.get_height() - 200,
            280,
            60
        )
        self.back_button = pygame.Rect(
            self.screen.get_width() // 2 - 60,
            self.screen.get_height() - 120,
            120,
            60
        )

        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color_rect = self.color_inactive
        self.active = False

    def home_screen(self):
        clock = pygame.time.Clock()
        running = True
        background_path = os.path.join("assets", "backgrounds", "home_bg.png")
        background = pygame.image.load(background_path).convert()
        background = pygame.transform.scale(background, self.screen.get_size())
        while running:
            self.screen.blit(background, (0, 0))
            self.draw_home_buttons()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.collidepoint(event.pos):
                        if self.player_name.strip() == "":
                            self.show_warning = True
                            self.warning_timer = pygame.time.get_ticks()
                        else:
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
            if self.show_warning:
                now = pygame.time.get_ticks()
                if now - self.warning_timer > self.warning_duration:
                    self.show_warning = False
                else:
                    self.draw_warning_box()
            pygame.display.flip()
            clock.tick(60)

    def draw_home_buttons(self):
        title_text = self.head_font.render("Dungeon Escape", True, pygame.Color('#FFD700'))
        title_x = self.screen.get_width() // 2 - title_text.get_width() // 2
        title_y = 80  # เดิม 60 → เพิ่มระยะห่างจากขอบ
        self.screen.blit(title_text, (title_x, title_y))

        # Label
        label_text = self.font.render("Enter your name:", True, Config.COLORS['white'])
        label_width = label_text.get_width()
        label_height = label_text.get_height()
        spacing = 10
        input_width = max(300, self.font.size(self.player_name)[0] + 20)
        input_height = self.input_box.height

        total_width = label_width + spacing + input_width
        screen_center_x = self.screen.get_width() // 2

        label_x = screen_center_x - total_width // 2
        input_x = label_x + label_width + spacing
        y = 220  # เดิม 300 → ปรับให้สมดุลขึ้นใต้ title
        self.input_box.x = input_x
        self.input_box.y = y
        self.input_box.w = input_width

        label_y = y + (input_height // 2 - label_height // 2)
        self.screen.blit(label_text, (label_x, label_y))

        self.draw_input_box()

        # Buttons
        button_width = 400
        button_height = 50
        center_x = self.screen.get_width() // 2 - button_width // 2
        start_y = y + 80  # ห่างจาก input box มากขึ้นเล็กน้อย

        self.start_button = pygame.Rect(center_x, start_y, button_width, button_height)
        self.exit_button = pygame.Rect(center_x, start_y + button_height + 25, button_width, button_height)

        self.draw_button(
            self.start_button,
            "Start Game",
            base_color=Config.COLORS['green'],
            hover_color=(60, 200, 60),
            text_color=(0, 0, 0)
        )

        self.draw_button(
            self.exit_button,
            "Exit",
            base_color=Config.COLORS['red'],
            hover_color=(255, 100, 100),
            text_color=(0, 0, 0)
        )

    def draw_input_box(self):
        border_radius = 10
        background_color = pygame.Color("#2C2F33")  # dark gray
        active_outline_color = pygame.Color("#6C63FF")  # magical purple
        inactive_outline_color = pygame.Color("#444444")  # shadowy gray
        text_color = pygame.Color("#EEEEEE")
        placeholder_color = pygame.Color("#888888")

        outline_color = active_outline_color if self.active else inactive_outline_color

        # Shadow effect
        shadow_offset = 4
        shadow_rect = self.input_box.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        pygame.draw.rect(self.screen, pygame.Color("#1A1A1A"), shadow_rect, border_radius=border_radius)

        # Background box
        pygame.draw.rect(self.screen, background_color, self.input_box, border_radius=border_radius)

        # Outline
        pygame.draw.rect(self.screen, outline_color, self.input_box, width=2, border_radius=border_radius)

        # Text
        if self.player_name:
            txt_surface = self.font.render(self.player_name, True, text_color)
        else:
            txt_surface = self.font.render("Enter your name...", True, placeholder_color)

        self.screen.blit(txt_surface, (self.input_box.x + 10, self.input_box.y + 8))

    def show_player_stats(self, player):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.fill(Config.COLORS['white'])
            self.draw_player_stats_ui(player)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.next_button.collidepoint(event.pos):
                        return "continue"
                    elif self.back_button.collidepoint(event.pos):
                        return "back"

            pygame.display.flip()
            clock.tick(60)

        return None

    def draw_player_stats_ui(self, player):
        # Title
        title = self.font.render("Player Stats", True, Config.COLORS['black'])
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title, title_rect)

        info = [
            ("Username", player.name),
            ("MaxState", player.max_state),
            ("TimePlayed", player.time_played),
            ("EnemiesDefeated", player.enemies_defeated),
            ("ItemsCollected", player.items_collected)
        ]

        start_y = 130
        gap = 60

        for i, (label, value) in enumerate(info):
            label_text = self.font.render(f"{label}:", True, Config.COLORS['black'])
            value_text = self.font.render(str(value), True, pygame.Color("#0097A7"))

            label_rect = label_text.get_rect(topleft=(400, start_y + i * gap))
            value_rect = value_text.get_rect(topright=(880, start_y + i * gap))

            self.screen.blit(label_text, label_rect)
            self.screen.blit(value_text, value_rect)

        #Continue Button
        self.draw_button(
            self.next_button,
            "Continue",
            base_color=pygame.Color("#4CAF50"),
            hover_color=pygame.Color("#66BB6A")
        )
        #Back Button
        self.draw_button(
            self.back_button,
            "Back",
            base_color=pygame.Color("#FF5722"),
            hover_color=pygame.Color("#FF7043")
        )

    def draw_button(self, rect, text, base_color, hover_color, text_color=(255, 255, 255), border_color=(0, 0, 0),
                    shadow=True):
        mouse = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse)

        if shadow:
            shadow_rect = pygame.Rect(rect.x + 4, rect.y + 4, rect.width, rect.height)
            pygame.draw.rect(self.screen, (50, 50, 50), shadow_rect, border_radius=8)

        current_color = hover_color if is_hovered else base_color
        pygame.draw.rect(self.screen, current_color, rect, border_radius=8)
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=8)

        text_surf = self.font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def draw_warning_box(self):
        message = "Please enter your name before starting!"
        font = pygame.font.Font(None, 24)

        box_width = 360
        box_height = 50
        box_x = self.screen.get_width() // 2 - box_width // 2
        box_y = self.input_box.y + self.input_box.height + 20

        border_radius = 10
        background_color = pygame.Color("#FFCDD2")  # soft red
        border_color = pygame.Color("#C62828")  # deep red
        text_color = pygame.Color("#B71C1C")

        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, background_color, box_rect, border_radius=border_radius)
        pygame.draw.rect(self.screen, border_color, box_rect, 2, border_radius=border_radius)

        warning_text = font.render(message, True, text_color)
        text_rect = warning_text.get_rect(center=box_rect.center)
        self.screen.blit(warning_text, text_rect)

    def handle_input_events(self):
        mouse = pygame.mouse.get_pos()
        if self.input_box.collidepoint(mouse):
            self.color_rect = self.color_active
        else:
            self.color_rect = self.color_inactive