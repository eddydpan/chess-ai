"""
Initialization of our model for chess. This file stores the data that makes up
the backend of the game.
"""
import model

board = model.Board()
print(board)
board.legal_moves