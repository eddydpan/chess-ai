import chess
import minimax

board = chess.Board()
move = chess.Move.from_uci("e2e4")
board.push(move)

minmax = minimax.Minimax(board)

results = minmax.generate_next_move(3)
board.push(results[1])
print(board)
