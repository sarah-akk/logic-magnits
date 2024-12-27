الاسم : سارة العقاد
الفئة : 3

Logic Magnets Game
1. State Space

In this game, the board represents an n×n grid with multiple types of pieces: gray (iron), purple (magnetic), and red (magnetic), as well as empty and goal slots. The state of the game at any given moment is defined by the configuration of these pieces on the board. Each state keeps track of several elements, including:

    The position of each iron or magnetic piece on the grid.
    The status of each grid cell (either empty, occupied by a magnetic or iron piece, or marked as a goal).

2. Initial State

The initial state sets up the board with the starting locations of the magnetic and iron pieces, along with the designated goal slots. Magnetic pieces (purple and red) are either fixed in position or can be moved based on the player's choices. The player’s objective is to manipulate the board to cover all goal slots, following specific movement rules.

3. Actions

Players control the movement of magnetic pieces, which in turn affect the position of iron pieces (gray). The rules for each magnetic piece type are as follows:

    Purple Piece: Can move to any empty slot. When moved, it repels any adjacent iron pieces in its row or column, pushing them to the opposite side.
    Red Piece: Can also move to any empty slot. Instead of repelling iron pieces, it attracts them in its row or column, pulling them toward its new location.

Movement Restrictions:

    Iron pieces cannot be moved directly by the player and only shift position due to the influence of nearby magnetic pieces. For example, an iron piece will move away from a purple piece when repelled or move toward a red piece when attracted.

4. Goal State

The game’s goal is to arrange the pieces so that all designated goal squares (represented by white circles on the board) are covered by either iron or magnetic pieces. Each piece must adhere to the movement rules described above while the player works to cover every goal slot. Once all goal slots are filled, the player wins the level.

Python Code Implementation Details

The game logic is implemented in Python with an interactive interface, including text-based menus and a visual board display in the console. Here are additional details about the game’s code:

    Initialization:
        The Game class loads game stages from files and sets parameters like available moves for each stage.
        The pygame library is used to enhance user experience with background music and sound effects for wins, losses, and clicks.

    Stage Selection and Play:
        The game starts with a welcome screen where players can choose to play, select a specific stage, or exit.
        During gameplay, players may manually move pieces or let the computer solve the board using algorithms like BFS or DFS.

    Algorithmic Solvers:
        BFS (Breadth-First Search) and DFS (Depth-First Search) algorithms are implemented to find solutions for each level, simulating moves to cover all goal squares.

    Piece Movement Mechanics:
        Magnetic pieces (purple and red) can be selected and moved. When moved, the generate_possible_states method calculates potential board states for each available position.
        The Board class checks for valid moves and updates piece positions based on the effects of attraction and repulsion.

    End of Stage Handling:
        After a level is completed (either by reaching the goal state or running out of moves), the player can choose to retry, proceed to the next level, or return to the main menu.


_dfs_solve(board, max_moves)

This function performs a Depth-First Search (DFS) to solve the board puzzle within a specified maximum number of moves (max_moves). It tracks the current state of the board and the positions of magnetic pieces ('p', 'r', 'ⓟ', 'ⓡ'). For each move:

    The function generates possible moves for each piece and creates a deep copy of the board to simulate the move.
    It updates the piece positions and checks if the new state is in the visited set to avoid reprocessing.
    If the board reaches a win condition (all goal slots are filled), it returns the list of moves.
    If no solution is found within the given moves, it returns None.

generate_moves_for_piece(board, piece_symbol, x, y)

This helper function generates all possible moves for a given piece (piece_symbol) located at (x, y) on the board. It identifies all empty cells ('.' or 'O') where the piece could potentially move and returns a list of those positions.
_bfs_solve(board, max_moves)

This function performs a Breadth-First Search (BFS) to find the shortest sequence of moves to solve the board puzzle within a specified maximum number of moves (max_moves). BFS is often more efficient for finding the shortest path due to its layered approach:

    Starting with the initial board state, it checks for a win condition at each level.
    It generates all possible moves using generate_possible_moves and adds each new state to the queue if it hasn’t been visited.
    When the solution is found (win condition is met), it returns the list of moves taken.
    If no solution is found within max_moves, the function returns None.

generate_possible_moves(board)

This function generates all possible moves for all pieces on the board, specifically for magnetic pieces ('p' and 'r'). It iterates over each cell, checking for empty cells ('.' or 'O'), and adds potential moves for both types of pieces to the list. The moves are returned in a format that allows the bfs_solve and dfs_solve functions to simulate and test each move.