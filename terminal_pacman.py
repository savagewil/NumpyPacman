import time
from curses import wrapper

from GhostController import GhostController
from PacmanController import PacmanController
from PacmanGamePTUIRenderV2 import PacmanGamePTUIRenderV2
from PacmanGameV2 import PacmanGameV2


def end(window, renderer, game):
    for _ in range(1000):
        key = window.getch()
        window.clear()
        window.addstr(0, 0, renderer.__str__())
        window.addstr(game.size // 2 - 3, 3 * game.size // 2 - 11, f"                       ")
        window.addstr(game.size // 2 - 2, 3 * game.size // 2 - 11, f"  ┌-----------------┐  ")
        window.addstr(game.size // 2 - 1, 3 * game.size // 2 - 11, f"  |     Game over   |  ")
        window.addstr(game.size // 2, 3 * game.size // 2 - 11, f"  | Final Score:{str(game.score).zfill(3)} |  ")
        window.addstr(game.size // 2 + 1, 3 * game.size // 2 - 11, f"  | Press x to exit |  ")
        window.addstr(game.size // 2 + 2, 3 * game.size // 2 - 11, f"  └-----------------┘  ")
        window.addstr(game.size // 2 + 3, 3 * game.size // 2 - 11, f"                       ")
        window.refresh()
        time.sleep(0.2)
        if key != -1 and chr(key) == "x":
            break


def start(window, renderer, game):
    # window.addstr(0, 0, renderer.__str__())
    # window.refresh()
    for _ in range(1000):
        key = window.getch()
        window.clear()
        window.addstr(0, 0, renderer.__str__())
        window.addstr(game.size // 2 - 3, 3 * game.size // 2 - 11, f"                       ")
        window.addstr(game.size // 2 - 2, 3 * game.size // 2 - 11, f"  ┌-----------------┐  ")
        window.addstr(game.size // 2 - 1, 3 * game.size // 2 - 11, f"  | TERMINAL PACMAN |  ")
        window.addstr(game.size // 2, 3 * game.size // 2 - 11, f"  | William  Savage |  ")
        window.addstr(game.size // 2 + 1, 3 * game.size // 2 - 11, f"  |  wasd to start  |  ")
        window.addstr(game.size // 2 + 2, 3 * game.size // 2 - 11, f"  └-----------------┘  ")
        window.addstr(game.size // 2 + 3, 3 * game.size // 2 - 11, f"                       ")
        window.refresh()
        time.sleep(0.2)
        if key != -1 and (chr(key) == "w" or chr(key) == "a" or chr(key) == "s" or chr(key) == "d"):
            saved_key = chr(key)
            break
    return saved_key


def death(window, renderer, game):
    game.lives -= 1
    saved_key = ""
    for dir in range(4):
        dir = dir % 4 + 7
        game.pacman_direction_num = dir
        window.addstr(0, 0, renderer.__str__())
        window.refresh()
        time.sleep(0.2)
    return saved_key


def pause(window, renderer, game):
    while True:
        key = window.getch()
        window.clear()
        window.addstr(0, 0, renderer.__str__())
        window.addstr(game.size // 2 - 3, 3 * game.size // 2 - 12, f"                       ")
        window.addstr(game.size // 2 - 2, 3 * game.size // 2 - 12, f"  ┌-------------------┐  ")
        window.addstr(game.size // 2 - 1, 3 * game.size // 2 - 12, f"  |       Paused      |  ")
        window.addstr(game.size // 2, 3 * game.size // 2 - 12, f"  | Current Score:{str(game.score).zfill(3)} |  ")
        window.addstr(game.size // 2 + 1, 3 * game.size // 2 - 12, f"  |  Press f to exit  |  ")
        window.addstr(game.size // 2 + 2, 3 * game.size // 2 - 12, f"  └-------------------┘  ")
        window.addstr(game.size // 2 + 3, 3 * game.size // 2 - 12, f"                       ")
        window.refresh()
        time.sleep(0.2)
        if key != -1 and chr(key) == "f":
            break

# def game_loop(window, renderer, game, saved_key):


def main(window):
    # curses.cbreak()
    tick_per_second = 100
    window.nodelay(True)

    game = PacmanGameV2(9)
    renderer = PacmanGamePTUIRenderV2(game)
    pacman = PacmanController(game)
    ghosts = GhostController(game)
    game.random_pacman_grid()
    game.fill_dots()
    game.spawn_pacman(fresh=True)

    saved_key = start(window, renderer, game)

    while game.lives:
        # print(renderer)

        game.spawn_pacman()
        game.spawn_ghosts()

        for clock in range(10000):

            key = window.getch()
            if key != -1:
                if chr(key) == "f":
                    pause(window, renderer, game)
                else:
                    saved_key = chr(key)


            # key = chr(key) if key != -1 else None
            if clock % (tick_per_second // game.pacman_speed) == 0:
                pacman.step(c_key=saved_key)
                if game.get_done():
                    break

            if clock % (tick_per_second // game.ghost_speed) == 0:
                ghosts.step()
                if game.get_done():
                    break
            game.update()

            window.clear()
            window.addstr(0, 0, renderer.__str__())
            window.refresh()
            time.sleep(1.0 / tick_per_second)
        saved_key = death(window, renderer, game)
    end(window, renderer, game)

    # print()


if __name__ == '__main__':
    wrapper(main)
