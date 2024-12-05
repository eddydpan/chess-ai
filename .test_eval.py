"""
A module that tests the implementation frmo eval.py
"""

import chess
import eval
import time

board = chess.Board()
start_time = time.time()



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
num_trials = 30000
for i in range(num_trials):
        t = eval.calc_piece_activity(board)
print(t)
end_time = time.time()

elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time} seconds for {num_trials} trials.")