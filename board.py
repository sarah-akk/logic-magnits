import os
from pieces import GrayPiece, PurplePiece, RedPiece

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
GRAY = "\033[90m"


class Board:
    def __init__(self, stage_path):
        self.original_board  = self.load_stage(stage_path)
        self.pieces = self.init_pieces()
        self.board = [row.copy() for row in self.original_board] 
        self.height = len(self.board[0])  
        self.width = len(self.board[0])
    def __lt__(self, other):
        """
        Define the comparison logic for Board instances to allow heapq to order them.
        For example, compare based on a string or a unique hash of the board's state.
        """
        return str(self.board) < str(other.board)

    def __eq__(self, other):
        """Check if two boards are equivalent."""
        return str(self.board) == str(other.board)

    def __hash__(self):
        """Provide a hash for the board based on its state."""
        return hash(str(self.board)) 
###############################################################################    

    def load_stage(self, stage_file):
        """Loads a stage from a file and returns a 2D list representing the board."""
        with open(stage_file, 'r',encoding='utf-8') as f:
            lines = f.readlines()
        board = [line.strip().split() for line in lines]
        return board

###############################################################################

    def init_pieces(self):
        """Initialize pieces based on the loaded board layout."""
        pieces = []
        for y, row in enumerate(self.original_board):
            for x, cell in enumerate(row):
                if cell == "g" or cell == "ⓖ":
                    pieces.append(GrayPiece(x, y))
                elif cell == "p" or cell == "ⓟ":
                    pieces.append(PurplePiece(x, y))
                elif cell == "r"  or cell == "ⓡ":
                    pieces.append(RedPiece(x, y))
        return pieces
    
###############################################################################


    def display(self):
        """Displays the board in a formatted 5x5 grid layout."""
        print("                 ")
        print("+" + "---+" * len(self.board[0]))  
        for row in self.board:
            row_display = "| " + " | ".join(
                (f"{GRAY}{cell}{RESET}" if cell in ["g", "ⓖ"] else
                 f"{PURPLE}{cell}{RESET}" if cell in ["p", "ⓟ"] else
                 f"{RED}{cell}{RESET}" if cell in ["r", "ⓡ"] else
                 f"{BLUE}{cell}{RESET}" if cell in ["∎"] else
                 cell)
                 for cell in row
            ) + " |"
            print(row_display)
            print("+" + "---+" * len(self.board[0]))  

###############################################################################

    def move_piece(self, piece_symbol, target_x, target_y):
        """Move a piece to a target position and return True if the move is successful."""

        if(piece_symbol == "ⓟ"):
            piece_symbol="p"
        if(piece_symbol == "ⓡ"):
            piece_symbol="r"

        for piece in self.pieces:
            if piece.symbol == piece_symbol:
                if self.is_valid_move(target_x, target_y):
                    
                    original_cell = self.original_board[piece.y][piece.x]

                    if original_cell == "O" or original_cell == "ⓖ" or original_cell == "ⓡ" or original_cell == "ⓟ":
                        self.board[piece.y][piece.x] = "O"
                    else:
                        self.board[piece.y][piece.x] = "."    

                    piece.move(target_x, target_y)

                    if isinstance(piece, PurplePiece) and self.board[target_y][target_x] == "O":
                        self.board[target_y][target_x] = "ⓟ"
                    elif isinstance(piece, GrayPiece) and self.board[target_y][target_x] == "O":
                        self.board[target_y][target_x] = "ⓖ"
                    elif isinstance(piece, RedPiece) and self.board[target_y][target_x] == "O":
                        self.board[target_y][target_x] = "ⓡ"    
                    else:               
                        self.board[target_y][target_x] = piece.symbol  

                    self.apply_effects(piece)  
                    return True
        return False
    
###############################################################################

    def is_valid_move(self, x, y):
        """Check if a position is within bounds and empty."""
        return 0 <= x < len(self.board[0]) and 0 <= y < len(self.board[0]) and (self.board[y][x] == "." or self.board[y][x] == "O") and self.board[y][x] != "∎"
    
###############################################################################

    def apply_effects(self, piece):
        """Move gray pieces based on the purple/red piece effect."""
        if isinstance(piece, PurplePiece) or piece == "ⓟ":
            self.repel_gray_pieces(piece)
        elif isinstance(piece, RedPiece) or piece == "ⓡ":
            self.attract_gray_pieces(piece)

