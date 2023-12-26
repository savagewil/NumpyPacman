import time

import numpy as np

from PacmanGamePTUIRenderV2 import PacmanGamePTUIRenderV2
from PacmanGameV2 import PacmanGameV2
import os

# def cls():
#     print(20 * "\n")


# now, to clear the screen

directions = [
    np.array([-1, 0]),
    np.array([0, -1]),
    np.array([1, 0]),
    np.array([0, 1]),
]


class GhostController:
    def __init__(self, game: PacmanGameV2):
        self.game = game
        self.scatter_points = []
        self.ghost_clock = 0
        self.scatter_time = 7 * self.game.ghost_speed
        self.chase_time = 20 * self.game.ghost_speed
        for row in [3, self.game.size - 4]:
            for col in [3, self.game.size - 4]:
                self.scatter_points.append(np.array([row, col]))

    def step(self):
        now = self.ghost_clock % (self.chase_time + self.scatter_time)
        if self.game.frightened_timer > 0:
            self.frightened()
        else:
            if now < self.chase_time:
                self.chase()
            else:
                self.scatter()
            self.ghost_clock += 1

    def get_target(self, index: int) -> np.ndarray:
        if index == 0:
            return self.game.pacman
        elif index == 1:
            return self.game.pacman + self.game.pacman_direction * 4
        elif index == 2:
            return self.game.pacman if np.linalg.norm(self.game.pacman - self.game.ghosts[2]) >= 8 else \
                self.scatter_points[2]
        elif index == 3:
            return ((self.game.pacman + self.game.pacman_direction * 2) - self.game.ghosts[0]) * 2

    def scatter(self):
        pacman = self.game.pacman
        for ghost_idx, ghost in enumerate(self.game.ghosts):
            pacman = self.scatter_points[ghost_idx]
            best_dir = self.game.ghost_directions[ghost_idx]
            best_dist = self.game.size ** 2
            for direction in directions:
                if self.game.valid_ghost_direction(ghost_idx, direction):
                    step = ghost + direction
                    diff = np.linalg.norm(pacman - step)
                    if diff < best_dist:
                        best_dist = diff
                        best_dir = direction
            self.game.move_ghost(ghost_idx, best_dir)

    def frightened(self):
        pacman = self.game.pacman
        for ghost_idx, ghost in enumerate(self.game.ghosts):
            _directions = []
            for direction in directions:
                if self.game.valid_ghost_direction(ghost_idx, direction):
                    _directions.append(direction)
            if len(_directions) > 1:
                self.game.move_ghost(ghost_idx, _directions[np.random.randint(0, len(_directions))])
            elif len(_directions) == 1:
                self.game.move_ghost(ghost_idx, _directions[0])

    def chase(self):
        for ghost_idx, ghost in enumerate(self.game.ghosts):
            target = self.get_target(ghost_idx)
            best_dir = self.game.ghost_directions[ghost_idx]
            best_dist = self.game.size ** 2
            for direction in directions:
                if self.game.valid_ghost_direction(ghost_idx, direction):
                    step = ghost + direction
                    diff = np.linalg.norm(target - step)
                    if diff < best_dist:
                        best_dist = diff
                        best_dir = direction
            self.game.move_ghost(ghost_idx, best_dir)

# if __name__ == '__main__':
#     game = PacmanGameV2(7)
#     renderer = PacmanGamePTUIRenderV2(game)
#     ghosts = GhostController(game)
#     game.random_pacman_grid()
#     game.fill_dots()
#     game.spawn_pacman()
#     print(renderer)
#     for _ in range(100):
#         ghosts.step()
#         time.sleep(1.0)
#         # cls()
#         print(renderer)
#         if game.get_done():
#             print("Boo")
#             break
