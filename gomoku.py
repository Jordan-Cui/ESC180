"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Nov. 1, 2023
"""
import copy

def is_empty(board):
    if board == make_empty_board(len(board)):
        return True
    return False
    
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    #stone = board[y_end][x_end]
    y_start = y_end - (d_y * length)
    x_start = x_end - (d_x * length)
    #print(y_start, x_start)
    y_end += d_y
    x_end += d_x
    #print(y_end, x_end)
    ub = len(board) - 1
    
    numOpen = 2

    if y_start < 0 or y_start > ub or x_start < 0 or x_start > ub:
        numOpen -= 1
    elif board[y_start][x_start] != " ":
        numOpen -= 1
    if y_end < 0 or y_end > ub or x_end < 0 or x_end > ub:
        numOpen -= 1
    elif board[y_end][x_end] != " ":
        numOpen -= 1
    
    match numOpen:
        case 2:
            return "OPEN"
        case 1:
            return "SEMIOPEN"
        case 0:
            return "CLOSED"
        case _:
            return "BIG PROBLEM"
    
    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    ub = len(board)

    seq = 0
    #consecutive = False
    while y_start < ub and y_start > -1 and x_start < ub and x_start > -1:
        if board[y_start][x_start] == col:
            seq += 1
            #consecutive = True
        else:
            if seq == length:
                bound = is_bounded(board, y_start - d_y, x_start - d_x, length, d_y, d_x)
                if bound == "OPEN":
                    open_seq_count += 1
                elif bound == "SEMIOPEN":
                    semi_open_seq_count += 1
            #consecutive = False
            seq = 0
        y_start += d_y
        x_start += d_x
    
    if seq == length:
        bound = is_bounded(board, y_start - d_y, x_start - d_x, length, d_y, d_x)
        if bound == "OPEN":
            open_seq_count += 1
        elif bound == "SEMIOPEN":
            semi_open_seq_count += 1


    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0
    #LOTS OF DOUBLE COUNTING HERE FIX!!!

    #Rows starting from top edge
    for x_start in range(len(board)):
        for d_y, d_x in [[1, 0], [1, 1], [1, -1]]:
            temp1, temp2 = detect_row(board, col, 0, x_start, length, d_y, d_x)
            open_seq_count += temp1
            semi_open_seq_count += temp2
    
    #Rows starting from left edge
    #Start at 1 to avoid double counting diagonal row
    #Add extra lines to count first horizontal
    temp1, temp2 = detect_row(board, col, 0, 0, length, 0, 1)
    open_seq_count += temp1
    semi_open_seq_count += temp2
    
    for y_start in range(1, len(board)):
        for d_y, d_x in [[0, 1], [1, 1]]:
            temp1, temp2 = detect_row(board, col, y_start, 0, length, d_y, d_x)
            open_seq_count += temp1
            semi_open_seq_count += temp2

    #Rows starting from right edge
    #Start at 1 to avoid double counting diagonal row starting at (0, len(board) - 1)
    for y_start in range(1, len(board)):
        for d_y, d_x in [[1, -1]]:
            temp1, temp2 = detect_row(board, col, y_start, len(board) - 1, length, d_y, d_x)
            open_seq_count += temp1
            semi_open_seq_count += temp2

    return open_seq_count, semi_open_seq_count
    
def search_max(board):
    maxscore = -100001
    move_y, move_x = 0, 0

    for i in range(len(board)):
        for j in range(len(board)):
            if(board[i][j] == " "):
                board[i][j] = "b"
                temp = score(board)
                if(temp > maxscore):
                    maxscore = temp
                    move_y, move_x = i, j
                board[i][j] = " "

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

def win(board, col):
    boardcopy = copy.deepcopy(board)
    for i in range(len(boardcopy)):
        boardcopy[i].extend([" ", " "])
    boardcopy.insert(0, [" "] * len(boardcopy[0]))
    boardcopy.append([" "] * len(boardcopy[0]))

    for i in range(len(boardcopy)):
        for j in range(len(boardcopy)):
            if boardcopy[i][j] != col:
                boardcopy[i][j] = " "
    open_seq_count, closed_seq_count = detect_rows(boardcopy, col, 5)
    return open_seq_count > 0 or closed_seq_count > 0



def is_win(board):

    if win(board, "w"):
        return "White won"
    if win(board, "b"):
        return "Black won"
    draw = False
    for i in board:
        if not " " in i:
            draw = True
    if draw:
        return "Draw"
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
    x = 0; y = 0; d_x = 1; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    board[3][3] = "b"
    print_board(board)
    
    y_end = 2
    x_end = 2

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'CLOSED':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    put_seq_on_board(board, 5, 5, 1, 0, 3, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,1):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 1; y = 0; d_x = 1; d_y = 0; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
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
    board[0][6] = "w"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")

    print_board(board)

    analysis(board)
    print_board(board)

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
            
if __name__ == '__main__':
    #play_gomoku(8)
    #test_is_bounded()
    #test_detect_row()
    #test_detect_rows()
    #test_search_max()
    #some_tests()
    board = make_empty_board(5)
    put_seq_on_board(board, 0, 0, 1, 1, 5, "b")
    print_board(board)
    print(is_win(board))