###############################################################################


    def find_connected_gray_pieces(self, piece, direction):
        """Finds the closest gray piece in a specified direction and any gray pieces connected to it."""
        connected_gray_pieces = []
        x, y = piece.x, piece.y
        dx, dy = direction
        closest_gray_piece = None

        # First pass: Find the closest gray piece in the direction
        while 0 <= x + dx < len(self.board[0]) and 0 <= y + dy < len(self.board[0]):
            x += dx
            y += dy
            
            if not (0 <= x < len(self.board[0]) and 0 <= y < len(self.board[0])):
                break  
            # print(x ,y)   
            if self.board[y][x] in ("g", "ⓖ" , "r" , "ⓡ" , "p" , "ⓟ"):
                closest_gray_piece = next(p for p in self.pieces if p.x == x and p.y == y and (isinstance(p, GrayPiece) or isinstance(p, RedPiece) or isinstance(p, PurplePiece) ))
                break  # Stop at the closest gray piece

        if not closest_gray_piece:
            return connected_gray_pieces

        connected_gray_pieces.append(closest_gray_piece)

        while 0 <= x + dx < len(self.board[0]) and 0 <= y + dy < len(self.board[0]):
            x += dx
            y += dy

            if not (0 <= x < len(self.board[0]) and 0 <= y < len(self.board[0])):
                break  

            if self.board[y][x] in ("g", "ⓖ" , "r" , "ⓡ" , "p" , "ⓟ"):
                connected_piece = next(p for p in self.pieces if p.x == x and p.y == y and (isinstance(p, GrayPiece) or isinstance(p, RedPiece) or isinstance(p, PurplePiece)))
                connected_gray_pieces.append(connected_piece)
            else:
                break  # Stop if a non-gray cell is encountered

        return connected_gray_pieces

###############################################################################

    def repel_gray_pieces(self, purple_piece):
        """Repel the nearest gray piece and connected pieces away from the purple piece."""
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # down, up, right, left

        for dx, dy in directions:
            gray_pieces = self.find_connected_gray_pieces(purple_piece, (dx, dy))
            for gray_piece in reversed(gray_pieces):  
                new_x = gray_piece.x + dx
                new_y = gray_piece.y + dy
                if self.is_valid_move(new_x, new_y):
                    original_cell = self.original_board[gray_piece.y][gray_piece.x]
                    current_cell = self.board[gray_piece.y][gray_piece.x]
                    # edit old piece 
                    self.board[gray_piece.y][gray_piece.x] = "O" if (original_cell == "O" or original_cell == "ⓖ" or original_cell == "ⓡ" or original_cell == "ⓟ") else "."
                    gray_piece.move(new_x, new_y)
                    if original_cell == "p" or original_cell == "ⓟ" and self.board[new_y][new_x] != "O":
                        self.board[new_y][new_x] = "p"
                    elif original_cell == "r" or original_cell == "ⓡ" and self.board[new_y][new_x] != "O":   
                        self.board[new_y][new_x] = "r" 
                    else:
                        if current_cell  in ("ⓖ" , "g" ) and self.board[new_y][new_x] == "O":
                            self.board[new_y][new_x] = "ⓖ"
                        elif current_cell  in ("ⓡ" , "r") and self.board[new_y][new_x] == "O":
                            self.board[new_y][new_x] = "ⓡ" 
                        elif current_cell  in ("ⓟ" , "p") and self.board[new_y][new_x] == "O":
                            self.board[new_y][new_x] = "ⓟ"                                                                                     
                        else:
                            self.board[new_y][new_x] = "g"   

###############################################################################

    def attract_gray_pieces(self, red_piece):
        """Attract the nearest gray piece and connected pieces towards the red piece."""
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # down, up, right, left

        for dx, dy in directions:
            gray_pieces = self.find_connected_gray_pieces(red_piece, (dx, dy))
            for gray_piece in gray_pieces:
                new_x = gray_piece.x - dx
                new_y = gray_piece.y - dy
                if self.is_valid_move(new_x, new_y):
                    original_cell = self.original_board[gray_piece.y][gray_piece.x]
                    current_cell = self.board[gray_piece.y][gray_piece.x]
                    self.board[gray_piece.y][gray_piece.x] = "O" if original_cell == "O" or original_cell == "ⓖ" or original_cell == "ⓡ" or original_cell == "ⓟ" else "."
                    gray_piece.move(new_x, new_y)
                    if original_cell == "p" or original_cell == "ⓟ" and self.board[new_y][new_x] != "O":
                        self.board[new_y][new_x] = "p"
                    elif original_cell == "r" or original_cell == "ⓡ" and self.board[new_y][new_x] != "O":   
                        self.board[new_y][new_x] = "r"                                               
                    else:
                        if current_cell  in ("ⓖ" , "g" ) and self.board[new_y][new_x] == "O":
                            self.board[new_y][new_x] = "ⓖ"
                        elif current_cell  in ("ⓡ" , "r") and self.board[new_y][new_x] == "O":
                            self.board[new_y][new_x] = "ⓡ"     
                        elif current_cell  in ("ⓟ" , "p") and self.board[new_y][new_x] == "O":
                            self.board[new_y][new_x] = "ⓟ"                              
                        else:
                            self.board[new_y][new_x] = "g"                           
 
 

###############################################################################
    def check_win_condition(self):
        """Checks if the win condition is met (all 'O' cells are filled)."""
        return all(cell != 'O' for row in self.board for cell in row)
