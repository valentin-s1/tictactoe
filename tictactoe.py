import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns the initial state of the playing board as a 3x3 array.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Return the player whose turn it currently is based on the playing field.

    Parameters:
    board (array): the playing board as a 3x3 array 

    Returns:
    string:     "X" for even number of moves played 
                "O" for odd number of moves played
    """

    #if the board is empty it is X's turn
    if board == initial_state():
        return X
    
    #for every entry on the board that is not empty we add one to the move count (moves played)
    num_moves = 0
    rows = [0,1,2]
    for row in rows:
        for entry in board[row]:
            if entry is not EMPTY:
                num_moves += 1

    #for an even number of moves played, it is X's turn
    if num_moves%2 == 0:
        return X
    #for an odd number of moves played, it is O's turn
    else:
        return O


def actions(board):
    """
    Returns the positions of all playable fields (possible actions).

    Parameters:
    board (array): the playing board as a 3x3 array 

    Returns:
    array:      all possible actions (i,j) in an array
    """
    rows = [0,1,2]
    cols = [0,1,2]

    actions = []

    #check every tile of the playing field - if EMPTY, add to list of possible actions
    for row in rows:
        for col in cols:
            if board[row][col] is EMPTY:
                actions.append((row,col))
    
    return actions


def result(board, action):
    """
    Moves the playing field forward by one move.

    Parameters:
    board (array): the playing board as a 3x3 array
    action (array): the position/coordinate of the tile that is chosen for the next move 

    Returns:
    array:      the new state of the playing board after the current move has been played
    """

    if action not in actions(board):
        raise Exception('Not a valid action for this board')
    
    newboard = copy.deepcopy(board)
    #entry of the new board at position chosen by the action/move is the symbol of the player that takes the turn (X or O)
    newboard[action[0]][action[1]] = player(board)

    return newboard


def winner(board):
    """
    Checks if there is a winner on the board and if so, returns them. 

    Parameters:
    board (array): the playing board as a 3x3 array

    Returns:
    string:     "X" if player X fulfils a win condition 
                "O" if player O fulfils a win condition
    NoneType    if the current board has no winner
    """

    rows = [0,1,2]
    cols = [0,1,2]

    #check all horizontal win conditions
    #the if condition might look strange at first due to the if board[row][0] and ...
    #this is implemented due to the fact that otherwise if e.g. X chooses only the bottom row and O chooses only the center row and X has a full row,
    #the check returns None because the first row has 3 identical entries (all None)
    for row in rows:
        if board[row][0] and board[row][0] == board[row][1] == board[row][2]:
            return board[row][0]
    
    #check all vertical win conditions
    for col in cols:
        if board[0][col] and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]
    
    #check all diagonal win conditions
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2]) or (board[2][0] == board[1][1] and board[1][1] == board[0][2]):
        return board[1][1]  

    return None


def terminal(board):
    """
    Checks if the board has reached the terminal state (there is a winner or all tiles are filled). 

    Parameters:
    board (array): the playing board as a 3x3 array

    Returns:
    boolean:    True if someone has won or all tiles are filled
                False otherwise
    """

    #if there is already a winner, return True
    if winner(board) is not None:
        return True
    
    #check if any of the tiles are still empty - if so, return False
    for row in [0,1,2]:
        for col in [0,1,2]:
            if board[row][col] is EMPTY:
                return False

    #if there is no winner and no empty tiles are found, return True
    return True


def utility(board):
    """
    Determines the utility values for the minimax algorithm.

    Parameters:
    board (array): the playing board as a 3x3 array

    Returns:
    int:        1 if X is the winner
                -1 if O is the winner
                0 otherwise
    """

    if winner(board)==X:
        return 1
    
    elif winner(board)==O:
        return -1
    
    #since utility is only called on terminal boards, we can use else for a tie
    else:
        return 0

def MaxValue(board):
    """
    Finds the maximum value attainable through still playable steps.

    Parameters:
    board (array): the playing board as a 3x3 array

    Returns:
    float:      val determines the value of the maximizing action (best move for maximizing player)
    """
    val = -1e10

    #if the current state is an end state, return the utility (1 if X wins, 0 for a tie, -1 if O wins)
    if terminal(board):
        return utility(board)
    
    #the maximizing player (in our case X) should pick the move that maximizes the value
    #so, they compare the current value with the best move that the minimizing player could play from the resulting state
    #in short form: if player X chooses action a, what is the best that player O can do after action a has been performed
    #if after the action, the new board value is larger than the current val, it makes sense for the maximizing player to make that move 
    #this is checked for all possible actions one can still play with the current board state
    for action in actions(board):
        val = max(val, MinValue(result(board, action)))
    return val

def MinValue(board):
    """
    Finds the minimum value attainable through still playable steps.

    Parameters:
    board (array): the playing board as a 3x3 array

    Returns:
    float:      val determines the value of the minimizing action (best move for minimizing player)
    """
    val = 1e10

    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        val = min(val, MaxValue(result(board, action)))
    return val

def minimax(board):
    """
    The function combs through the possible game trees and chooses the optimal one to take at the current game state.

    Parameters:
    board (array): the playing board as a 3x3 array

    Returns:
    array:      the optimal move to make based on the current state of the board
    """

    if terminal(board)==True:
        return None

    #player O wants to minimize, so player X, "anticipating" this, will choose the maximum value of the minimum values
    #consider it this way: X makes a move, then O makes a move that aims to minimize the score. Since X wants to maximize it, they will pick the 
    #maximum of the moves that O can make (the ones that aim to minimize).
    #that is why we encounter max(MinValue)
    if player(board)==X:
        values = []
        #determine the minimum value for the board after each possible action
        for action in actions(board):
            values.append(MinValue(result(board,action)))
        #choose the move that is the maximum of all the minimum values
        maximum = max(values)
        return actions(board)[values.index(maximum)]
    
    #same applies here, just the other way around
    if player(board)==O:
        values = []
        for action in actions(board):
            values.append(MaxValue(result(board,action)))
        minimum = min(values)
        return actions(board)[values.index(minimum)]