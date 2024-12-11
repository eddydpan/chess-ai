"""
A module that tests the implementation from eval.py
"""

import chess
import eval
import time

board = chess.Board()
start_time = time.time()
num_trials = 10000

board = chess.Board()

#####################
board2 = chess.Board()
score = eval.calc_piece_activity(board2) # Initialize score of initial board

m = chess.Move(chess.E2, chess.E4)
score = eval.evaluate_board(board2, move=m, score=score)
print(board2)
print(f"Score is {score}")

board2.push_san("e4")

m = chess.Move(chess.D7, chess.D5)
score = eval.evaluate_board(board2, move=m, score=score)
print(board2)
print(f"Score is {score}")

board2.push_san("d5")
m = chess.Move(chess.E4, chess.D5)
score = eval.evaluate_board(board2, move=m, score=score)
print(board2)
print(f"Score is {score}")
######################

# m = board.push_san("e4")
for i in range(num_trials):
    # eval.calc_piece_activity(board)
    eval.evaluate_board(board, move=chess.Move(chess.E2, chess.E4))
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds for {num_trials} trials.")