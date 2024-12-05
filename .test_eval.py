"""
A module that tests the implementation frmo eval.py
"""

import chess
import eval
import time

board = chess.Board()
start_time = time.time()
num_trials = 1


# legal_moves = [board.san(move) for move in board.legal_moves] # list of legal moves

# print(legal_moves)
# print(board)

score = eval.calc_piece_activity(board)
print(f"Score is {score}")

board.push_san("e4")
# board.push_san("d5")

score = eval.calc_piece_activity(board)
print(board)
print(f"Score is {score}")

# board.push_san("exd5")
# board.push_san("Nc6")

# score = eval.calc_piece_activity(board)
# print(board)
# print(f"Score is {score}")


# board.push_san("dxc6")
# score = eval.calc_piece_activity(board)
# print(board)
# print(f"Score is {score}")

# board.push_san("bxc6")
# score = eval.calc_piece_activity(board)
# print(board)
# print(f"Score is {score}")

board2 = chess.Board()
score = eval.calc_piece_activity(board2) # Initialize score of initial board

m = chess.Move(chess.E2, chess.E4)
score = eval.evaluate_board(board2, move=m, score=score)
print(board2)
print(f"Score is {score}")


end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds for {num_trials} trials.")