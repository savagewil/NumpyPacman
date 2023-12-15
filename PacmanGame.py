import numpy as np
from TileValues import TileValues


class PacmanGame:
    def __init__(self, size, pacmen=[]):
        self.size = size
        self.h_walls = np.zeros((size - 1, size))
        self.v_walls = np.zeros((size, size - 1))
        self.pacmen = []
        self.ghosts = []
        self.dots = np.zeros((size, size))

    def random_dots(self):

        self.dots = np.random.choice([1, 0], (self.size, self.size))

    def random_walls(self):
        self.h_walls = np.random.choice([1, 0], (self.size - 1, self.size))
        self.v_walls = np.random.choice([1, 0], (self.size, self.size - 1))

    def fill_walls(self):
        self.h_walls = np.ones((self.size - 1, self.size))
        self.v_walls = np.ones((self.size, self.size - 1))




