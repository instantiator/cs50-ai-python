"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    blanks = 0
    for row in board:
        blanks += row.count(EMPTY)
    if blanks % 2 == 1:
        return X  # ODD blanks for X eg. 9 blanks, X goes first
    else:
        return O  # EVEN blanks for O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    # step through board
    for i in range(len(board)):
        for j in range(len(board[i])):
            # an empty cell is a potential action
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    mark = player(board)
    (i, j) = action
    if i < 0 or i > len(board) or j < 0 or j > len(board[i]):
        raise Exception("Out of bounds")
    if board[i][j] != EMPTY:
        raise Exception("Invalid move")
    new_board = copy.deepcopy(board)
    new_board[i][j] = mark
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # ok, I over-engineered this
    # it's looking for a chain of 3 that fits on the board from the starting position
    win_length = 3
    # these are all the directions it can search
    directions = [
        (-1, 0),
        (-1, -1),
        (0, -1),
        (1, -1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1),
    ]
    # step through the board
    for i in range(len(board)):
        for j in range(len(board[i])):
            # look at the token in the cell
            token = board[i][j]
            # if it's not empty, explore it for all possible win chains
            if token != EMPTY:
                # every direction
                for direction in directions:
                    # check if there's a win from this cell in that direction
                    win = check_win_chain(board, token, (i, j), direction, win_length)
                    if win:
                        return token
    return None


def check_win_chain(board, token, start, direction, length):
    """
    Returns true if there's a win chain from the given starting position, in the given direction.
    Configurable for length of winning chains, for if the board weren't fixed.
    """
    pos = start
    found = 0
    # stay within the bounds of the board
    while (
        pos[0] >= 0
        and pos[0] < len(board)
        and pos[1] >= 0
        and pos[1] < len(board[pos[0]])
    ):
        # if the cell doesn't match the player's token, it's not a win
        if board[pos[0]][pos[1]] != token:
            return False
        else:
            # count the length of the chain
            found += 1
            # if it's long enough, it's a win
            if found == length:
                return True
        # continue moving along the chain
        pos = (pos[0] + direction[0], pos[1] + direction[1])
    return False


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if there's a winner, or no more moves, the game is over
    return (winner(board) is not None) or (len(actions(board)) == 0)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # a simple utility function based on the winner
    win = winner(board)
    utility = 1 if win == X else -1 if win == O else 0
    return utility


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        # X wants to maximise, O wants to minimise
        # each function returns a value and an action
        if player(board) == X:
            (v, action) = max_value_and_move(board)
            return action
        else:
            (v, action) = min_value_and_move(board)
            return action


def max_value_and_move(board):
    if terminal(board):
        return (utility(board), None)
    best_v = -math.inf
    best_move = None
    # check each action on the board
    for action in actions(board):
        new_board = result(board, action)
        v = max(best_v, min_value_and_move(new_board)[0])
        # if this is better than the move that came before
        # keep it, and continue to check the rest
        if v > best_v:
            best_v = v
            best_move = action
    return (best_v, best_move)


def min_value_and_move(board):
    if terminal(board):
        return (utility(board), None)
    best_v = math.inf
    best_move = None
    # check each action on the board
    for action in actions(board):
        new_board = result(board, action)
        v = min(best_v, max_value_and_move(new_board)[0])
        # if this is better than the move that came before
        # keep it, and continue to check the rest
        if v < best_v:
            best_v = v
            best_move = action
    return (best_v, best_move)
