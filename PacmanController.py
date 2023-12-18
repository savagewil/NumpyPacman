import time
from typing import List

import numpy as np

from PacmanGamePTUIRenderV2 import PacmanGamePTUIRenderV2
from PacmanGameV2 import PacmanGameV2
import os
import curses
from curses import wrapper

# now, to clear the screen

directions = [
    np.array([-1, 0]),
    np.array([0, -1]),
    np.array([1, 0]),
    np.array([0, 1]),
]


direction_names = [
    "Up",
    "Left",
    "Down",
    "Right",
]

direction_keys = [
    "w",
    "a",
    "s",
    "d",
]
class PacmanController:
    def __init__(self, game: PacmanGameV2):
        self.game = game

    def step(self, c_key=None):
        # _directions:List[np.ndarray] = []
        # _keys = []
        # _names = []
        _direction = self.game.pacman_direction
        _num = self.game.pacman_direction_num
        # for direction, name, key in zip(directions, direction_names, direction_keys):
        #     if self.game.valid_pacman_direction(direction):
        #         _directions.append(direction)
        #         _keys.append(key)
        #         _names.append(name)
        # if len(_directions) == 1 and all(_directions[0] == self.game.pacman_direction):
        #     self.game.move_pacman(_directions[0], self.game.pacman_direction_num)
        # elif c_
        if (c_key is not None and
                c_key in direction_keys and
                self.game.valid_pacman_direction(directions[direction_keys.index(c_key)])):
            _num = direction_keys.index(c_key)
            _direction = directions[_num]
            # break
        # else:
        #     input_str = input(f"Pick a direction or press enter to stay straight {','.join([f'{name}({key})' for key, name in zip(_keys, _names)])}")
        #     for idx, key in enumerate(_keys):
        #         if key in input_str:
        #             _direction = _directions[idx]
        #             _num = direction_keys.index(key)
        #             break
        self.game.move_pacman(_direction, _num)

def main(window):
    # curses.cbreak()
    window.nodelay(True)

    game = PacmanGameV2(7)
    renderer = PacmanGamePTUIRenderV2(game)
    pacman = PacmanController(game)
    game.random_pacman_grid()
    game.fill_dots()
    game.spawn_pacman()
    # print(renderer)
    saved_key = ""
    for _ in range(1000):

        key = window.getch()
        if key != -1:
            saved_key = chr(key)
        # key = chr(key) if key != -1 else None
        pacman.step(c_key=saved_key)

        window.erase()
        rendered = renderer.__str__()
        window.addstr(0, 0, rendered)
        window.refresh()
        time.sleep(0.2)

        # print()
        # if game.get_done():
        #     print("Boo")
        #     break


if __name__ == '__main__':
    wrapper(main)
