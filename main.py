from collections import deque
import os
from AStar_solver import AStar_solve
from bfs_solver import bfs_solve
from board import Board
from copy import deepcopy
from dfs_solver import dfs_solve
from hillClimbing_solver import hill_climbing_solve
import pygame
from ucs_solver import ucs_solve
from user_play import user_play_mode

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
GRAY = "\033[90m"
BOLD = "\033[1m"
PINK = "\033[38;2;255;182;193m"
BRIGHT_RED = "\033[38;2;255;69;0m"

DIRECTIONS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

class Game:
    def __init__(self, stages_dir):
        self.stages_dir = stages_dir
        self.current_stage = 1
        self.board = None
        self.max_moves = {
            1: 5,
            2: 5,
            3: 5,
            4: 2,
            5: 2,
            6: 2,
            7: 2,
            8: 2,
            9: 2,
            10: 2,
            11: 1,
            12: 1,
            13: 2,
            14: 2,
            15: 2,
            16: 3,
            17: 3,
            18: 2,
            19: 4,
            20: 2,
            21: 2,
            22: 3,
            23: 3,
            24: 3,
            25: 3,
        }
        self.board_states = []

        pygame.mixer.init()
        pygame.mixer.music.load("sounds/bg.mp3") 
        pygame.mixer.music.play(-1)  
        self.win_sound = pygame.mixer.Sound("sounds/win.mp3")  
        self.lose_sound = pygame.mixer.Sound("sounds/over.mp3")  
        self.click_sound = pygame.mixer.Sound("sounds/click.mp3")  

###############################################################################

    def welcome_screen(self):
        print(f"{CYAN}================================================{RESET}")
        print(f"{PINK}🧲️💫🎮   Welcome to Logic Magnets! 🧲️💫🎮      {RESET}")
        print(f"{CYAN}================================================{RESET}")
        print(f"{YELLOW}1. Play{RESET} ▶️")
        print(f"{YELLOW}2. Choose Stage 📍{RESET}")
        print(f"{YELLOW}3. Exit 🚪{RESET}")
        print(f"{CYAN}================================================{RESET}")
        
        choice = input(f"{CYAN}Enter your choice (1, 2, or 3): {RESET}")
        self.click_sound.play()
        if choice == "1":
            self.load_stage(self.current_stage)
        elif choice == "2":
            self.choose_stage()
        elif choice == "3":
            print(f"{PINK}Thank you for playing Logic Magnets! Goodbye!{RESET}")
            exit()  
        else:
            print(f"{YELLOW}⚠️ Invalid choice. Please select 1, 2, or 3.{RESET}")
            self.welcome_screen()


###############################################################################


    def generate_possible_states(self, piece_symbol):
        """Generates all possible new board states by moving a specific piece to all available cells."""
        possible_states = []
    
        piece = next((p for p in self.board.pieces if p.symbol == piece_symbol), None)
        if not piece:
            print(f"{piece_symbol} piece not found on the board.")
            return possible_states

        for x in range(len(self.board.board[0])):
            for y in range(len(self.board.board[0])):
                if self.board.is_valid_move(x, y) and self.board.board[y][x] in ['.', 'O']:
                    new_board = deepcopy(self.board)
                
                    if new_board.move_piece(piece_symbol, x + 1, y + 1):  
                        possible_states.append(new_board)
    
        return possible_states

###############################################################################

    def choose_stage(self):
        print(f"\n{BOLD}{PURPLE}Available Stages:{RESET}")
        print(f"{CYAN}{'=' * 19}{RESET}")
        
        for i in range(1, 26):
            print(f"{PINK}Stage {i:02}{RESET}", end="  ")
            if i % 5 == 0:
                print()
    
        print(f"{CYAN}\n{'=' * 19}{RESET}")
    
        try:
            stage_number = int(input(f"{YELLOW}Enter stage number (1-25): {RESET}"))
            self.click_sound.play()
            if 1 <= stage_number <= 25:
                print(f"{GREEN}Loading Stage {stage_number}... 🚀{RESET}")
                self.load_stage(stage_number)
            else:
                print(f"{RED}⚠️ Invalid stage number. Please choose between 1 and 25.{RESET}")
                self.choose_stage()
        except ValueError:
            print(f"{RED}⚠️ Invalid input. Please enter a number between 1 and 25.{RESET}")
            self.choose_stage()

