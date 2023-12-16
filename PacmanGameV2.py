import numpy as np
from TileValues import TileValues


class PacmanGameV2:
    def __init__(self, size, pacmen=[]):
        self.size = size
        self.walls = np.zeros((size, size))
        self.pacmen = []
        self.ghosts = []
        self.dots = np.zeros((size, size))

    def random_dots(self):
        self.dots = np.random.choice([1, 0], (self.size, self.size))

    def random_walls(self):
        self.walls = np.random.choice([1, 0], self.walls.shape)

    # def random_pacman(self):
    #     self.walls = np.zeros_like(self.walls)
    #     self.walls[0, :] = 1
    #     self.walls[:, 0] = 1
    #     self.walls[-1, :] = 1
    #     self.walls[1, 1:-2] = -1
    #     self.walls[1:-2, 1] = -1
    #     self.walls[-2, 1:-2] = -1
    #     points = []
    #     for col in range(2, self.size / 2):
    #         for row in range(2, self.size - 2):
    #             points.append((row, col))
    #     np.random.shuffle(points)
    #     for row, col in points:
    #         path_count = 0
    #         corner_path_count = 0
    #         wall_count = 0
    #         for i in [-1,0,1]:
    #             for j in [-1,0,1]:
    #                 wall_count += self.walls[row+i, col+j] == 1
    #                 path_count += self.walls[row+i, col+j] == -1
    #                 corner_path_count += (i!=0 and j!=0) and self.walls[row+i, col+j] == -1
    #         if corner_path_count > 1 and
    #         self.walls[]

    def fill_walls(self):
        self.walls = np.ones_like(self.walls)
