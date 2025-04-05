import pygame

from DungeonEscape.db.player_data import PlayerDB
from DungeonEscape.entities.Entity import Entity

class Player(Entity):
    def __init__(self, x=0, y=0, sprite=None, health=100, armor=0, name="Player",
                 time_played=0, enemies_defeated=0, items_collected=0, max_state=0):
        super().__init__(x, y, sprite, health, armor)
        self.name = name
        self.speed = 5
        self.time_played = time_played
        self.enemies_defeated = enemies_defeated
        self.items_collected = items_collected
        self.max_state = max_state

    def update(self):
        self.handle_input()
        super().update()

    def handle_input(self):
        """ ควบคุมการเคลื่อนไหวของ Player ด้วยปุ่มคีย์ """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:  # ถ้ากดปุ่ม Right Arrow
            self.direction.x = 1
        else:
            self.direction.x = 0  # ไม่มีการเคลื่อนไหวในแนวนอน

        if keys[pygame.K_UP]:  # ถ้ากดปุ่ม Up Arrow
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:  # ถ้ากดปุ่ม Down Arrow
            self.direction.y = 1
        else:
            self.direction.y = 0  # ไม่มีการเคลื่อนไหวในแนวตั้ง

    def draw(self, screen):
        """ วาด Player บนหน้าจอ """
        super().draw(screen)  # ใช้ฟังก์ชัน draw จาก Entity class

    def take_damage(self, amount):
        """ Player จะลดความเสียหายจากการโจมตีที่ได้รับ """
        super().take_damage(amount)  # เรียกใช้ฟังก์ชัน take_damage ของ Entity
        if not self.is_alive:
            self.die()  # เมื่อ Player ตาย
            # เพิ่มการจัดการเมื่อ Player ตาย เช่น การแสดงข้อความ Game Over

    def die(self):
        """ เมื่อ Player ตาย """
        print(f"{self.name} has died.")
        # คุณสามารถเพิ่มการเล่นเสียงหรือการแสดงข้อความ Game Over ที่นี่

    def update_max_state(self, max_state):
        self.max_state = max_state
        PlayerDB().update_player_stats(self.name, self.max_state, self.time_played, self.enemies_defeated, self.items_collected)
        print(f'Updated {self.name} MaxState to {self.max_state}')

    def update_time_played(self, time_played):
        self.time_played = time_played
        PlayerDB().update_player_stats(self.name, self.max_state, self.time_played, self.enemies_defeated, self.items_collected)
        print(f'Updated {self.name} TimePlayed to {self.time_played}')

    def update_enemies_defeated(self, enemies_defeated):
        self.enemies_defeated = enemies_defeated
        PlayerDB().update_player_stats(self.name, self.max_state, self.time_played, self.enemies_defeated, self.items_collected)
        print(f'Updated {self.name} EnemiesDefeated to {self.enemies_defeated}')

    def update_items_collected(self, items_collected):
        self.items_collected = items_collected
        PlayerDB().update_player_stats(self.name, self.max_state, self.time_played, self.enemies_defeated, self.items_collected)
        print(f'Updated {self.name} ItemsCollected to {self.items_collected}')

    def __str__(self):
        return f'Player: {self.name}, MaxState: {self.max_state}, TimePlayed: {self.time_played}, EnemiesDefeated: {self.enemies_defeated}, ItemsCollected: {self.items_collected}'