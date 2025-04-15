import random

class RandomMapGenerator:
    def __init__(self, width=20, height=11):  # fit 1280x720
        self.width = width
        self.height = height
        self.map = [[1 for _ in range(width)] for _ in range(height)]

    def generate(self):
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                self.map[y][x] = 0

        # place player start
        self.map[1][1] = 4

        # place exit
        self.map[self.height - 2][self.width - 2] = 5

        # random traps and enemies
        for _ in range(3):
            while True:
                x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
                if self.map[y][x] == 0:
                    self.map[y][x] = 2
                    break

        for _ in range(3):
            while True:
                x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
                if self.map[y][x] == 0:
                    self.map[y][x] = 3
                    break

        return self.map