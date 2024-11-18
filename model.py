"""
Initialization of our model for chess. This file stores the data that makes up
the backend of the game.
"""
import chess

board = chess.Board()
print(board)
print(type(board.legal_moves))
legal_moves = [board.san(move) for move in board.legal_moves] # list of legal moves
print(board)
