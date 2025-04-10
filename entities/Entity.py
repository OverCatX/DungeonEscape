from os.path import join
import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.move_x = 0
        self.move_y = 0
        self.speed = 0.25
        self.attack_animation = False
        self.current_sprite = 0
        self.animation_speed = 0.025
        self.time_passed = 0

        self.images = {
            'up': [pygame.image.load(join('assets', 'player', 'up', f'{i}.png')).convert_alpha() for i in range(4)],
            'down': [pygame.image.load(join('assets', 'player', 'down', f'{i}.png')).convert_alpha() for i in range(4)],
            'left': [pygame.image.load(join('assets', 'player', 'left', f'{i}.png')).convert_alpha() for i in range(4)],
            'right': [pygame.image.load(join('assets', 'player', 'right', f'{i}.png')).convert_alpha() for i in
                      range(4)],
        }

        # Set the initial image and scale it
        self.image = pygame.transform.scale(self.images['down'][self.current_sprite], (64, 64))
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def attack(self):
        self.attack_animation = True

    def update(self, dt):
        self.rect.x += self.move_x
        self.rect.y += self.move_y

        self.time_passed += dt
        # print(self.time_passed)

        if self.move_y < 0:
            self.image = pygame.transform.scale(self.images['up'][self.current_sprite], (64, 64))
        elif self.move_y > 0:
            self.image = pygame.transform.scale(self.images['down'][self.current_sprite], (64, 64))
        elif self.move_x < 0:
            self.image = pygame.transform.scale(self.images['left'][self.current_sprite], (64, 64))
        elif self.move_x > 0:
            self.image = pygame.transform.scale(self.images['right'][self.current_sprite], (64, 64))

        if self.move_x != 0 or self.move_y != 0:
            if self.time_passed >= self.animation_speed:
                print(self.current_sprite)
                if self.current_sprite >= 3:
                    self.current_sprite = 0
                else:
                    self.current_sprite += 1
                self.time_passed = 0
        self.image = pygame.transform.scale(self.image, (64, 64))