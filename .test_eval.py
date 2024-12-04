"""
A module that tests the implementation frmo eval.py
"""

import chess
import eval

board = chess.Board()
# legal_moves = [board.san(move) for move in board.legal_moves] # list of legal moves

# print(legal_moves)
# print(board)

# score = eval.evaluate_board(board)
# print(f"Score is {score}")

# board.push_san("e4")
# board.push_san("e5")

# score = eval.evaluate_board(board)
# print(f"Score is {score}")
# print(board)

# board.push_san("Nf3")
# board.push_san("Nc6")

# score = eval.evaluate_board(board)
# print(f"Score is {score}")
print(board)
t = 0
for i in range(10000):
        t = eval.calc_piece_activity(board)
print(t)
