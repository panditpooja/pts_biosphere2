import random

class TerrainGrid:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.goal = (9, 9)
        self.obstacles = set()
        self.crop_zones = {
            (2, 2): "Tomatoes",
            (7, 6): "Corn",
            (4, 4): "Lettuce"
        }
        self.crop_health = {}
        self.generate_obstacles()

    def generate_obstacles(self):
        self.obstacles = set()
        attempts = 0
        while len(self.obstacles) < 15 and attempts < 100:
            x, y = random.randint(0, 9), random.randint(0, 9)
            if (x, y) not in self.crop_zones and (x, y) != (0, 0) and (x, y) != self.goal:
                self.obstacles.add((x, y))
            attempts += 1

    def is_valid(self, position):
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height and position not in self.obstacles

    def reset(self):
        self.generate_obstacles()


class Agent:
    def __init__(self, terrain):
        self.terrain = terrain
        self.start = (0, 0)
        self.goal = terrain.goal
        self.reset()

    def reset(self):
        self.state = self.start
        self.trail = []

    def step(self, action):
        dx, dy = action
        next_pos = (self.state[0] + dx, self.state[1] + dy)
        if self.terrain.is_valid(next_pos):
            self.trail.append(self.state)
            self.state = next_pos
