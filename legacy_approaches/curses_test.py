import time
from curses import wrapper

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    stdscr.addstr(0, 0, '10 divided \n by {} is {}')
    stdscr.refresh()
    time.sleep(10)

    stdscr.refresh()
    stdscr.getkey()

if __name__ == '__main__':
    wrapper(main)