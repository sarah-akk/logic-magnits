from copy import deepcopy
import heapq  # for priority queue ()

def AStar_solve(board, max_moves):
    minHeap = []
                      
    heapq.heappush(minHeap, (0,0, board, []))  
    explored = set()  

    while minHeap:
        cost,cost2, current_board, path = heapq.heappop(minHeap)
        # print(cost)

        if current_board.check_win_condition():
            return path  

        if current_board in explored:
            continue

        explored.add(current_board)

        piece_symbols = {piece.symbol for piece in current_board.pieces if piece.symbol in ['p', 'r']}

        for piece_symbol in piece_symbols:
            possible_states = generate_possible_states(current_board, piece_symbol)
            
            for new_state, target_x, target_y in possible_states:
                next_score = heuristic(new_state)
                new_cost = cost + 1  
                new_cost2 = next_score + new_cost
                new_path = path + [(piece_symbol, target_x, target_y)]  
                
                if new_state not in explored:
                    heapq.heappush(minHeap , (new_cost ,new_cost2, new_state, new_path))
    
    return None  


#############################################################################

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

def generate_possible_states(current_board, piece_symbol):
    possible_states = []
    
    piece = next((p for p in current_board.pieces if p.symbol == piece_symbol), None)
    if not piece:
        print(f"{piece_symbol} piece not found on the board.")
        return possible_states

    for x in range(len(current_board.board[0])):  
        for y in range(len(current_board.board[0])):
            if current_board.board[y][x] in ['.', 'O']: 
                new_board = deepcopy(current_board)  
                
                if new_board.move_piece(piece_symbol, x, y):  
                    possible_states.append((new_board, x, y))  
    
    return possible_states

