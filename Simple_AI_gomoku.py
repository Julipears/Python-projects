"""Gomoku starter code provided by Prof. Michael Guerzhoy with tests contributed by Siavash Kazemian.
"""

def is_empty(board):
    for i in range(len(board)):
        if "b" in board[i] or "w" in board[i]:
            return False
    return True

# Loops through every element only once
def is_empty_alt(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i] == "b" or board[i] == "w":
                return False
    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    # Find The starting square
    y_start = y_end - d_y * (length - 1)
    x_start = x_end - d_x * (length - 1)

    # Square coordinates "before" the start
    x_before = x_start - d_x
    y_before = y_start - d_y
    # Square coordinates  "after" the end
    x_after = x_end + d_x
    y_after = y_end + d_y

    # Find the Number of Closed Ends
    closed_end = 0
    
    # Check the square before
    # Out of Bounds Case
    if x_before == -1 or y_before == -1 or x_before == 8 or y_before == 8:
        closed_end += 1
    elif board[y_before][x_before] != " ":
        closed_end += 1

    # Check the square after
    # Out of Bounds Case
    if x_after == -1 or y_after== -1 or x_after == 8 or y_after == 8:
        closed_end += 1
    elif board[y_after][x_after] != " ":
        closed_end += 1
    
    # Return According to the number of closed ends
    if closed_end == 0:
        return "OPEN"
    elif closed_end == 1:
        return "SEMIOPEN"
    else:
        return "CLOSED"


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    # Coordinates of Sqaure we are checking
    cur_x = x_start
    cur_y = y_start 
    
    num_open = 0
    num_semi = 0

    cur_run = 0

    # Iterate through the "row" and find all the valid sequences
    while cur_x != -1 and cur_y != -1 and cur_x != 8 and cur_y != 8:
        if board[cur_y][cur_x] == col:
            cur_run += 1

            # Reached the edge case
            if cur_x + d_x == -1 or cur_y + d_y == -1 or cur_x + d_x == 8 or cur_y + d_y == 8:
                # Valid Sequence is found
                if cur_run == length:
                    result = is_bounded(board, cur_y, cur_x, length, d_y, d_x)
                    if result == "OPEN":
                        num_open += 1
                    elif result == "SEMIOPEN":
                        num_semi += 1
                    # Reset cur_run
                    cur_run = 0
                        
        else:
            # Valid Sequence is found
            if cur_run == length:
                result = is_bounded(board, cur_y-d_y, cur_x-d_x, length, d_y, d_x)
                if result == "OPEN":
                    num_open += 1
                elif result == "SEMIOPEN":
                    num_semi += 1
            # Reset cur_run
            cur_run = 0

        cur_x += d_x
        cur_y += d_y
    
    return (num_open, num_semi)


def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0

    for i in range(8):
        open_seq_count += detect_row(board, col, 0, i, length, 1, 0)[0] # going down the row
        semi_open_seq_count += detect_row(board, col, 0, i, length, 1, 0)[1]

        open_seq_count += detect_row(board, col, i, 0, length, 0, 1)[0] # going down the column
        semi_open_seq_count += detect_row(board, col, i, 0, length, 0, 1)[1]


        open_seq_count += detect_row(board, col, 0, i, length, 1, 1)[0] # top left to bottom right, top right corner half
        semi_open_seq_count += detect_row(board, col, 0, i, length, 1, 1)[1]

        open_seq_count += detect_row(board, col, 0, 7-i, length, 1, -1)[0] # top right to bottem left, top left corner half
        semi_open_seq_count += detect_row(board, col, 0, 7-i, length, 1, -1)[1]

        if i != 0 and i != 7:
        # make sure the center row doesn't repeat
            open_seq_count += detect_row(board, col, 7-i, 0, length, 1, 1)[0] # top left to bottom right, bottom left corner half
            semi_open_seq_count += detect_row(board, col, 7-i, 0, length, 1, 1)[1] 

            open_seq_count += detect_row(board, col, 7-i, 7, length, 1, -1)[0] # top right to bottem left, bottom right corner half
            semi_open_seq_count += detect_row(board, col, 7-i, 7, length, 1, -1)[1] 

    return open_seq_count, semi_open_seq_count


