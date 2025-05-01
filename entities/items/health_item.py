from entities.items.dropitem import DropItem


class HealthDrop(DropItem):
    def __init__(self, x, y, image):
        def heal(player):
            player.health = min(player.health + 30, 100)
        super().__init__(x, y, image, heal)