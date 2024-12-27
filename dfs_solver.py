from copy import deepcopy

def dfs_solve(board, max_moves):
    """DFS that tracks and moves pieces 'p', 'r', 'ⓟ', 'ⓡ' up to max_moves."""
    
    initial_positions = [(x  , y , board.original_board[y][x]) 
                         for y in range(board.height) 
                         for x in range(board.width) 
                         if board.board[y][x] in ['p','r', 'ⓟ', 'ⓡ']]
    # print(initial_positions)
    if not initial_positions:
        return None  
    
    stack = [(board, initial_positions, [], 0)]
    visited = set()
    visited.add((str(board), tuple((x, y, piece) for x, y, piece in initial_positions)))
    
    while stack:
        current_board, pieces, moves, move_count = stack.pop()
        
        if current_board.check_win_condition():
            return moves
        
        if move_count >= max_moves:
            continue
        
        for (px, py, piece) in pieces:
            possible_moves = generate_moves_for_piece(current_board, piece, px, py)
            # print(possible_moves)
            for new_x, new_y in possible_moves:
                new_board = deepcopy(current_board)

                # print(piece)    
                if new_board.move_piece(piece, new_x, new_y):
                    new_pieces = [(new_x if (x == px and y == py and p == piece) else x,
                                   new_y if (x == px and y == py and p == piece) else y,
                                   p) for x, y, p in pieces]
                    
                    board_state_str = str(new_board)
                    # new_board.display()
                    
                    if (board_state_str, tuple((x, y, p) for x, y, p in new_pieces)) not in visited:
                        visited.add((board_state_str, tuple((x, y, p) for x, y, p in new_pieces)))
                        stack.append((new_board, new_pieces, moves + [(piece, new_x, new_y)], move_count + 1))
    
    return None

#################################################################################

def generate_moves_for_piece(board, piece_symbol, x, y):
    """Generates all possible moves by placing the 'p' piece in every empty position ('.' or 'O') on the board."""
    moves = []
    for y in range(board.height): 
        for x in range(board.width):
            if  board.board[y][x] in ['.', 'O']: 
                moves.append((x, y))

    return moves

#################################################################################