def search_max(board):
    cur_max_score = -1000000
    cur_max_move = -1, -1
    testing_board = make_empty_board(8)
    for i in range(len(board)): # copying over the board
        for j in range(len(board[0])):
            testing_board[i][j] = board[i][j]
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            if testing_board[i][j] == " ":
                testing_board[i][j] = "b"
                temp_score = score(testing_board)
                if temp_score > cur_max_score:
                    cur_max_score = temp_score
                    cur_max_move = i, j
                testing_board[i][j] = " "

    move_y, move_x = cur_max_move  

    return move_y, move_x


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win_helper(board, col):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    win = False

    for d_y, d_x in directions:
        for y in range(8):
            for x in range(8):
                cur_y = y
                cur_x = x 

                # Only Check the Edges
                if cur_y != 0 and cur_x != 0 and cur_y != 7 and cur_x != 7:
                    continue

                # Top Case
                if cur_y == 0:
                    # Don't run horizonal unless its the top left corner
                    if d_y == 0 and d_x == 1:
                        if cur_x != 0:
                            continue
                
                # Left Edge Cases
                if cur_x == 0:
                    # Don't run vertical unless its the top left corner
                    if d_y == 1 and d_x == 0:
                        if cur_y != 0:
                            continue
                
                # Right Edge Cases
                if cur_x == 7:
                    # Don't run vertical unless its the top right corner
                    if d_y == 1 and d_x == 0:
                        if cur_y != 0:
                            continue

                # Bottom Edge
                if cur_y == 7:
                    # Don't run horinzonal unless its bottom left corner
                    if d_y == 0 and d_x == 1:
                        if cur_x != 0:
                            continue
                
                
                cur_run = 0
                # Iterate through the "row" and find all the valid sequences
                while cur_x != -1 and cur_y != -1 and cur_x != 8 and cur_y != 8:
                    if board[cur_y][cur_x] == col:
                        cur_run += 1
                        # Consecutive 5 is found
                        if cur_run == 5:
                            win = True

                        # More than 5 is not considered a win
                        if cur_run > 5:
                            win = False
                    else:
                        # Consecutive 5 is found
                        if cur_run == 5:
                            return True
                        cur_run = 0


                    cur_y += d_y
                    cur_x += d_x
                
                # Check Again (When we run to the edge of the board)
                if cur_run == 5:
                    return True

    # Col has not won yet
    return win


def is_win(board):

    white_win = is_win_helper(board, "w")
    black_win = is_win_helper(board, "b")

    if white_win and black_win:
        # print("ERROR")
        return "ERROR" # This shouldn't happen
    elif white_win:
        # print("White won")
        return "White won"
    elif black_win:
        # print("Black won")
        return "Black won"
    
    # If neither wins
    row = 0 # checking for full board first
    full = True
    while full and row < 8:
        if " " in board[row]:
            full = False
        row += 1

    # Full Board Case
    if full == True:
        # print("Draw")
        return "Draw"
    else:
        # print("Continue playing")
        return "Continue playing"


def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")


def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    print(detect_row(board, "w", y, x, length,d_y,d_x))
    if detect_row(board, "w", y, x, length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")


def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")


def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")


def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()


def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0



def special_tests():
    # Special Test That didn't Pass

    #*0|1|2|3|4|5|6|7*
    #0w| | | | |w| |w*
    #1w| | | |w|w|b| *
    #2 | | | | | |b| *
    #3 |b| | | | |b|w*
    #4w| |w| |b| |b|w*
    #5 |b|b|b|w|w|w|w*
    #6 |b|b| |w| |b|w*
    #7b|b|b| | |w|b|w*

    # Make a test similar but will w on the very right

    board = make_empty_board(8)
    for i in range(5):
        board[3 + i][7] = "w"

    print_board(board)
    print(is_win(board))
    assert(is_win(board) == "White won")
    
    
    '''
    *0|1|2|3|4|5|6|7*
    0b| |w|w| |w| |b*
    1b|b|w|w|b|w|b| *
    2b|b|b|w|w|b|w|w*
    3 |b|w| |w|w|w| *
    4b|b|w| |w|w|w|w*
    5b|w|w|w|w|b|w| *
    6b|w|w| |w|b| | *
    7 |w|w|w|b| | |w*
    *****************'''

    # When there is consecutive 5 and consecutive 6
    # Expected output white win

    board = make_empty_board(8)
    for i in range(6):
        board[2+i][6-i] = "w"
    for i in range(5):
        board[3+i][2] = "w"

    board[0][1] = "b" 

    print_board(board)
    print(is_win(board))
    assert(is_win(board) == "White won")

    # Full column or full row
    board = make_empty_board(8)
    for i in range(8):
        board[i][1] = "w"
    print_board(board)
    print(is_win(board))
    assert(is_win(board) == "Continue playing")

    # More Overline tests
    # A lot in a row
    #*0|1|2|3|4|5|6|7*
    #0w|w|w|b|b| | |w*
    #1w| |b|w|b| | |w*
    #2b|b|b| | | | |b*
    #3 | |w|b|b|w|b|b*
    #4 |b| | | |w|w|b*
    #5 |b|b| | |w|b|b*
    #6 |b| | | |b| |b*
    #7 | | | |b|w| |b*
    #*****************

    board = make_empty_board(8)
    for i in range(6):
        board[2 + i][7] = "b"
    print_board(board)
    print(is_win(board))
    assert(is_win(board) == "Continue playing")


def detect_row_tests():
    board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', 'w', 'w', 'w', 'w', 'w'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b'], [' ', ' ', ' ', ' ', 'b', ' ', ' ', 'b'], [' ', ' ', 'w', ' ', 'b', ' ', 'b', ' '], [' ', 'w', 'w', 'w', 'b', 'b', ' ', 'b'], ['w', ' ', ' ', 'w', 'b', ' ', 'w', ' ']]
    '''
    *0|1|2|3|4|5|6|7*
    0 | | | | | | | *
    1 | | | | | | | *
    2 | | |w|w|w|w|w*
    3 | | | | | | |b*
    4 | | | |b| | |b*
    5 | |w| |b| |b| *
    6 |w|w|w|b|b| |b*
    7w| | |w|b| |w| *
    *****************
    '''

    print_board(board)
    print(detect_rows(board, "b", 2))


if __name__ == '__main__':
    easy_testset_for_main_functions()
    special_tests()
    detect_row_tests()
    some_tests()
    
    play_gomoku(8)
