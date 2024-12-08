"""
Initialization of a controller which manipulates the python chess library
object.
"""

import chess
import minimax


class ControlGame:
    """
    Manipulates the chess object by adding moves, removing moves, and checking
    for legality of moves.
    """

    def __init__(self, board):
        self.board = board

    def move(self, move_from: int, move_to: int):
        """
        Move piece from move_from square to move_to square
        """
        move = chess.Move(from_square=move_from, to_square=move_to)
        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        else:
            return False

    def move_uci(self, string):
        """
        Move piece using uci style formatting
        """
        move = chess.Move.from_uci(string)
        if move in self.board.legal_moves:
            self.board.push(move)

    def bot_move(self):
        """
        bot makes a move
        """
        minmax = minimax.Minimax(self.board)

        results = minmax.alpha_beta_min(3, float("-inf"), float("inf"))
        self.board.push(results[1])
