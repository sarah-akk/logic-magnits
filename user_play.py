from copy import deepcopy
from board import Board

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


def user_play_mode(game):
    """
    Handles the user play logic for the current stage.
    """
    print(f"\nStage: {game.current_stage}")
    
    while game.moves_left > 0:
        print()
        game.board.display()
        print()
        
        print(f"{YELLOW}Moves left: {game.moves_left}{RESET}")
        print()

        # Check win condition
        if game.board.check_win_condition():    
            game.end_stage(True)
            return
        
        piece = input(f"{PINK}Enter the piece to move{RESET} ({PURPLE}p{RESET} for purple, {BRIGHT_RED}r{RESET} for red, {GREEN}g{RESET} for generating possible states): ")

        if piece == "g":
            piece_to_move = input(f"{PINK}Enter the piece to generate moves for{RESET} ({PURPLE}p{RESET} for purple, {BRIGHT_RED}r{RESET} for red): ")
            possible_states = game.generate_possible_states(piece_to_move)
            
            if possible_states:
                print(f"{GREEN}Generated possible states:{RESET}")
                for i, state in enumerate(possible_states, 1):
                    print(f"\nState {i}:")
                    state.display()
            else:
                print(f"{RED}⚠️ No possible moves found for piece {piece_to_move}.{RESET}")
            print()
            print("=====================================================")
            continue

        try:
            target_x = int(input(f"{CYAN}Enter the x-coordinate to move to: {RESET}"))
            target_y = int(input(f"{CYAN}Enter the y-coordinate to move to: {RESET}"))
        except ValueError:
            print()
            print(f"{RED}⚠️ Invalid input. Coordinates must be numbers. Try again.{RESET}")
            print()
            continue

        target_x -= 1
        target_y -= 1

        if game.board.move_piece(piece, target_x, target_y):
            game.click_sound.play()
            if game.board.check_win_condition():
                game.board.display()
                game.end_stage(True)
                return
            game.moves_left -= 1
        else:
            print()
            print(f"{RED}⚠️ Invalid piece or move, try again.{RESET}")
            print()

    game.board.display()
    game.end_stage(False)
