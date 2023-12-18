import time
from curses import wrapper

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
    elif v == 12:
        return "-┼-"
    elif v == 13:
        return " ᗧ "
    elif v == 14:
        return " ᗤ "
    elif v == 15:
        return " ᗣ "
    elif v == 16:
        return " ᗢ "
    elif v == 17:
        return " Ⴖ "
    elif v == 18:
        return " • "
    elif v == 19:
        return " ◉ "
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

        drawing = drawing + (drawing == 0) * xs
        drawing = drawing + (drawing == 0) * ts
        drawing = drawing + (drawing == 0) * corners
        drawing = drawing + (drawing == 0) * inverse_corners
        drawing = drawing + (drawing == 0) * edges

        drawing = drawing + (drawing == 0) * self.game.dots * 18

        for dot in self.game.big_dots:
            drawing[dot[0], dot[1]] = 19

        drawing[self.game.pacman[0], self.game.pacman[1]] = 13
        for ghost in self.game.ghosts:
            drawing[ghost[0], ghost[1]] = 17

        return f"Score: {self.game.score}\n" + "\n".join(["".join([number_to_tile(v) for v in row])
                          for row in drawing]) + "\n"

    def block(self):
        return "\n".join(["".join([number_to_tile(v) for v in row])
                          for row in self.game.walls]) + "\n"


# if __name__ == '__main__':
#     # 909 9, 502
#     game = PacmanGameV2(7)
#     game.random_pacman_grid()
#     game.fill_dots()
#     renderer = PacmanGamePTUIRenderV2(game)
#     print(renderer)

def main(window):
    window.clear()
    game = PacmanGameV2(7)
    game.random_pacman_grid()
    renderer = PacmanGamePTUIRenderV2(game)
    str_ = renderer.__str__()
    for i in range(20):
        window.addstr(0, 0, str_)
        window.refresh()
        time.sleep(1)
    # This raises ZeroDivisionError when i == 10.


if __name__ == '__main__':
    wrapper(main)