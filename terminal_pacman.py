import time
from curses import wrapper

from GhostController import GhostController
from PacmanController import PacmanController
from PacmanGamePTUIRenderV2 import PacmanGamePTUIRenderV2
from PacmanGameV2 import PacmanGameV2


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
    game.spawn_pacman()
    # print(renderer)
    saved_key = ""
    for clock in range(10000):

        key = window.getch()
        if key != -1:
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
        rendered = renderer.__str__()
        window.addstr(0, 0, rendered)
        window.refresh()
        time.sleep(1.0/tick_per_second)


        # print()


    for _ in range(1000):
        key = window.getch()
        # window.clear()
        window.addstr(game.size//2-3, 3 * game.size//2 - 10, f"                     ")
        window.addstr(game.size//2-2, 3 * game.size//2 - 10, f" ┌-----------------┐ ")
        window.addstr(game.size//2-1, 3 * game.size//2 - 10, f" |     Game over   | ")
        window.addstr(game.size//2, 3 * game.size//2 - 10,   f" | Final Score:{str(game.score).zfill(3)} | ")
        window.addstr(game.size//2+1, 3 * game.size//2 - 10, f" | Press x to exit | ")
        window.addstr(game.size//2+2, 3 * game.size//2 - 10, f" └-----------------┘ ")
        window.addstr(game.size//2+3, 3 * game.size//2 - 10, f"                     ")
        window.refresh()
        time.sleep(0.2)
        if key != -1 and chr(key) == "x":
            break

if __name__ == '__main__':
    wrapper(main)
