from PacmanGameV2 import PacmanGameV2

import numpy as np

from PacmanGame import PacmanGame
from TileValues import TileValues

WALL = 2
UP = 3
DOWN = 5
LEFT = 7
RIGHT = 11


class PacmanGamePTUIRenderV2():
    def __init__(self, game: PacmanGameV2):
        self.game = game
        self.size = self.game.size
        self.right_matrix = np.zeros((self.size + 2, self.size + 2))
        self.up_matrix = np.zeros((self.size + 2, self.size + 2))
        self.down_matrix = np.zeros((self.size + 2, self.size + 2))
        self.left_matrix = np.zeros((self.size + 2, self.size + 2))
        for i in range(1, self.size + 2):
            self.right_matrix[i, i - 1] = 1
        for i in range(1, self.size + 2):
            self.up_matrix[i, i - 1] = 1
        for i in range(0, self.size + 1):
            self.down_matrix[i, i + 1] = 1
        for i in range(0, self.size + 1):
            self.left_matrix[i, i + 1] = 1

    def __str__(self):
        # dots_expanded = self.cell_expander.transpose().dot(self.dots).dot(self.cell_expander)
        print(self.game.walls, self.game.walls.shape)
        # walls = np.pad(self.game.walls, pad_width=1, mode='constant', constant_values=1)
        return "\n".join(["".join(['###' if v == 1 else "+++" if v == -1 else "   " for v in row])
                            for row in self.game.walls]) + "\n"


if __name__ == '__main__':
    np.random.seed(100)
    game = PacmanGameV2(26)
    game.random_pacman()
    renderer = PacmanGamePTUIRenderV2(game)
    print(renderer)
