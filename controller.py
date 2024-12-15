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
        self.captured_pieces_white = []
        self.captured_pieces_black = []
        self.depth = 5

    def move(self, move_from: int, move_to: int):
        """
        Move piece from move_from square to move_to square
        """
        move_promote = chess.Move(
            from_square=move_from,
            to_square=move_to,
            promotion=chess.QUEEN,
        )
        move = chess.Move(from_square=move_from, to_square=move_to)
        if move_promote in self.board.legal_moves:
            print("HELLO")
            self.board.push(move_promote)
            return True
        if move in self.board.legal_moves:
            # Check if the move is a capture
            if self.board.is_capture(move):
                captured_piece = self.board.piece_at(move.to_square).symbol()
                if self.board.turn:  # White's turn, so black piece is captured
                    self.captured_pieces_black.append(captured_piece)
            self.board.push(move)
            return True
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

        # self.is_endgame()

        results = minmax.alpha_beta_min(
            self.depth, float("-inf"), float("inf"), chess.Move.null()
        )
        print(results[0])
        if self.board.is_capture(results[1]):
            self.captured_pieces_white.append(
                self.board.piece_at(results[1].to_square).symbol()
            )
        self.board.push(results[1])

    def is_endgame(self):
        """
        Determines if the game is in the endgame phase based on material count.

        Args:
            board (chess.Board): The current board state.

        Returns:
            bool: True if it's endgame, False otherwise.
        """
        # Mapping dictionary for piece symbols to chess constants
        piece_map = {
            "P": chess.PAWN,
            "N": chess.KNIGHT,
            "B": chess.BISHOP,
            "R": chess.ROOK,
            "Q": chess.QUEEN,
            "K": chess.KING,
        }
        piece_vals = {"P": 100, "N": 280, "B": 320, "R": 479, "Q": 929, "K": 60000}

        total_material = 0

        for piece_type, value in piece_vals.items():
            # Get the corresponding chess constant
            chess_piece = piece_map[piece_type]

            # Calculate total material for major pieces
            if chess_piece in (chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN):
                total_material += (
                    len(self.board.pieces(chess_piece, chess.WHITE)) * value
                )
                total_material += (
                    len(self.board.pieces(chess_piece, chess.BLACK)) * value
                )

        # Define a threshold for endgame based on material
        if total_material <= 2500:  # Adjust threshold as needed
            self.depth = 6
        if total_material <= 1500:  # Adjust threshold as needed
            self.depth = 7
        if total_material <= 1000:  # Adjust threshold as needed
            self.depth = 8
