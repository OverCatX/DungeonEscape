import sys

import pygame

from entities.players.player_archer import PlayerArcher
from entities.players.player_assasin import *
from entities.players.player_blink import PlayerBlink


class CharacterCard:
    def __init__(self, name, image, description, cls, position):
        self.name = name
        self.image = pygame.transform.scale(pygame.image.load(image), (96, 96))
        self.description = description
        self.cls = cls
        self.rect = pygame.Rect(position[0], position[1], 140, 180)
        self.selected = False

    def draw(self, screen, font, is_hovered):
        border_color = (255, 215, 0) if self.selected else (180, 180, 180) if is_hovered else (100, 100, 100)
        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        pygame.draw.rect(screen, border_color, self.rect, 3)

        screen.blit(self.image, (self.rect.centerx - 48, self.rect.y + 10))
        name_text = font.render(self.name, True, (255, 255, 255))
        screen.blit(name_text, (self.rect.centerx - name_text.get_width() // 2, self.rect.y + 110))

        # Show description if hovered
        if is_hovered:
            lines = self.description.split("\n")
            for i, line in enumerate(lines):
                desc = font.render(line, True, (200, 200, 200))
                screen.blit(desc, (self.rect.x, self.rect.y + 130 + i * 18))


class CharacterSelectUI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 48)

        self.characters = [
            {
                "type": "Assassin",
                "img": pygame.transform.scale(
                    pygame.image.load("assets/characters/swordman_thumb.png").convert_alpha(),
                    (64, 64)
                ),
                "desc": "Agile melee specialist.\nStrong vs isolated enemies.\nWeak against swarms."
            },
            {
                "type": "Archer",
                "img": pygame.transform.scale(
                    pygame.image.load("assets/characters/archerman_thumb.png").convert_alpha(),
                    (64, 64)
                ),
                "desc": "Long-range attacker.\nEffective vs slow enemies.\nStruggles in close combat."
            },
            {
                "type": "Blink",
                "img": pygame.transform.scale(
                    pygame.image.load("assets/characters/mage_thumb.png").convert_alpha(),
                    (64, 64)
                ),
                "desc": "Burst AoE caster.\nGreat for groups & chokepoints.\nLow HP – avoid direct hits."
            }
        ]

    def select_character(self, name):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))

        # --- กล่องกลาง ---
        box = pygame.Rect(0, 0, 700, 400)
        box.center = self.screen.get_rect().center
        close_btn = pygame.Rect(box.right - 40, box.top + 10, 30, 30)

        buttons = []
        for i, char in enumerate(self.characters):
            rect = pygame.Rect(0, 0, 120, 140)
            rect.centerx = box.left + 150 + i * 200
            rect.centery = box.centery
            buttons.append((rect, char))

        while True:
            self.screen.blit(self.last_surface_copy, (0, 0))  # bg เป็นภาพก่อนหน้า
            self.screen.blit(overlay, (0, 0))
            pygame.draw.rect(self.screen, (50, 30, 10), box, border_radius=12)
            pygame.draw.rect(self.screen, (255, 255, 255), box, 2)

            # Title
            title = self.big_font.render("Choose Your Class", True, (255, 255, 200))
            self.screen.blit(title, (box.centerx - title.get_width() // 2, box.top + 20))

            # Close button
            pygame.draw.rect(self.screen, (150, 0, 0), close_btn)
            x_txt = self.font.render("X", True, (255, 255, 255))
            self.screen.blit(x_txt, (close_btn.centerx - x_txt.get_width() // 2, close_btn.centery - x_txt.get_height() // 2))

            mouse = pygame.mouse.get_pos()
            hovered = None

            # Character buttons
            for rect, char in buttons:
                scaled_img = pygame.transform.scale(char["img"], (rect.width, rect.height))

                img_rect = scaled_img.get_rect(center=rect.center)
                self.screen.blit(scaled_img, img_rect)

                pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)

                if rect.collidepoint(mouse):
                    hovered = char

            # Hover text
            if hovered:
                lines = hovered["desc"].split("\n")
                for i, line in enumerate(lines):
                    txt = self.font.render(line, True, (255, 255, 255))
                    self.screen.blit(txt, (box.left + 30, box.bottom - 80 + i * 25))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if close_btn.collidepoint(event.pos):
                        return None
                    for rect, char in buttons:
                        if rect.collidepoint(event.pos):
                            if char["type"] == 'Assassin':
                                return PlayerAssassin(name=name,character_type=char["type"])
                            elif char["type"] == 'Archer':
                                return PlayerArcher(name=name,character_type=char["type"])
                            elif char["type"] == 'Blink':
                                return PlayerBlink(name=name,character_type=char["type"])