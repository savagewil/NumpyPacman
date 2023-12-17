import numpy as np
from TileValues import TileValues

directions = [
    np.array([0, 1]),
    np.array([0, -1]),
    np.array([1, 0]),
    np.array([-1, 0]),
]
UP = np.array([-1, 0])
DOWN = np.array([1, 0])
LEFT = np.array([0, -1])
RIGHT = np.array([0, 1])


class PacmanGameV2:
    def __init__(self, wall_count=5, pacmen=[], seed=None):
        if seed is not None:
            np.random.seed(seed)
        self.wall_count = wall_count * 2
        self.size = 3 * self.wall_count + 7
        self.walls = np.zeros((self.size, self.size))
        self.pacmen = []
        self.ghosts = []
        self.dots = np.zeros((self.size, self.size))
        self.wall_chance = 1.0

    def random_pacman(self):
        self.walls = np.zeros_like(self.walls)

        self.walls[0:1, :] = -1
        self.walls[:, 0:1] = -1
        self.walls[-1:, :] = -1

        self.walls[1:3, 1:-2] = 1
        self.walls[1:-2, 1:3] = 1
        self.walls[-3:-1, 1:-2] = 1
        self.walls[1:-2, (self.size // 2) + 1:] = 1

        self.walls[3, 3:-4] = -1
        self.walls[3:-4, 3] = -1
        self.walls[3:-4, (self.size // 2)] = -1
        self.walls[-4, 3:-4] = -1

        points = []
        for wall_row in range(self.wall_count):
            for wall_col in range(1 + self.wall_count // 2):
                points.append((wall_row, wall_col))
        np.random.shuffle(points)
        for wall_row, wall_col in points:
            row = 3 * wall_row + 4
            col = 3 * wall_col + 4
            self.walls[row:row + 2, col:col + 2] = 1
            if np.random.random() < self.wall_chance:
                _directions = []

                up_left = 0
                down_left = 0
                down_right = 0
                up_right = 0

                for direction in directions:
                    up_left += self.walls[row - 1 + direction[0], col - 1 + direction[1]] != 1
                    down_left += self.walls[row + 2 + direction[0], col - 1 + direction[1]] != 1
                    down_right += self.walls[row + 2 + direction[0], col + 2 + direction[1]] != 1
                    up_right += self.walls[row - 1 + direction[0], col + 2 + direction[1]] != 1

                # print(f"({wall_row},{wall_col})")
                # print(f"up_left:{up_left} down_left:{down_left} down_right:{down_right} up_right:{up_right}")

                # if wall_row != 0 and \
                if up_right > 2 and up_left > 2:
                    _directions.append(UP)

                # if wall_row != self.wall_count - 1 and\
                if down_left > 2 and down_right > 2:
                    _directions.append(DOWN)

                # if wall_col != 0 and \

                if down_left > 2 and up_left > 2:
                    _directions.append(LEFT)

                if down_right > 2 and up_right > 2:
                    _directions.append(RIGHT)

                if _directions:
                    direction = _directions[np.random.randint(0, len(_directions))]
                else:
                    direction = np.array([0, 0])
            else:
                direction = np.array([0, 0])

            self.walls[min(row, row + direction[0]):max(row + 2, row + 2 + direction[0]),
            min(col, col + direction[1]):max(col + 2, col + 2 + direction[1])] = 1

        self.walls[:, self.size - self.size // 2:] = np.fliplr(self.walls[:, :self.size // 2])
        self.walls = self.walls + -1 * (self.walls == 0)

    def fill_walls(self):
        self.walls = np.ones_like(self.walls)
