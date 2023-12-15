import numpy as np

from PacmanGame import PacmanGame
from TileValues import TileValues


class PacmanGamePTUIRender():
    def __init__(self, game: PacmanGame):
        self.game = game
        self.size = self.game.size
        self.wall_expander_short = np.zeros((self.size + 1, self.size + self.size + 1))
        for i in range(self.size + 1):
            self.wall_expander_short[i, 2 * i] = 1
            # self.wall_expander_short[i, 2 * i + 2] = 1
            # if i+1 < size - 1:
            #     self.wall_expander[i+1, 2 * i + 1] = 1
        self.wall_expander_long = np.zeros((self.size, self.size + self.size + 1))
        for i in range(self.size):
            self.wall_expander_long[i, 2 * i + 1] = 1
            if 2 * i + 2 < self.size + self.size + 1:
                self.wall_expander_long[i, 2 * i + 2] = 5
            if 2 * i >= 0:
                self.wall_expander_long[i, 2 * i] = 7

        self.cell_expander = np.zeros((self.size, self.size + self.size + 1))
        for i in range(self.size):
            self.cell_expander[i, 2 * i + 1] = 1

    def __str__(self):
        # dots_expanded = self.cell_expander.transpose().dot(self.dots).dot(self.cell_expander)
        h_walls = np.concatenate([np.ones((1, self.size)), self.game.h_walls, np.ones((1, self.size))])
        h_wall_expanded = ((self.wall_expander_short.transpose()).dot(h_walls).dot(
            self.wall_expander_long))

        print(self.wall_expander_short.transpose(),self.wall_expander_short.transpose().shape)
        print()
        print(self.wall_expander_long, self.wall_expander_long.shape)
        print()

        print(h_walls, h_walls.shape)
        print()

        print(h_wall_expanded)
        print()
        print(TileValues.HWALL.value * h_wall_expanded)

        # exit()
        v_walls = np.concatenate([np.ones((self.size, 1)), self.game.v_walls, np.ones((self.size, 1))], axis=1)
        v_wall_expanded = (self.wall_expander_long.transpose().dot(v_walls)).dot(self.wall_expander_short)
        expanded = (TileValues.VWALL.value * v_wall_expanded) + (TileValues.HWALL.value * h_wall_expanded)
        print(v_wall_expanded)
        print()
        print(expanded)
        return ("\n").join(["".join(map(number_to_tile, row)) for row in expanded]) + "\n"
    # └-" + ((self.size * 2 - 1) * "---") + "-┘
    # "┌-" + ((self.size * 2 - 1) * "---") + "-┐\n"


# ("|-" if (i % 2 == 1) and self.game.h_walls[(i - 1) // 2, 0] == 1 else "| ") +
# ("-|" if (i % 2 == 1) and self.game.h_walls[(i - 1) // 2, -1] else " |"

def number_to_tile(v):
    if v == (12 * TileValues.VWALL.value + 12 * TileValues.HWALL.value):
        return "-┼-"
    elif v == (5 * TileValues.VWALL.value + 12 * TileValues.HWALL.value):
        return "-┴-"
    elif v == (7 * TileValues.VWALL.value + 12 * TileValues.HWALL.value):
        return "-┬-"
    elif v == (12 * TileValues.VWALL.value + 5 * TileValues.HWALL.value):
        return "-┤ "
    elif v == (12 * TileValues.VWALL.value + 7 * TileValues.HWALL.value):
        return " ├-"
    elif v == (7 * TileValues.VWALL.value + 7 * TileValues.HWALL.value):
        return " ┌-"
    elif v == (5 * TileValues.VWALL.value + 5 * TileValues.HWALL.value):
        return "-┘ "
    elif v == (5 * TileValues.VWALL.value + 7 * TileValues.HWALL.value):
        return " └-"
    elif v == (7 * TileValues.VWALL.value + 5 * TileValues.HWALL.value):
        return "-┐ "
    elif v == TileValues.VWALL.value:
        return " | "
    elif v == 5 * TileValues.VWALL.value:
        return " | "
    elif v == 7 * TileValues.VWALL.value:
        return " | "
    elif v == TileValues.HWALL.value:
        return "---"
    elif v == 5 * TileValues.HWALL.value:
        return "-- "
    elif v == 7 * TileValues.HWALL.value:
        return " --"
    elif v == TileValues.DOT.value:
        return " o "
    else:
        return "   "


if __name__ == '__main__':
    np.random.seed(100)
    game = PacmanGame(10)
    game.random_walls()
    renderer = PacmanGamePTUIRender(game)
    print(renderer)
