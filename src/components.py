import curses
import click

from puzzle import SudokuGenerator
from solver import solveBoard

class Cursor():
    def __init__(self, stdscr, option=[0,0]):
        self.stdscr = stdscr
        self.option = option

class Board():
    def __init__(self, stdscr, option=[0,0]):
        self.stdscr = stdscr
        self.cursor = Cursor(stdscr, option)
        self.board = [
            [
                {
                    'value': str(i) if i else ' ',
                    'given': bool(i)
                }
                for i in row
            ]
            for row in SudokuGenerator().generate_puzzle()
        ]
        self.stylings = [curses.COLOR_GREEN]
        self.solution = solveBoard([
            [
                cell['value'] if cell['given'] else '.'
                for cell in row
            ]
            for row in self.board
        ])['board']
        # self.board = [
        #     [
        #         {
        #             'value': str(i),
        #             'given': True
        #         }
        #         for i in row
        #     ]
        #     for row in self.solution
        # ]

    def generate_sudoku(self):
        return [[' ']*9 for i in range(9)]

    def draw(self, row=4, col=2, ):
        self.stdscr.addstr(row-1, col, ' '*18, curses.A_UNDERLINE)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)

        for i in range(9):
            l_styles = curses.A_UNDERLINE + curses.A_BOLD if i % 3 == 0 else curses.A_UNDERLINE
            for j in range(9):
                # print(i + row, j*2+1 + col, self.board[i][j])
                cell = self.board[i][j]
                styles = curses.A_UNDERLINE + curses.color_pair(1) if cell['given'] else curses.A_UNDERLINE
                self.stdscr.addstr(i + row, j*2+1 + col, cell['value'], styles)

                self.stdscr.addstr(i + row, j*2 + col, '|', l_styles)
                # self.stdscr.hline(i*2+1, j*2+1, '_', 1)
            self.stdscr.addstr(i + row, j*2 + 2 + col, '|', l_styles)
        # highlight option in stdscr
        self.stdscr.addstr(self.cursor.option[0] + row, self.cursor.option[1]*2 + 1 + col, self.board[self.cursor.option[0]][self.cursor.option[1]]['value'], curses.A_REVERSE)
        # self.stdscr.addstr(0,0,f'{self.option[0] + row}, {self.option[1]*2 + 1 + col}')
        # mystring = '\n'.join(' '.join(sublist) for sublist in self.board)
        # print(mystring)
        # self.stdscr.addstr(0,60, mystring)
        # click.echo(mystring)

        self.stdscr.refresh()

    def render(self):
        c = 0
        while c != 10:
            if self.solution == self.board:
                self.stdscr.addstr(0,0,'You Win!')
                break
            # self.stdscr.erase()
            # if self.cursor.option == [5,5]:
            #     self.stdscr.addstr(0,0,'You Win!')
            #     break
            self.stdscr.addstr(0,0,f'{self.cursor.option}, {self.board[self.cursor.option[0]][self.cursor.option[1]]["value"]}')
            # self.stdscr.addstr(0,13,f'{c}')
            self.draw()
            c = self.stdscr.getch()  

            match c:
                case curses.KEY_UP:
                    if self.cursor.option[0] > 0:
                        self.cursor.option[0] -= 1
                case curses.KEY_DOWN:
                    if self.cursor.option[0] < 8:
                        self.cursor.option[0] += 1
                case curses.KEY_LEFT:
                    if self.cursor.option[1] > 0:
                        self.cursor.option[1] -= 1
                case curses.KEY_RIGHT:
                    if self.cursor.option[1] < 8:
                        self.cursor.option[1] += 1
                case 127:
                    if not self.board[self.cursor.option[0]][self.cursor.option[1]]['given']:
                        self.board[self.cursor.option[0]][self.cursor.option[1]]['value'] = ' '
                case curses.KEY_DC:
                    if not self.board[self.cursor.option[0]][self.cursor.option[1]]['given']:
                        self.board[self.cursor.option[0]][self.cursor.option[1]]['value'] = ' '
                case num if num in range(49,58):
                    # self.stdscr.addstr(self.cursor.option[0],self.cursor.option[1]+40,f'{self.board[self.cursor.option[0]][self.cursor.option[1]]}')
                    # print(c, self.cursor.option)
                    if not self.board[self.cursor.option[0]][self.cursor.option[1]]['given']:
                        self.board[self.cursor.option[0]][self.cursor.option[1]]['value'] = str(c - 48)
                case _:
                    pass
            
        curses.reset_shell_mode()

    def play(self):
        self.render()