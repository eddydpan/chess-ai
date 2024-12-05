"""
Minimax to find the option with the least 
"""

from eval import *


class Minimax:
    """
    Run minimax on a chess game :) to find the position that maximizes the
    bot's chances of winning.
    """

    def __init__(self, board):
        self.board = board
        pass

    def generate_next_move(self, depth):
        if depth == 0:
            return (evaluate_board(self.board), None)
        max_eval = float("-inf")
        best_move = None

        list_of_legal_moves = list(self.board.legal_moves)
        for i in list_of_legal_moves:
            self.board.push(i)
            cur_eval = -self.generate_next_move(depth - 1)[0]
            if cur_eval > max_eval:
                best_move = i
                max_eval = cur_eval
            self.board.pop()
        return (max_eval, best_move)
