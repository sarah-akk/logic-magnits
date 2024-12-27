from collections import deque
from copy import deepcopy

def bfs_solve(board, max_moves):
    """BFS algorithm to solve the puzzle stage with max_moves limit."""
    queue = deque([(board, [], 0)]) 
    visited = set()
    visited.add(str(board))  
    
    while queue:
        current_board, moves, move_count = queue.popleft()
        
        if current_board.check_win_condition():
            return moves
        
        # if move_count >= max_moves:
        #     continue
        
        possible_moves = generate_possible_moves(current_board)
        
        for piece_symbol, x, y in possible_moves:
            new_board = deepcopy(current_board)
            if new_board.move_piece(piece_symbol, x, y):
                board_state_str = str(new_board)
                if board_state_str not in visited:
                    visited.add(board_state_str)
                    queue.append((new_board, moves + [(piece_symbol, x, y)], move_count + 1))  
    
    return None


#################################################################################


def generate_possible_moves(board):
    """Generates all possible moves by placing the 'p' piece in every empty position ('.' or 'O') on the board."""
    moves = []
    for y in range(board.height): 
        for x in range(board.width):
            if  board.board[y][x] in ['.', 'O']: 
                moves.append(('p', x  , y  )) 
                moves.append(('r', x , y ))   
                # print(x,y)
    return moves


