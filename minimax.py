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

    def alpha_beta_max(self, depth, alpha, beta, move):
        if depth == 0:
            print(self.board)
            print(move)
            return (evaluate_board(self.board, move), None)
        max_eval = float("-inf")
        best_move = None

        list_of_legal_moves = list(self.board.legal_moves)
        for i in list_of_legal_moves:
            # self.board.push(i)
            cur_eval = self.alpha_beta_min(depth - 1, alpha, beta, i)[0]
            # self.board.pop()
            if cur_eval > max_eval:
                max_eval = alpha
                best_move = i
                if cur_eval > alpha:
                    alpha = cur_eval
            if cur_eval >= beta:
                return (cur_eval, best_move)

        return (max_eval, best_move)

    def alpha_beta_min(self, depth, alpha, beta, move):
        if depth == 0:
            print(self.board)
            print(move)
            return (evaluate_board(self.board, move), None)
        min_eval = float("inf")
        best_move = None

        list_of_legal_moves = list(self.board.legal_moves)
        for i in list_of_legal_moves:
            # self.board.push(i)
            cur_eval = self.alpha_beta_max(depth - 1, alpha, beta, i)[0]
            # self.board.pop()
            if cur_eval < min_eval:
                min_eval = cur_eval
                best_move = i
                if cur_eval < beta:
                    beta = cur_eval
            if cur_eval <= alpha:
                return (cur_eval, best_move)
            
        return (min_eval, best_move)