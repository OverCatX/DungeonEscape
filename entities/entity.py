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

        images = {'up': [pygame.transform.scale(pygame.image.load(join(base_path, 'up', f'{i}.png')).convert_alpha(),
                                                self.scale_size) for i in range(4)], 'down': [
            pygame.transform.scale(pygame.image.load(join(base_path, 'down', f'{i}.png')).convert_alpha(),
                                   self.scale_size) for i in range(4)], 'left': [
            pygame.transform.scale(pygame.image.load(join(base_path, 'left', f'{i}.png')).convert_alpha(),
                                   self.scale_size) for i in range(4)], 'right': [
            pygame.transform.scale(pygame.image.load(join(base_path, 'right', f'{i}.png')).convert_alpha(),
                                   self.scale_size) for i in range(4)], 'attack': {
            'up': pygame.transform.scale(pygame.image.load(join(base_path, 'attack', 'up.png')).convert_alpha(),
                                         self.scale_size),
            'down': pygame.transform.scale(pygame.image.load(join(base_path, 'attack', 'down.png')).convert_alpha(),
                                           self.scale_size),
            'left': pygame.transform.scale(pygame.image.load(join(base_path, 'attack', 'left.png')).convert_alpha(),
                                           self.scale_size),
            'right': pygame.transform.scale(pygame.image.load(join(base_path, 'attack', 'right.png')).convert_alpha(),
                                            self.scale_size),
        }}
        return images

    def attack(self):
        if not self.attack_animation:
            self.attack_animation = True
            self.attack_timer = 0

    def update(self, dt):
        self.rect.x += self.move_x
        self.rect.y += self.move_y
        self.time_passed += dt

        if self.attack_animation:
            self.attack_timer += dt
            self.image = self.images['attack'][self.direction]

            if self.attack_timer >= self.attack_duration:
                self.attack_animation = False
                self.attack_timer = 0
            return

        if self.move_y < 0:
            self.direction = 'up'
        elif self.move_y > 0:
            self.direction = 'down'
        elif self.move_x < 0:
            self.direction = 'left'
        elif self.move_x > 0:
            self.direction = 'right'

        if self.move_x != 0 or self.move_y != 0:
            if self.time_passed >= self.animation_speed:
                self.current_sprite = (self.current_sprite + 1) % 4
                self.time_passed = 0
        else:
            self.current_sprite = 0

        self.image = self.images[self.direction][self.current_sprite]