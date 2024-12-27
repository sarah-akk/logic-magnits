class Piece:
    """Base class for all pieces on the board."""
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def move(self, new_x, new_y):
        """Move the piece to a specified position."""
        self.x = new_x
        self.y = new_y

class GrayPiece(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, "g")

class PurplePiece(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, "p")

class RedPiece(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, "r")
