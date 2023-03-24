import curses

from components import Board, Cursor

def main(stdscr):
    # stdscr.addstr(0, 0, 'Hello World!')
    board = Board(stdscr, [3,4])
    board.play()
    # board(stdscr, 1, 0, [['.']*9]*9)
    # board.render()
    stdscr.getkey()
    # add easy mode

if __name__ == '__main__':
    curses.wrapper(main)