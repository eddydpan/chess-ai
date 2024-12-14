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

    def alpha_beta_max(self, depth, alpha, beta, move, score=0):
        try:
            cur_score = evaluate_board(self.board, move, score)
        except:
            cur_score = 0
        if depth == 0:
            return (cur_score, move)
        max_eval = float("-inf")
        best_move = None

        if not move == chess.Move.null():
            self.board.push(move)

        list_of_legal_moves = list(self.board.legal_moves)
        for i in list_of_legal_moves:
            cur_eval = self.alpha_beta_min(depth - 1, alpha, beta, i, cur_score)[0]
           
            if cur_eval > max_eval:
                max_eval = cur_eval
                best_move = i
            if cur_eval >= beta:
                break
            if max_eval > alpha:
                alpha = max_eval

        if not move == chess.Move.null():
            self.board.pop()

        return (max_eval, best_move)

    def alpha_beta_min(self, depth, alpha, beta, move, score=0):
        try:
            cur_score = evaluate_board(self.board, move, score)
        except:
            cur_score = 0
        if depth == 0:
            return (cur_score, move)
        min_eval = float("inf")
        best_move = None

        if not move == chess.Move.null():
            self.board.push(move)

        list_of_legal_moves = list(self.board.legal_moves)
        for i in list_of_legal_moves:
            cur_eval = self.alpha_beta_max(depth - 1, alpha, beta, i, cur_score)[0]
            if cur_eval < min_eval:
                min_eval = cur_eval
                best_move = i
            if cur_eval <= alpha:
                break
            if min_eval < beta:
                beta = min_eval

        if not move == chess.Move.null():
            self.board.pop()

        return (min_eval, best_move)
