import random

class RandomMapGenerator:
    def __init__(self, width=20, height=11):  # fit 1280x720
        self.width = width
        self.height = height
        self.map = [["wall" for _ in range(width)] for _ in range(height)]

    def generate(self):
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                self.map[y][x] = "floor"

        # place player start
        self.map[1][1] = "player"

        # place exit
        self.map[self.height - 2][self.width - 2] = "exit"

        # place random traps
        for _ in range(10):
            while True:
                x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
                if self.map[y][x] == "floor":
                    trap_type = random.choice(["spike", "poison", "timed_spike"])
                    self.map[y][x] = trap_type
                    break

        # place random enemies
        for _ in range(3):
            while True:
                x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
                if self.map[y][x] == "floor":
                    self.map[y][x] = "enemy"
                    break

        return self.map
