import copy

def solveSudoku(board):
    first_attempt = solveBoard(copy.deepcopy(board))
    # board = first_attempt
    print(first_attempt)
    if first_attempt['stuck']:
        if not first_attempt['failed']:
            first = first_attempt['empty'][0]
            r, c, s = get_filled(first_attempt['rows'], first_attempt['columns'], first_attempt['squares'], first)
            unav = r | c | s
            options = (1 << 9) - 1 - unav
            guesses = tuple(
                i + 1
                for i, guess in enumerate(reversed(bin(options)[2:]))
                if guess == '1'
            )
            print(guesses, '|||||||', options, "||||||", unav)
            for guess in guesses:
                print(guess, 'bbbbbbbbbb', len(guesses))
                board_copy = copy.deepcopy(first_attempt["board"])
                # print()
                board_copy[first[0]][first[1]] = str(guess)
                # only mutates board_copy
                next_attempt = solveSudoku(board_copy)
                # if not next_attempt['stuck']:
                #     return next_attempt
                # elif next_attempt['failed']:
                #     continue
                
                if type(next_attempt) == str:
                    pass
                # elif next_attempt['stuck']:
                #     solveSudoku(board_copy)
                else:
                    for i, r in enumerate(next_attempt):
                        board[i] = r
                    break
            else:
                print('tried all', guesses)
                return 'failed'
        else:
            print('failieds')
            return 'failed'
            
    else:
        for i, r in enumerate(first_attempt['board']):
            board[i] = r

    return board

def solveBoard(board):
    rows, columns, squares = calcFilled(board)
    empty = list()
    for r, row in enumerate(board):
        for c, n in enumerate(row):
            if n == '.':
                empty.append((r, c))

    # print(rows)
    # print(columns)
    # print(squares, len(empty))
    # print(empty)
    c = 0
    while len(empty) > 0:
        empty_copy = empty.copy()
        for i, sq in enumerate(empty):
            row, col, square = get_filled(rows, columns, squares, sq)
            unav = row | col | square
            options = (1 << 9) - 1 - unav
            option = options.bit_length()
            # # print(option, options, square, sq)
            # print(unav, option, options, sq, row, col, square, int(options.bit_count()), 'aaa')
            # # print(i)
            # if 1 << option - 1 == options:
            if options.bit_count() == 1:
                sqloc = 3*(sq[0]//3) + (sq[1]//3)
                # print(unav, option, options, sq, (row), (col), (square), sqloc, 'bb')
                board[sq[0]][sq[1]] = str(option)
                # empty_copy.pop(i)
                empty_copy[i] = None
                rows[sq[0]] += 1 << (option - 1)
                columns[sq[1]] += 1 << (option - 1)
                squares[3*(sq[0]//3) + (sq[1]//3)] += 1 << (option - 1)
                c += 1
                # print(c, len(empty), len(empty_copy))
                # # print(empty)
                # break
            elif options.bit_count() == 0:
                return {
                'stuck': True,
                'failed': True,
                'board': board,
                'empty': empty,
                'options': options,
                'rows': rows,
                'columns': columns,
                'squares': squares
            }
        # break
        # # print(empty)
        not_none = list(filter(
            lambda e: e != None,
            empty_copy
        ))
        if len(not_none) == len(empty) and len(empty) > 0: 
            #  guess
            test = empty[0]

            return {
                'stuck': True,
                'failed': False,
                'board': board,
                'empty': empty,
                'options': options,
                'rows': rows,
                'columns': columns,
                'squares': squares
            }
        empty = not_none
        # # print

    # # print(empty)

    # # print(rows)
    # # print(columns)
    # # print(squares)
    # # print(empty)
    return {
        'stuck': False,
        'failed': False,
        'board': board
    }
def calcFilled(board):
    rows = {
            i: sum(
                1 << int(n) - 1
                for n in row 
                if n != '.'
            )
            for i, row in enumerate(board)
        }
    columns = {
        i: sum(
            1 << int(board[j][i]) - 1
            for j in range(9)
            if board[j][i] != '.'
        )
        for i in range(9)
    }
    squares = {
        i: sum(
            1 << int(board[j//3 + 3*(i//3)][j%3 + 3*(i%3)]) - 1
            for j in range(9)
            if board[j//3 + 3*(i//3)][j%3 + 3*(i%3)] != '.'
        )
        for i in range(9)
    }
    return (rows, columns, squares)

def get_filled(rows, columns, squares, sq):
     
    row = rows[sq[0]]
    col = columns[sq[1]]
    # # print(sq)
    sqloc = 3*(sq[0]//3) + (sq[1]//3)
    square = squares[sqloc]
    return(row, col, square)