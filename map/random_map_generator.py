import random

class RandomMapGenerator:
    def __init__(self, width=15, height=15):
        self.width = width
        self.height = height
        self.map = [[1 for _ in range(width)] for _ in range(height)]  # 1 = wall

    def generate(self, room_count=4):
        rooms = []
        for _ in range(room_count):
            w, h = random.randint(3, 5), random.randint(3, 5)
            x, y = random.randint(1, self.width - w - 2), random.randint(1, self.height - h - 2)
            rooms.append((x, y, w, h))
            for i in range(x, x + w):
                for j in range(y, y + h):
                    self.map[j][i] = 0  # 0 = floor

        for i in range(1, len(rooms)):
            x1, y1 = rooms[i-1][0], rooms[i-1][1]
            x2, y2 = rooms[i][0], rooms[i][1]
            self.carve_corridor(x1, y1, x2, y2)

        px, py = rooms[0][0]+1, rooms[0][1]+1
        ex, ey = rooms[-1][0]+1, rooms[-1][1]+1
        self.map[py][px] = 4  # player
        self.map[ey][ex] = 5  # exit

        for _ in range(3):
            while True:
                x, y = random.randint(1, self.width-2), random.randint(1, self.height-2)
                if self.map[y][x] == 0:
                    self.map[y][x] = 3  # enemy
                    break

        return self.map

    def carve_corridor(self, x1, y1, x2, y2):
        if random.choice([True, False]):
            self.h_corridor(x1, x2, y1)
            self.v_corridor(y1, y2, x2)
        else:
            self.v_corridor(y1, y2, x1)
            self.h_corridor(x1, x2, y2)

    def h_corridor(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map[y][x] = 0

    def v_corridor(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map[y][x] = 0