from DungeonEscape.entities.entity import Entity

class Enemy(Entity):
    def __init__(self, asset_folder='enemy', x=0, y=0):
        super().__init__(asset_folder=asset_folder, x=x, y=y)
        self.health = 20
        self.speed = 1
        self.alive = True

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        self.alive = False
        print(f"[Enemy] {self.asset_folder} died.")
        self.kill()

    def update(self, dt, player=None):
        if not self.alive:
            return
        self.rect.x += self.move_x
        self.rect.y += self.move_y
        super().update(dt)