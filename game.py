import pygame.display

from DungeonEscape.config import Config
from DungeonEscape.ui.menu import Menu

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.screen)
        self.running = False
        self.player = None
        self.map = None
        self.enemies = []
        self.items = []
        self.traps = []

    def start(self):
        self.running = True
        self.run()
        self.get_player_info()
        self.setup_game()

    def get_player_info(self):
        self.menu.get_player_info_menu()

    def setup_game(self):
        """
        Note: Setup game ex. create enemy,item,charactor
        """

    def handle_events(self):
        """
        Note: Handle Events ex. interaction etc..
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_input(event)

    def handle_input(self, event):
        """
        Note: Handle Press button from player
        """
        if event.key == pygame.K_UP:
            self.player.move_up()
        elif event.key == pygame.K_DOWN:
            self.player.move_down()
        elif event.key == pygame.K_LEFT:
            self.player.move_left()
        elif event.key == pygame.K_RIGHT:
            self.player.move_right()

    def update(self):
        """
        อัปเดตสถานะของเกม (การเคลื่อนที่ของตัวละคร, การทำงานของศัตรู, การชน ฯลฯ)
        """
        self.player.update()  # อัปเดตสถานะของผู้เล่น
        for enemy in self.enemies:
            enemy.update()  # อัปเดตสถานะของศัตรู
        for trap in self.traps:
            trap.update()  # อัปเดตสถานะของกับดัก

    def render(self):
        """
        แสดงผลหน้าจอ (การวาดภาพต่าง ๆ เช่น ตัวละคร, ศัตรู, ไอเท็ม)
        """
        self.screen.fill(Config.BACKGROUND_COLOR)  # เติมพื้นหลังด้วยสีที่กำหนดใน config
        self.player.render(self.screen)  # วาดตัวละครผู้เล่น
        for enemy in self.enemies:
            enemy.render(self.screen)  # วาดศัตรู
        for trap in self.traps:
            trap.render(self.screen)  # วาดกับดัก

        pygame.display.flip()  # อัปเดตหน้าจอ

    def check_game_over(self):
        """
        ตรวจสอบว่าเกมจบหรือยัง (เช่น ผู้เล่นตายหรือชนะ)
        """
        if self.player.hp <= 0:
            self.running = False
            self.show_game_over()

    def show_game_over(self):
        """
        แสดงหน้าจอ Game Over
        """
        font = pygame.font.SysFont("Arial", 32)
        text = font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(text, (Config.SCREEN_WIDTH // 2 - text.get_width() // 2, Config.SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # รอ 2 วินาที

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()