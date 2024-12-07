"""
A module that tests the implementation from eval.py
"""

import chess
import eval
import time

board = chess.Board()
start_time = time.time()
num_trials = 10000
##########

score = eval.calc_piece_activity(board)
print(f"Score on initialization is {score}")

board.push_san("e4")
score = eval.calc_piece_activity(board)
print(f"Score after e4 is {score}")
board.push_san("e5")

score = eval.calc_piece_activity(board)
print(board)
print(f"Score after d5 is {score}")
###############



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

#####################
board2 = chess.Board()
score = eval.calc_piece_activity(board2) # Initialize score of initial board

m = chess.Move(chess.E2, chess.E4)
score = eval.evaluate_board(board2, move=m, score=score)
print(board2)
print(f"Score is {score}")

board2.push_san("e4")

m = chess.Move(chess.E7, chess.E5)
score = eval.evaluate_board(board2, move=m, score=-score)
print(board2)
print(f"Score is {score}")
######################

# board.push_san("e4")


# Calculate computation time
# for i in range(num_trials):
#     # eval.calc_piece_activity(board)
#     eval.evaluate_board(board, move=chess.Move(chess.E2, chess.E4))
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds for {num_trials} trials.")