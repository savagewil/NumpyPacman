from typing import List

import numpy as np
from TileValues import TileValues

directions = [
    np.array([-1, 0]),
    np.array([0, -1]),
    np.array([1, 0]),
    np.array([0, 1]),
]

UP = np.array([-1, 0])
DOWN = np.array([1, 0])
LEFT = np.array([0, -1])
RIGHT = np.array([0, 1])
STILL = np.array([0, 0])


class PacmanGameV2:
    def __init__(self, wall_count=5, pacmen=[], seed=None):
        if seed is None:
            seed = int(np.random.random() * 1000)
            # print(f"Seed:{seed}")
        np.random.seed(seed)
        self.wall_count = wall_count
        self.score = 0
        self.pacman_speed = 10
        self.ghost_speed = 8
        self.size = 3 * self.wall_count + 7
        self.walls = np.zeros((self.size, self.size))
        self.pacman = np.array([3, 3])
        self.pacman_direction = STILL
        self.pacman_direction_num = 0
        self.ghosts = [np.array([self.size - 4, 3]),
                       np.array([3, self.size - 4]),
                       np.array([self.size - 4, self.size - 4]),
                       np.array([3, 3])]
        self.ghost_directions: List[np.ndarray] = [STILL, STILL, STILL, STILL]
        self.dots = np.zeros((self.size, self.size))
        self.big_dots = []
        self.wall_chance = 1.0

    def random_pacman_grid(self):
        self.walls = np.zeros_like(self.walls)

        self.walls[0:1, :] = -1
        self.walls[:, 0:1] = -1
        self.walls[-1:, :] = -1

        self.walls[1:3, 1:-2] = 1
        self.walls[1:-2, 1:3] = 1
        self.walls[-3:-1, 1:-2] = 1

        self.walls[3, 3:-4] = -1
        self.walls[3:-4, 3] = -1
        self.walls[3:-4, (self.size // 2)] = -1
        self.walls[-4, 3:-4] = -1
        unmarked = []
        points = []
        for wall_col in range(self.wall_count // 2 + self.wall_count % 2):
            for wall_row in range(self.wall_count):
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

                if ((wall_row != 0 or wall_col < (self.wall_count // 2 - 1)) and
                        ((wall_col < (self.wall_count // 2 - 1) and up_right > 2 and up_left > 2)
                         or
                         (up_right > 3 and up_left > 2))):
                    _directions.append(UP)

                if ((wall_row != self.wall_count - 1 or wall_col < (self.wall_count // 2 - 1)) and
                        ((wall_col < (self.wall_count // 2 - 1) and down_left > 2 and down_right > 2)
                         or
                         (down_left > 2 and down_right > 3))):
                    _directions.append(DOWN)

                if (wall_col < (self.wall_count // 2 - 1) and down_left > 2 and up_left > 2) or (
                        down_left > 2 and up_left > 2):
                    _directions.append(LEFT)

                if ((wall_col < self.wall_count // 2 - 1) and down_right > 2 and up_right > 2) or (
                        self.wall_count % 2 == 0 and
                        down_right > 3 and up_right > 3):
                    _directions.append(RIGHT)

                if _directions:
                    direction = _directions[np.random.randint(0, len(_directions))]
                else:
                    unmarked.append((wall_row, wall_col))
                    direction = np.array([0, 0])
            else:
                direction = np.array([0, 0])

            self.walls[min(row, row + direction[0]):max(row + 2, row + 2 + direction[0]),
            min(col, col + direction[1]):max(col + 2, col + 2 + direction[1])] = 1

        self.walls[:, self.size - self.size // 2:] = np.fliplr(self.walls[:, :self.size // 2])
        self.walls = self.walls + -1 * (self.walls == 0)

        if self.wall_count % 2 == 0:
            wall_col = self.wall_count // 2 - 1
            for wall_row in range(self.wall_count):
                if (wall_row, wall_col) in unmarked:

                    row = 3 * wall_row + 4
                    col = 3 * wall_col + 4

                    down_right = 0
                    up_right = 0

                    for direction in directions:
                        down_right += self.walls[row + 2 + direction[0], col + 2 + direction[1]] != 1
                        up_right += self.walls[row - 1 + direction[0], col + 2 + direction[1]] != 1

                    if down_right > 2 and up_right > 2:
                        direction = RIGHT
                        self.walls[min(row, row + direction[0]):max(row + 2, row + 2 + direction[0]),
                        min(col, col + direction[1]):max(col + 2, col + 2 + direction[1])] = 1
        else:
            wall_col = self.wall_count // 2
            for wall_row in range(self.wall_count):

                if (wall_row, wall_col) in unmarked:
                    row = 3 * wall_row + 4
                    col = 3 * wall_col + 4

                    up_left = 0
                    down_left = 0
                    down_right = 0
                    up_right = 0

                    for direction in directions:
                        up_left += self.walls[row - 1 + direction[0], col - 1 + direction[1]] != 1
                        down_left += self.walls[row + 2 + direction[0], col - 1 + direction[1]] != 1
                        down_right += self.walls[row + 2 + direction[0], col + 2 + direction[1]] != 1
                        up_right += self.walls[row - 1 + direction[0], col + 2 + direction[1]] != 1

                    _directions = []
                    if down_right > 2 and down_left > 2:
                        _directions.append(DOWN)
                    if up_right > 2 and up_left > 2:
                        _directions.append(UP)
                    if _directions:
                        direction = _directions[np.random.randint(0, len(_directions))]
                        self.walls[min(row, row + direction[0]):max(row + 2, row + 2 + direction[0]),
                        min(col, col + direction[1]):max(col + 2, col + 2 + direction[1])] = 1
        self.walls[:, self.size - self.size // 2:] = np.fliplr(self.walls[:, :self.size // 2])

    def get_done(self):
        return any([(ghost == self.pacman).all() for ghost in self.ghosts])

    def fill_dots(self):
        self.dots = np.zeros_like(self.walls) + self.walls < 1

        self.dots[0:1, :] = 0
        self.dots[:, 0:1] = 0
        self.dots[-1:, :] = 0
        self.dots[:, -1:] = 0

        self.big_dots = []
        dots = np.where(self.dots[0:self.size // 2, 0:self.size // 2])
        self.big_dots.append(np.array(list(zip(dots[0], dots[1]))[np.random.randint(0, len(dots[0]))]))
        self.big_dots.append(np.array([self.big_dots[0][0], self.size - 1 - self.big_dots[0][1]]))

        dots = np.where(self.dots[self.size // 2:, 0:self.size // 2])
        dot = list(zip(dots[0], dots[1]))[np.random.randint(0, len(dots[0]))]

        self.big_dots.append(np.array([dot[0] + self.size // 2, dot[1]]))
        self.big_dots.append(np.array([self.big_dots[2][0], self.size - 1 - self.big_dots[2][1]]))

    def move_ghost(self, idx, direction: np.ndarray):
        if self.valid_ghost_direction(idx, direction):
            self.ghost_directions[idx] = direction
            self.ghosts[idx] = self.ghosts[idx] + direction

    def move_pacman(self, direction: np.ndarray, dir_num):
        if self.valid_pacman_direction(direction) and all(directions[dir_num] == direction):
            # print(direction, self.pacman, self.pacman + direction, dir_num)
            self.pacman_direction = direction
            self.pacman = self.pacman + direction
            self.pacman_direction_num = dir_num

    def valid_ghost_direction(self, idx, direction: np.ndarray):
        next_pos = self.ghosts[idx] + direction
        return self.walls[next_pos[0], next_pos[1]] != 1 and not all(direction == -1 * self.ghost_directions[idx])

    def valid_pacman_direction(self, direction: np.ndarray):
        next_pos = self.pacman + direction
        return self.walls[next_pos[0], next_pos[1]] != 1 # and not all(direction == -1 * self.pacman_direction)

    def update(self):
        self.score += self.dots[self.pacman[0], self.pacman[1]]
        self.dots[self.pacman[0], self.pacman[1]] = 0

    def spawn_pacman(self):
        dots = np.where(self.dots[self.size // 4:self.size - self.size // 4,
                        self.size // 4:self.size - self.size // 4])
        self.pacman = np.array(list(zip(dots[0], dots[1]))[np.random.randint(0, len(dots[0]))]) + self.size // 4
