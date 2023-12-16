import numpy as np
import random as rand
from PacmanGamePTUIRenderV2 import PacmanGamePTUIRenderV2
from PacmanGameV2 import PacmanGameV2

if __name__ == '__main__':
    game = PacmanGameV2(26)
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
    print(render)
    for col in range(2, game.size // 2):
        points.append((2, col))
        points.append((game.size - 3, col))

    for row in range(2, game.size - 2):
        if not (row, 2) in points:
            points.append((row, 2))
    print(points)
    while points:
        print()
        row, col = points.pop(np.random.randint(len(points)))
        print((row, col))
        path_count = 0
        corner_path_count = 0
        wall_count = 0
        new_points = []
        paths = np.zeros((3, 3))
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i != 0 or j != 0:
                    wall_count += game.walls[row + i, col + j] == 1
                    path_count += game.walls[row + i, col + j] == -1
                    paths[1+i, 1+j] = game.walls[row + i, col + j] == -1
                    if game.walls[row + i, col + j] == 0 and col + j <= game.size // 2:
                        new_points.append((row + i, col + j))
                    corner_path_count += (i != 0 and j != 0) and game.walls[row + i, col + j] == -1
        if path_count >= 5:
            print("path_count >= 5")
            game.walls[row, col] = 1
            continue
        print(paths)
        for i in [0, 2]:
            if (paths[i, i] and paths[i, 1] and paths[1, i]) or (paths[i, 2 - i] and paths[i, 1] and paths[1, 2 - i]):
                game.walls[row, col] = 1
                print("corner")
                break
        if game.walls[row, col] == 1:
            continue
        if path_count == 1:
            print("path_count == 1")
            game.walls[row, col] = -1
            for point in new_points:
                if not point in points:
                    points.append(point)
            continue
        else:
            print("else")
            game.walls[row, col] = -1  # np.random.choice([1, -1])
            for point in new_points:
                if not point in points:
                    points.append(point)
        # input("test")

    # for row, col in points:
    #     path_count = 0
    #     corner_path_count = 0
    #     wall_count = 0
    #     for i in [-1, 0, 1]:
    #         for j in [-1, 0, 1]:
    #             wall_count += game.walls[row + i, col + j] == 1
    #             path_count += game.walls[row + i, col + j] == -1
    #             corner_path_count += (i != 0 and j != 0) and game.walls[row + i, col + j] == -1
    #     if corner_path_count > 1 and path_count > 3:
    #         game.walls[row, col] = 1
    for col in range(2, game.size // 2):
        for row in range(2, game.size - 2):
            if game.walls[row, col] == -1:
                path_count = 0
                corner_path_count = 0
                wall_count = 0
                nexts = [(row, col)]
                while nexts:
                    row, col = nexts.pop(0)
                    for i, j in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                        if game.walls[row + i, col + j] == -1:
                            nexts.append((row + i, col + j))
                    if len(nexts) > 1:
                        nexts = []
                    else:
                        game.walls[row, col] = 1
    game.walls[:, game.size // 2:] = np.fliplr(game.walls[:, :game.size // 2])
    game.walls = game.walls> 0
    print(render)
