import csv
import math
import os
import subprocess
import sys
import time

import pygame
import random
from config import Config


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
        self.sparkles = []
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
        self.particles = []
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

            #Particle
            if random.random() < 0.1:
                sparkle_x = random.randint(0, self.screen.get_width())
                sparkle_y = self.screen.get_height() - 50
                self.sparkles.append(SparkleParticle(sparkle_x, sparkle_y))

            self.sparkles = [s for s in self.sparkles if s.update()]
            for sparkle in self.sparkles:
                sparkle.draw(self.screen)
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
                    elif self.how_to_button.collidepoint(event.pos):
                        self.show_how_to_play()
                        # print('test')
                    elif self.visualizer_button.collidepoint(event.pos):
                        subprocess.Popen(["python3", "stats/visualizer.py"])

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
        self.how_to_button = pygame.Rect(center_x, start_y + (button_height + 25) * 2, button_width, button_height)
        self.visualizer_button = pygame.Rect(center_x, start_y + (button_height + 25) * 3, button_width, button_height)

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

        self.draw_button(
            self.how_to_button,
            "How to Play",
            base_color=pygame.Color('#607D8B'),
            hover_color=pygame.Color('#78909C'),
            text_color=(255, 255, 255)
        )

        self.draw_button(
            self.visualizer_button,
            "Visualizer",
            base_color=pygame.Color('#3949AB'),
            hover_color=pygame.Color('#5C6BC0'),
            text_color=(255, 255, 255)
        )

    def show_how_to_play(self):
        running = True
        title_font = pygame.font.Font(os.path.join("assets", "fonts", "Balthazar.ttf"), 48)
        text_font = pygame.font.Font(None, 32)
        back_button = pygame.Rect(50, self.screen.get_height() - 70, 150, 50)

        while running:
            self.screen.fill((15, 15, 20))

            # Draw box background
            box_width, box_height = 700, 400
            box_x = self.screen.get_width() // 2 - box_width // 2
            box_y = 100
            surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            pygame.draw.rect(surface, (30, 30, 30, 200), surface.get_rect(), border_radius=15)
            self.screen.blit(surface, (box_x, box_y))
            pygame.draw.rect(self.screen, (100, 100, 100), (box_x, box_y, box_width, box_height), 2, border_radius=15)

            # Title
            title = title_font.render("How to Play", True, pygame.Color("#FFD700"))
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, box_y + 40))
            self.screen.blit(title, title_rect)

            # Instructions
            lines = [
                "- Move: WASD",
                "- Attack: Spacebar",
                "- Dash: Shift (consumes energy)",
                "- Defeat all enemies to unlock the exit",
                "- Avoid traps and hazards",
                "- Collect dropped items (heal potions)",
                "- Survive as many stages as possible",
                "- Choose different characters with unique abilities"
            ]

            for i, line in enumerate(lines):
                text = text_font.render(line, True, (220, 220, 220))
                self.screen.blit(text, (box_x + 40, box_y + 80 + i * 35))

            # Back Button
            pygame.draw.rect(self.screen, (100, 100, 100), back_button, border_radius=8)
            back_text = text_font.render("Back", True, (255, 255, 255))
            self.screen.blit(back_text, (back_button.x + 45, back_button.y + 12))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        running = False

            pygame.display.flip()

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
        background_path = os.path.join("assets", "backgrounds", "stats_bg.png")
        background = pygame.image.load(background_path).convert()
        background = pygame.transform.scale(background, self.screen.get_size())

        while running:
            self.screen.blit(background, (0,0))

            #Particle
            if random.random() < 0.05:
                x = random.randint(0, self.screen.get_width())
                y = self.screen.get_height()
                self.particles.append(Particle(x, y))

            self.particles = [p for p in self.particles if p.update()]
            for p in self.particles:
                p.draw(self.screen)

            self.draw_player_stats_ui(player)

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
                    elif self.leaderboard_button.collidepoint(event.pos):
                        # subprocess.Popen(["python3", "stats/visualizer_player_stats.py", player.name])
                        subprocess.Popen(["python", "stats/visualizer_player_stats.py", player.name])

            pygame.display.flip()
            clock.tick(60)

        return None

    def draw_player_stats_ui(self, player):
        box_width = 600
        box_height = 600  # Increased to avoid button overlap
        box_x = self.screen.get_width() // 2 - box_width // 2
        box_y = 80

        t = time.time()
        float_offset = math.sin(t * 2) * 5
        animated_box_y = box_y + float_offset

        border_radius = 20
        background_color = (30, 30, 30, 200)
        surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(surface, background_color, surface.get_rect(), border_radius=border_radius)
        self.screen.blit(surface, (box_x, animated_box_y))

        box_rect = pygame.Rect(box_x, animated_box_y, box_width, box_height)
        pygame.draw.rect(self.screen, (90, 90, 90), box_rect, 3, border_radius=border_radius)

        title_font = pygame.font.Font(os.path.join("assets", "fonts", "Balthazar.ttf"), 64)
        title = title_font.render("Player Stats Overall", True, pygame.Color("#FFD700"))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, animated_box_y + 40))
        self.screen.blit(title, title_rect)

        stats_font = pygame.font.Font(None, 36)

        stats_row = None
        try:
            with open("stats/players.csv", newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['name'] == player.name:
                        stats_row = row
                        break
        except Exception as e:
            print("[ERROR] Failed to load players.csv:", e)

        if stats_row:
            info = [
                ("Username", player.name),
                ("Current Stage", player.current_stage),
                ("Total Sessions", stats_row.get("total_sessions", "-")),
                ("Avg Time Played", stats_row.get("time_played", "-")),
                ("Avg Enemies Defeated", stats_row.get("enemies_defeated", "-")),
                ("Avg Dash Used", stats_row.get("dash_used", "-")),
                ("Avg Traps Triggered", stats_row.get("traps_triggered", "-")),
                ("Avg Distance Traveled", stats_row.get("distance_traveled", "-")),
                ("Win Rate", f"{float(stats_row.get('survived', 0)) * 100:.1f}%")
            ]
        else:
            info = [
                ("No gameplay data yet. Start your first run", "")
            ]

        start_y = title_rect.bottom + 20
        gap = 45

        for i, (label, value) in enumerate(info):
            label_text = stats_font.render(f"{label}:", True, pygame.Color("#CCCCCC"))
            value_text = stats_font.render(str(value), True, pygame.Color("#00B8D4"))

            label_rect = label_text.get_rect(topleft=(box_x + 40, start_y + i * gap))
            value_rect = value_text.get_rect(topright=(box_x + box_width - 40, start_y + i * gap))

            self.screen.blit(label_text, label_rect)
            self.screen.blit(value_text, value_rect)

        button_width = 180
        button_height = 50
        spacing = 40

        button_y = animated_box_y + box_height - button_height - 60
        leaderboard_button_y = animated_box_y + box_height - button_height - 5

        self.back_button = pygame.Rect(
            self.screen.get_width() // 2 - button_width - spacing // 2,
            button_y,
            button_width,
            button_height
        )

        self.next_button = pygame.Rect(
            self.screen.get_width() // 2 + spacing // 2,
            button_y,
            button_width,
            button_height
        )

        self.leaderboard_button = pygame.Rect(
            self.screen.get_width() // 2 - button_width // 2,
            leaderboard_button_y,
            button_width,
            button_height
        )

        self.draw_button(
            self.next_button,
            "Continue",
            base_color=pygame.Color("#3E8E7E"),
            hover_color=pygame.Color("#50BFA6"),
            text_color=pygame.Color("#F1F8E9")
        )

        self.draw_button(
            self.back_button,
            "Back",
            base_color=pygame.Color("#8B5E3C"),
            hover_color=pygame.Color("#A9745B"),
            text_color=pygame.Color("#FFF3E0")
        )

        self.draw_button(
            self.leaderboard_button,
            "Your Visualize",
            base_color=pygame.Color("#3949AB"),
            hover_color=pygame.Color("#5C6BC0"),
            text_color=pygame.Color("#E8EAF6")
        )

    def game_selection_screen(self):
        clock = pygame.time.Clock()
        running = True

        background = pygame.image.load(os.path.join("assets", "backgrounds", "selection_bg.png")).convert()
        background = pygame.transform.scale(background, self.screen.get_size())

        title_font = pygame.font.Font(os.path.join("assets", "fonts", "Balthazar.ttf"), 72)
        base_title_y = 100

        modes = [("Stage Mode", "#1B5E20", "#43A047")]
        buttons = []
        button_w, button_h = 360, 70
        spacing = 100
        center_x = self.screen.get_width() // 2 - button_w // 2
        start_y = 220

        for i, (label, base_col, hover_col) in enumerate(modes):
            rect = pygame.Rect(center_x, start_y + i * spacing, button_w, button_h)
            buttons.append((label, rect, pygame.Color(base_col), pygame.Color(hover_col)))

        back_button = pygame.Rect(center_x, start_y + len(modes) * spacing + 20, button_w, button_h)
        sparkles = []

        while running:
            self.screen.blit(background, (0, 0))

            if random.random() < 0.08:
                sparkles.append(SparkleParticle(
                    random.randint(0, self.screen.get_width()),
                    random.randint(self.screen.get_height() - 150, self.screen.get_height())
                ))
            sparkles = [s for s in sparkles if s.update()]
            for sparkle in sparkles:
                sparkle.draw(self.screen)

            t = pygame.time.get_ticks() / 1000
            float_y = math.sin(t * 2) * 10
            title = title_font.render("Select Your Challenge", True, pygame.Color("#FFD700"))
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, base_title_y + float_y))
            self.screen.blit(title, title_rect)

            mouse = pygame.mouse.get_pos()

            for label, rect, base_color, hover_color in buttons:
                self.draw_dungeon_magic_button(
                    rect, label,
                    base_color=base_color,
                    hover_color=hover_color
                )

            self.draw_dungeon_magic_button(
                back_button, "Back",
                base_color=pygame.Color("#4E342E"),
                hover_color=pygame.Color("#6D4C41")
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for label, rect, _, _ in buttons:
                        if rect.collidepoint(event.pos):
                            return label
                    if back_button.collidepoint(event.pos):
                        return "back"

            pygame.display.flip()
            clock.tick(60)

    def show_game_over_screen(self, game):
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 64)
        small_font = pygame.font.Font(None, 36)
        button_font = pygame.font.Font(None, 32)

        restart_button = pygame.Rect(self.screen.get_width() // 2 - 100, 400, 200, 50)
        home_button = pygame.Rect(self.screen.get_width() // 2 - 100, 470, 200, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        game.player = game.player.__class__(name=game.player.name,current_stage=game.player.current_stage)
                        game.player_group = pygame.sprite.Group(game.player)
                        game.session_saved = False #Reset Stat
                        game.player.reset_stats()
                        game.game_data['state'] = 'on_game'
                        return
                    elif home_button.collidepoint(event.pos):
                        game.game_data['state'] = 'home'
                        return

            if game.last_game_surface:
                self.screen.blit(game.last_game_surface, (0, 0))
                overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                self.screen.blit(overlay, (0, 0))

            game_over_text = font.render("Game Over", True, (255, 0, 0))
            self.screen.blit(game_over_text, (self.screen.get_width() // 2 - game_over_text.get_width() // 2, 200))

            # Colors
            restart_bg = pygame.Color("#8B0000")  # deep blood red
            restart_hover = pygame.Color("#A00000")
            home_bg = pygame.Color("#4B3621")  # dark stone brown
            home_hover = pygame.Color("#5A4030")
            border_color = pygame.Color("#FFD700")  # gold
            text_color = pygame.Color("#FFFFFF")

            # Hover effect
            mouse = pygame.mouse.get_pos()
            restart_is_hovered = restart_button.collidepoint(mouse)
            home_is_hovered = home_button.collidepoint(mouse)

            # Draw Restart Button
            pygame.draw.rect(self.screen, restart_hover if restart_is_hovered else restart_bg, restart_button,
                             border_radius=10)
            pygame.draw.rect(self.screen, border_color, restart_button, 2, border_radius=10)

            # Draw Home Button
            pygame.draw.rect(self.screen, home_hover if home_is_hovered else home_bg, home_button, border_radius=10)
            pygame.draw.rect(self.screen, border_color, home_button, 2, border_radius=10)

            # Text
            restart_text = button_font.render("Restart", True, text_color)
            home_text = button_font.render("Home", True, text_color)

            self.screen.blit(restart_text, restart_text.get_rect(center=restart_button.center))
            self.screen.blit(home_text, home_text.get_rect(center=home_button.center))

            pygame.display.flip()
            clock.tick(60)

    def draw_dungeon_magic_button(self, rect, text, base_color, hover_color, text_color=(255, 255, 255)):
        mouse = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse)

        t = pygame.time.get_ticks() / 1000
        float_offset = math.sin(t * 2 + rect.y * 0.01) * 4
        glow_strength = int((math.sin(t * 3 + rect.x) + 1) * 50 + 80)
        pulse_color = (255, 160, 60, glow_strength)

        floating_rect = rect.copy()
        floating_rect.y += float_offset

        border_radius = 12
        shadow_rect = floating_rect.copy()
        shadow_rect.y += 6
        pygame.draw.rect(self.screen, (10, 5, 5), shadow_rect, border_radius=border_radius)

        if is_hovered:
            aura = pygame.Surface((floating_rect.width + 20, floating_rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(aura, pulse_color, aura.get_rect(), border_radius=border_radius)
            self.screen.blit(aura, (floating_rect.x - 10, floating_rect.y - 10))

        if is_hovered:
            angle = (t * 90) % 360
            circle_surf = pygame.Surface((floating_rect.width + 30, floating_rect.height + 30), pygame.SRCALPHA)
            pygame.draw.ellipse(circle_surf, (180, 100, 255, 60), circle_surf.get_rect(), 3)
            circle_rotated = pygame.transform.rotate(circle_surf, angle)
            circle_rect = circle_rotated.get_rect(center=floating_rect.center)
            self.screen.blit(circle_rotated, circle_rect)

        pygame.draw.rect(self.screen, base_color, floating_rect, border_radius=border_radius)
        pygame.draw.rect(self.screen, (70, 50, 30), floating_rect, 2, border_radius=border_radius)

        rune_layer = pygame.Surface((floating_rect.width, floating_rect.height), pygame.SRCALPHA)
        for _ in range(6):
            rx = random.randint(10, floating_rect.width - 10)
            ry = random.randint(10, floating_rect.height - 10)
            alpha = random.randint(20, 50)
            pygame.draw.circle(rune_layer, (180, 180, 255, alpha), (rx, ry), 2)
        self.screen.blit(rune_layer, floating_rect.topleft)

        text_surface = self.font.render(text, True, text_color)
        text_shadow = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=floating_rect.center)
        shadow_rect = text_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        self.screen.blit(text_shadow, shadow_rect)
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, rect, text, base_color, hover_color, text_color=(255, 255, 255),
                    border_color=(0, 0, 0), shadow=True):
        mouse = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse)

        if shadow:
            shadow_rect = pygame.Rect(rect.x + 4, rect.y + 4, rect.width, rect.height)
            pygame.draw.rect(self.screen, (40, 30, 30), shadow_rect, border_radius=8)

        if is_hovered:
            glow_color = pygame.Color("#FFD180")
            pygame.draw.rect(self.screen, glow_color, rect.inflate(12, 12), border_radius=10)
            pygame.draw.rect(self.screen, glow_color, rect.inflate(6, 6), 2, border_radius=10)

        current_color = hover_color if is_hovered else base_color
        pygame.draw.rect(self.screen, current_color, rect, border_radius=10)
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=10)

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

    def character_selection_screen(self):
        screen = self.screen
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 36)
        big_font = pygame.font.Font(None, 48)

        characters = [
            {"name": "Swordman", "desc": "Balanced melee fighter.",
             "image": pygame.image.load("assets/char_select/swordman.png")},
            {"name": "Archer", "desc": "Long-range but fragile.",
             "image": pygame.image.load("assets/char_select/archer.png")}
        ]

        index = 0
        selecting = True

        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        index = (index - 1) % len(characters)
                    elif event.key == pygame.K_RIGHT:
                        index = (index + 1) % len(characters)
                    elif event.key == pygame.K_RETURN:
                        return characters[index]["name"]

            screen.fill((10, 10, 10))
            title = big_font.render("Select Your Character", True, (255, 255, 255))
            screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 80))

            char = characters[index]
            screen.blit(char["image"], (screen.get_width() // 2 - 64, 150))

            name_text = font.render(char["name"], True, (255, 255, 0))
            desc_text = font.render(char["desc"], True, (200, 200, 200))
            screen.blit(name_text, (screen.get_width() // 2 - name_text.get_width() // 2, 300))
            screen.blit(desc_text, (screen.get_width() // 2 - desc_text.get_width() // 2, 340))

            tip = font.render("← → to choose, Enter to confirm", True, (180, 180, 180))
            screen.blit(tip, (screen.get_width() // 2 - tip.get_width() // 2, 420))

            pygame.display.flip()
            clock.tick(60)

import random

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(5, 8)
        self.alpha = random.randint(80, 180)
        self.speed_y = random.uniform(-0.2, -0.7)
        self.speed_x = random.uniform(-0.2, 0.2)

    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x
        self.alpha -= 0.3  # ค่อย ๆ จาง
        return self.alpha > 0

    def draw(self, surface):
        s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 200, int(self.alpha)), (self.radius, self.radius), self.radius)
        surface.blit(s, (self.x, self.y))

class SparkleParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 4)
        self.alpha = random.randint(120, 200)
        self.speed_y = random.uniform(-0.3, -0.6)
        self.speed_x = random.uniform(-0.2, 0.2)
        self.color = (255, 255, random.randint(180, 220), self.alpha)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.alpha -= 0.6
        return self.alpha > 0

    def draw(self, surface):
        s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(s, self.color, (self.radius, self.radius), self.radius)
        surface.blit(s, (self.x, self.y))