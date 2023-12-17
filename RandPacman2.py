import numpy as np
import random as rand

from correlation import correlate_rotated
from PacmanGamePTUIRenderV2 import PacmanGamePTUIRenderV2
from PacmanGameV2 import PacmanGameV2

path_kernel = np.array([[-1, -1, -1],
                        [-1, -1, -1],
                        [-1, -1, -1]])

spiral_kernel = np.array([[0, -1, 0, 0, 0],
                          [0, -1, -1, -1, 0],
                          [-1, -1, -1, 0, 0],
                          [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]])

spiral2_kernel = np.array([[0, -1, 0, 0, 0],
                           [0, -1, -1, -1, 0],
                           [0, -1, -1, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0]])

wall_trimmer_kernel = np.array([[0, 0, 0, 0, 0],
                               [0, 1, 1, 1, 0],
                               [0, -1, 1, -1, 0],
                               [0, 0, -1, 0, 0],
                               [0, 0, 0, 0, 0]])

wall_filler_kernel = np.array([[0, 0, 0, 0, 0],
                               [0, 0, 1, 1, -1],
                               [0, 0, -1, 1, -1],
                               [0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0]])

wall_filler2_kernel = np.array([[0, 0, 1, 1, -1],
                                [0, 0, -1, 1, -1],
                                [0, 0, -1, 1, -1],
                                [0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0]])

corner_kernel = np.array([[-1, -1, 0],
                          [-1, 0, 0],
                          [0, 0, 0]])

trapped_kernel = np.array([[0, 0, 0],
                           [0, 1, -1],
                           [1, -1, 1]])

corner_kernel2 = np.array([[0, 0, 0, 0, 0],
                           [-1, -1, 0, 0, 0],
                           [-1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0]])
corner_kernel3 = np.array([[-1, -1, 0, 0, 0],
                           [-1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0]])

dead_kernel = np.array([[0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 1, 1, 1, 0],
                        [0, 1, -1, 1, 0],
                        [0, 0, 0, 0, 0]])

dead_kernel2 = np.array([[0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 1, -1, 1, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0]])

long_wall_kernel = np.array([[0, 0, 1, 1, 0],
                             [0, 0, 1, 1, 0],
                             [0, 0, 1, 1, 0],
                             [0, 0, 1, 1, 0],
                             [0, 0, 1, 1, 0]])


def fill_walls(game):
    new_walls = (correlate_rotated(game.walls, path_kernel, 9))
    game.walls = game.walls * (1 - new_walls) + new_walls

    new_walls = (correlate_rotated(game.walls, spiral2_kernel))
    game.walls = game.walls * (1 - new_walls) + new_walls

    new_walls = 1 * ((correlate_rotated(game.walls, corner_kernel, 3) +
                      correlate_rotated(game.walls, corner_kernel2, 3) +
                      correlate_rotated(game.walls, corner_kernel3, 3)) > 0)

    game.walls = game.walls * (1 - new_walls) + new_walls

    new_walls = (correlate_rotated(game.walls, wall_filler_kernel))
    game.walls = game.walls * (1 - new_walls) + new_walls
    new_walls = (correlate_rotated(game.walls, wall_filler2_kernel))
    game.walls = game.walls * (1 - new_walls) + new_walls


def fill_deads(game):
    new_paths = (correlate_rotated(game.walls, dead_kernel, 6))
    print("deads")
    print(new_paths)
    game.walls = game.walls * (1 - new_paths) - new_paths


def fill_paths(game):
    # new_paths = (correlate_rotated(game.walls, dead_kernel, 4))
    #
    # game.walls = game.walls * (1 - new_paths) - new_paths

    new_paths = (correlate_rotated(game.walls, trapped_kernel, 5))
    game.walls = game.walls * (1 - new_paths) - new_paths
    print("break walls")
    print(game.walls)
    new_paths = (correlate_rotated(game.walls, long_wall_kernel, 9))
    print(new_paths)
    print()
    game.walls = game.walls * (1 - new_paths) - new_paths

    fill_deads(game)


if __name__ == '__main__':
    # np.random.seed(155)
    game = PacmanGameV2(20)
    render = PacmanGamePTUIRenderV2(game)
    game.walls = np.zeros_like(game.walls)
    game.walls[0, :] = 1
    game.walls[:, 0] = 1
    game.walls[-1, :] = 1
    game.walls[1, 1:-2] = -1
    game.walls[1:-2, 1] = -1
    game.walls[1:-2, (game.size // 2)] = -1
    game.walls[-2, 1:-2] = -1

    points = []
    for col in range(2, game.size // 2):
        points.append((2, col))
        points.append((game.size - 3, col))

    for row in range(2, game.size - 2):
        if not (row, 2) in points:
            points.append((row, 2))
    print(points)

    fill_walls(game)
    fill_paths(game)
    while points:
        row, col = points.pop(np.random.randint(len(points)))
        if game.walls[row, col] != 0: continue
        game.walls[row, col] = -1
        fill_walls(game)
        fill_paths(game)
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if game.walls[row + i, col + j] == 0 and not (row + i, col + j) in points:
                    points.append((row + i, col + j))
    fill_paths(game)

    for i in range(5):
        new_walls = ((correlate_rotated(game.walls, wall_filler_kernel)) + (correlate_rotated(game.walls, wall_filler2_kernel))) > 0
        print("filling")
        print(new_walls)
        game.walls = game.walls * (1 - new_walls) + new_walls


        new_walls = (correlate_rotated(game.walls, dead_kernel2))
        print("filling")
        print(new_walls)
        game.walls = game.walls * (1 - new_walls) + new_walls


    new_walls = (correlate_rotated(game.walls,wall_trimmer_kernel )) > 0
    print("trimming")
    print(new_walls)
    game.walls = game.walls * (1 - new_walls) - new_walls

    game.walls[:, game.size // 2:] = np.fliplr(game.walls[:, :game.size // 2])
    game.walls = game.walls + -1 * (game.walls == 0)
    # game.walls = game.walls > 0
    print(render)
    print(render.block())
