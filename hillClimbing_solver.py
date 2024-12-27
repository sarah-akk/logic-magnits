from copy import deepcopy

def hill_climbing_solve(board, max_moves):
    current_board = deepcopy(board)
    current_score = heuristic(current_board)
    moves = []
    move_count = 0
    best_next_score = float('inf')  

    while not current_board.check_win_condition() and move_count < max_moves:

        best_next_state = None
        best_move = None
        

        possible_moves = generate_possible_moves(current_board)

        print("best" ,best_next_score)
        current_board.display()
        print("###############################")

        for piece_symbol, x, y in possible_moves:
            new_board = deepcopy(current_board)
            if new_board.move_piece(piece_symbol, x, y):
                new_board.display()  
                next_score = heuristic(new_board)
                # print(f"Score after move: {next_score}")

                if next_score <= best_next_score:  
                    best_next_state = new_board
                    best_next_score = next_score
                    best_move = (piece_symbol, x, y)

        if best_next_state is None:
            print()
            print("No improvement found.")
            print("best score (minimum number of white spaces rest) is :" , best_next_score )
            new_board.display()
            print()
            return

        current_board = best_next_state
        current_score = best_next_score
        # print(current_score)
        moves.append(best_move)
        move_count += 1


    print("best score (minimum number of white spaces rest) is :" , current_score )
    current_board.display()
    print()
    return moves  if current_board.check_win_condition() else None

#################################################################################

def heuristic(board):
    """Heuristic function to evaluate the board by counting the white spaces."""
    
    score = 0
    white_spaces = 0

    for y in range(board.height):
        for x in range(board.width):
            if board.board[y][x] == 'O':  
                white_spaces += 1

    score = white_spaces  

    return score

#################################################################################

def generate_possible_moves(board):
    moves = []
    for y in range(board.height): 
        for x in range(board.width):
            if board.board[y][x] in ['.', 'O']:  
                moves.append(('p', x, y))  
                moves.append(('r', x, y))  
    return moves
