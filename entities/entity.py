from os.path import join
import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, asset_folder='player', x=0, y=0):
        super().__init__()
        self.move_x = 0
        self.move_y = 0
        self.speed = 0.25
        self.attack_animation = False
        self.attack_timer = 0
        self.attack_duration = 0.07
        self.current_sprite = 0
        self.direction = 'down'
        self.animation_speed = 0.1
        self.time_passed = 0
        self.scale_size = (64, 64)
        self.asset_folder = asset_folder

        self.images = self.load_images()

        self.image = self.images['down'][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def load_images(self):
        base_path = join('assets', self.asset_folder)
        scale = self.scale_size

        # Load move animations
        move = {
            'up': [pygame.transform.scale(pygame.image.load(join(base_path, 'move', 'up', f'{i}.png')).convert_alpha(),
                                          scale) for i in range(4)],
            'down': [
                pygame.transform.scale(pygame.image.load(join(base_path, 'move', 'down', f'{i}.png')).convert_alpha(),
                                       scale) for i in range(4)],
            'left': [
                pygame.transform.scale(pygame.image.load(join(base_path, 'move', 'left', f'{i}.png')).convert_alpha(),
                                       scale) for i in range(4)],
            'right': [
                pygame.transform.scale(pygame.image.load(join(base_path, 'move', 'right', f'{i}.png')).convert_alpha(),
                                       scale) for i in range(4)],
        }

        # Load attack images
        attack = {
            'up': pygame.transform.scale(pygame.image.load(join(base_path, 'attack', 'up.png')).convert_alpha(), scale),
            'down': pygame.transform.scale(pygame.image.load(join(base_path, 'attack', 'down.png')).convert_alpha(),
                                           scale),
            'left': pygame.transform.scale(pygame.image.load(join(base_path, 'attack', 'left.png')).convert_alpha(),
                                           scale),
            'right': pygame.transform.scale(pygame.image.load(join(base_path, 'attack', 'right.png')).convert_alpha(),
                                            scale),
        }

        return {
            'up': move['up'],
            'down': move['down'],
            'left': move['left'],
            'right': move['right'],
            'attack': attack
        }

    def attack(self):
        if not self.attack_animation:
            self.attack_animation = True
            self.attack_timer = 0

    def update(self, dt):
        self.time_passed += dt

        # Attack animation
        if self.attack_animation:
            self.attack_timer += dt
            self.image = self.images['attack'][self.direction]
            if self.attack_timer >= self.attack_duration:
                self.attack_animation = False
                self.attack_timer = 0
            return

        # Movement direction
        if self.move_y < 0:
            self.direction = 'up'
        elif self.move_y > 0:
            self.direction = 'down'
        elif self.move_x < 0:
            self.direction = 'left'
        elif self.move_x > 0:
            self.direction = 'right'

        # Walk animation
        if self.move_x != 0 or self.move_y != 0:
            if self.time_passed >= self.animation_speed:
                self.current_sprite = (self.current_sprite + 1) % 4
                self.time_passed = 0
        else:
            self.current_sprite = 0

        self.image = self.images[self.direction][self.current_sprite]