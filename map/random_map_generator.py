import random

class RandomMapGenerator:
    def __init__(self, width=20, height=11):  # fit 1280x720
        self.width = width
        self.height = height
        self.map = [["wall" for _ in range(width)] for _ in range(height)]

    def generate(self, enemy_count=3):
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                self.map[y][x] = "floor"

        # place player start
        self.map[1][1] = "player"

        # place exit
        candidate_exits = []
        for y in range(2, self.height - 2):
            for x in range(2, self.width - 2):
                if self.map[y][x] == 'floor':
                    neighbors = [
                        self.map[y + 1][x], self.map[y - 1][x],
                        self.map[y][x + 1], self.map[y][x - 1]
                    ]
                    if neighbors.count('floor') >= 3:
                        candidate_exits.append((x, y))

        if candidate_exits:
            exit_x, exit_y = random.choice(candidate_exits)
            self.map[exit_y][exit_x] = 'exit'
        # y = random.randint(1, self.height - 2)
        # if self.map[y][self.width - 2] == "floor":
        #     self.map[y][self.width - 2] = "exit"

        # place random traps
        for _ in range(20):
            while True:
                x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
                if self.map[y][x] == "floor":
                    trap_type = random.choice(["spike", "poison", "timed_spike"])
                    self.map[y][x] = trap_type
                    break

        # place random enemies
        for _ in range(enemy_count):
            placed = False
            for _ in range(100):  # ลอง 100 ครั้ง
                x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
                if self.map[y][x] == 'floor':
                    self.map[y][x] = 'enemy'
                    placed = True
                    break
            if not placed:
                print("[Warning] Failed to place enemy after 100 tries.")
        return self.map