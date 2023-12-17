import correlation
from PacmanGameV2 import PacmanGameV2

import numpy as np

from PacmanGame import PacmanGame
from TileValues import TileValues

WALL = 2
UP = 3
DOWN = 5
LEFT = 7
RIGHT = 11

x_kernel = np.array([[-1, 1, 0],
                     [1, 1, 1],
                     [0, 1, -1]])

t_kernel = np.array([[-1, 1, 0],
                     [1, 1, -1],
                     [0, 1, 0]])

corner_kernel = np.array([[0, 0, 0],
                          [0, 1, 1],
                          [0, 1, -1]])

inverse_corner_kernel = np.array([[0, -1, 0],
                                  [-1, 1, 1],
                                  [0, 1, 1]])
edge_kernel = np.array([[0, 0, 0],
                        [0, 1, -1],
                        [0, 0, 0]])


def number_to_tile(v):
    if v == 1:
        return "###"
    elif v == 2:
        return " ┌-"
    elif v == 3:
        return "-┐ "
    elif v == 4:
        return "-┘ "
    elif v == 5:
        return " └-"
    elif v == 6:
        return "---"
    elif v == 7:
        return " | "
    elif v == 8:
        return "-┴-"
    elif v == 9:
        return " ├-"
    elif v == 10:
        return "-┬-"
    elif v == 11:
        return "-┤ "
    if v == 12:
        return "-┼-"
    # elif v == 5 * TileValues.HWALL.value:
    #     return "-- "
    # elif v == 7 * TileValues.HWALL.value:
    #     return " --"
    # elif v == TileValues.DOT.value:
    #     return " o "
    else:
        return "   "


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
        # print(self.game.walls, self.game.walls.shape)
        # walls = np.pad(self.game.walls, pad_width=1, mode='constant', constant_values=1)

        print(self.game.walls.astype(int))
        drawing = np.zeros_like(self.game.walls)

        xs = (correlation.correlate(self.game.walls, x_kernel, 7) * 12 +
              correlation.correlate(self.game.walls, np.rot90(x_kernel), 7) * 12)

        ts = (correlation.correlate(self.game.walls, t_kernel, 6) * 8 +
              correlation.correlate(self.game.walls, np.flipud(t_kernel), 6) * 8 +
              correlation.correlate(self.game.walls, np.rot90(t_kernel), 6) * 9 +
              correlation.correlate(self.game.walls, np.fliplr(np.rot90(t_kernel)), 6) * 9 +
              correlation.correlate(self.game.walls, np.rot90(t_kernel, 2), 6) * 10 +
              correlation.correlate(self.game.walls, np.flipud(np.rot90(t_kernel, 2)), 6) * 10 +
              correlation.correlate(self.game.walls, np.rot90(t_kernel, 3), 6) * 11 +
              correlation.correlate(self.game.walls, np.fliplr(np.rot90(t_kernel, 3)), 6) * 11)

        corners = (correlation.correlate(self.game.walls, corner_kernel, 4) * 2 +
                   correlation.correlate(self.game.walls, np.rot90(corner_kernel), 4) * 3 +
                   correlation.correlate(self.game.walls, np.rot90(corner_kernel, 2), 4) * 4 +
                   correlation.correlate(self.game.walls, np.rot90(corner_kernel, 3), 4) * 5)

        inverse_corners = (correlation.correlate(self.game.walls, inverse_corner_kernel, 6) * 2 +
                           correlation.correlate(self.game.walls, np.rot90(inverse_corner_kernel), 6) * 3 +
                           correlation.correlate(self.game.walls, np.rot90(inverse_corner_kernel, 2), 6) * 4 +
                           correlation.correlate(self.game.walls, np.rot90(inverse_corner_kernel, 3), 6) * 5
                           )
        edges = (
                ((correlation.correlate(self.game.walls, edge_kernel, 2) +
                  correlation.correlate(self.game.walls, np.fliplr(edge_kernel), 2)) > 0) * 6 +
                ((correlation.correlate(self.game.walls, np.rot90(edge_kernel), 2) +
                  correlation.correlate(self.game.walls, np.flipud(np.rot90(edge_kernel)), 2)) > 0) * 7)
        print("edges")
        print(correlation.correlate(self.game.walls, edge_kernel, 2))
        print("")
        print(correlation.correlate(self.game.walls, np.fliplr(edge_kernel), 2))
        drawing = drawing + (drawing == 0) * xs
        drawing = drawing + (drawing == 0) * ts
        drawing = drawing + (drawing == 0) * corners
        drawing = drawing + (drawing == 0) * inverse_corners
        drawing = drawing + (drawing == 0) * edges

        drawing[1:-1, 0] = 7
        drawing[1:-1, -1] = 7
        drawing[0, 1:-1] = 6
        drawing[-1, 1:-1] = 6
        print(drawing)
        print(self.game.walls)

        return "\n".join(["".join([number_to_tile(v) for v in row])
                          for row in drawing]) + "\n"

    def block(self):
        return "\n".join(["".join([number_to_tile(v) for v in row])
                          for row in self.game.walls]) + "\n"


if __name__ == '__main__':
    # np.random.seed(300)
    game = PacmanGameV2(26)
    game.random_pacman()
    renderer = PacmanGamePTUIRenderV2(game)
    print(renderer)
