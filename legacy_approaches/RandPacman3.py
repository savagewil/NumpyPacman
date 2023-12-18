import random

import numpy as np
import random as rand

from correlation import correlate_rotated
from PacmanGamePTUIRenderV2 import PacmanGamePTUIRenderV2
from PacmanGameV2 import PacmanGameV2

wall_chance = 1.0
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

if __name__ == '__main__':
    wall_count = 8
    game = PacmanGameV2(2 * wall_count + wall_count + 7)
    render = PacmanGamePTUIRenderV2(game)
    game.walls = np.zeros_like(game.walls)

    game.walls[0:1, :] = -1
    game.walls[:, 0:1] = -1
    game.walls[-1:, :] = -1

    game.walls[1:3, 1:-2] = 1
    game.walls[1:-2, 1:3] = 1
    game.walls[-3:-1, 1:-2] = 1
    game.walls[1:-2, (game.size // 2)+1] = 1


    game.walls[3, 3:-4] = -1
    game.walls[3:-4, 3] = -1
    game.walls[3:-4, (game.size // 2)] = -1
    game.walls[-4, 3:-4] = -1

    points = []
    for wall_row in range(wall_count):
        for wall_col in range(1 + wall_count // 2):
            points.append((wall_row, wall_col))
    np.random.shuffle(points)
    for wall_row, wall_col in points:
        row = 3 * wall_row + 4
        col = 3 * wall_col + 4
        game.walls[row:row + 2, col:col + 2] = 1
        if np.random.random() < wall_chance:
            _directions = []

            up_left = 0
            down_left = 0
            down_right = 0
            up_right = 0

            for direction in directions:
                up_left += game.walls[row - 1 + direction[0], col - 1 + direction[1]] != 1
                down_left += game.walls[row + 2 + direction[0], col - 1 + direction[1]] != 1
                down_right += game.walls[row + 2 + direction[0], col + 2 + direction[1]] != 1
                up_right += game.walls[row - 1 + direction[0], col + 2 + direction[1]] != 1


            if wall_row != 0 and up_right > 2 and up_left > 2:
                _directions.append(UP)

            if wall_row != wall_count-1 and down_left > 2 and down_right > 2:
                _directions.append(DOWN)

            if wall_col != 0 and down_left > 2 and up_left > 2:
                _directions.append(LEFT)

            if down_right > 2 and up_right > 2:
                _directions.append(RIGHT)
            if _directions:
                direction = random.choice(_directions)
            else:
                direction = np.array([0, 0])
        else:
            direction = np.array([0, 0])

        game.walls[min(row, row + direction[0]):max(row + 2, row + 2 + direction[0]),
        min(col, col + direction[1]):max(col + 2, col + 2 + direction[1])] = 1

    game.walls[:, 1 + game.size // 2:] = np.fliplr(game.walls[:, :game.size // 2])
    game.walls = game.walls + -1 * (game.walls == 0)
    print(render)
    print(render.block())