###############################################################################

    def load_stage(self, stage_number):
        """Load a specific stage based on its number."""
        stage_path = os.path.join(self.stages_dir, f"stage{stage_number}.txt")
        self.board = Board(stage_path)
        self.current_stage = stage_number
        self.moves_left = self.max_moves.get(stage_number, 10) 
        self.board_states = []
        self.play_stage()

###############################################################################
    def play_stage(self):
        print(f"{GREEN}stage : {self.current_stage}{RESET}")
        self.board.display()
        print()        

        """Play the loaded stage, allowing piece movements and checking for win/loss conditions."""
        choice = input(f"{YELLOW}Choose: (1) Solve by player, (2) BFS, (3) DFS, (4) UCS, (5) Hill Climbing, (6) A* : {RESET}")
        if choice == "1":
            user_play_mode(self)         
        elif choice == "2":
            max_moves_for_stage = self.max_moves.get(self.current_stage, 5)
            solution_moves = bfs_solve(self.board, max_moves_for_stage)
        elif choice == "3":
            max_moves_for_stage = self.max_moves.get(self.current_stage, 5)
            solution_moves = dfs_solve(self.board, max_moves_for_stage)
        elif choice == "4":
            max_moves_for_stage = self.max_moves.get(self.current_stage, 5)
            solution_moves = ucs_solve(self.board, max_moves_for_stage) 
        elif choice == "5":
            max_moves_for_stage = self.max_moves.get(self.current_stage, 5)
            solution_moves = hill_climbing_solve(self.board, max_moves_for_stage) 
        elif choice == "6":
            max_moves_for_stage = self.max_moves.get(self.current_stage, 5)
            solution_moves = AStar_solve(self.board, max_moves_for_stage)      
        else:
            solution_moves = None

        if solution_moves:
            print(f"{GREEN}Solution found by computer! Executing moves...{RESET}")
            for move in solution_moves:
                piece, target_x, target_y = move
                self.board.move_piece(piece, target_x, target_y)
                self.board.display()
                print(f"{YELLOW}Move: {piece} to ({target_x + 1}, {target_y + 1}){RESET}")
                if self.board.check_win_condition():
                    self.end_stage(True)
                    return
            print(f"{GREEN}Computer completed the solution!{RESET}")
            self.end_stage(True)
            
        elif choice != "1":
            print(f"{RED}No solution found by the chosen algorithm.{RESET}")
            self.end_stage(False)
            return

###############################################################################

    def end_stage(self, won):
        """Handles end of stage options after winning or losing."""
        if won:
            print()
            print(f"{GREEN}🎉 You won! 🎉{RESET}")
            self.win_sound.play() 
            print()
            
        else:
            print()
            print(f"{BRIGHT_RED}Game Over! Out of moves. 💀{RESET}")
            self.lose_sound.play()
            print()

        while True:
            choice = input(f"{YELLOW}\nOptions: (r)etry, (n)ext level, (m)ain menu{RESET}").strip().lower()
            self.click_sound.play()
            if choice == "r":
                self.load_stage(self.current_stage)
            elif choice == "m":
                self.welcome_screen()                
            elif choice == "n":
                if self.current_stage < 25:
                    self.load_stage(self.current_stage + 1)
                else:
                    print(f"{CYAN}You've completed all levels!{RESET}")
                    break
            else:
                print(f"{RED}Invalid choice, try again.{RESET}")

###############################################################################

    def play(self):
        """Start the game by showing the welcome screen."""
        self.welcome_screen()

###############################################################################

if __name__ == "__main__":
    game = Game(stages_dir="stages")
    game.play()
