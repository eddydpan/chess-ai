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
        print(f"max {depth}")
        print(move)
        if depth == 0:
            return (evaluate_board(self.board, move), move)
        max_eval = float("-inf")
        best_move = None

        if move is not None:
            self.board.push(move)

        print(self.board)

        list_of_legal_moves = list(self.board.legal_moves)
        for i in list_of_legal_moves:
            cur_eval = self.alpha_beta_min(depth - 1, alpha, beta, i)[0]
            if cur_eval > max_eval:
                max_eval = alpha
                best_move = i
                if cur_eval > alpha:
                    alpha = cur_eval
            if cur_eval >= beta:
                print("PRUNES")
                self.board.pop()
                print(f"SCORE {cur_eval}")
                return (cur_eval, best_move)

        if move is not None:
            print("POP")
            self.board.pop()

        print(f"SCORE {max_eval}")
        return (max_eval, best_move)

    def alpha_beta_min(self, depth, alpha, beta, move):
        print(f"min {depth}")
        print(move)
        if depth == 0:
            return (evaluate_board(self.board, move), move)
        min_eval = float("inf")
        best_move = None

        if move is not None:
            self.board.push(move)

        print(self.board)

        list_of_legal_moves = list(self.board.legal_moves)
        for i in list_of_legal_moves:
            cur_eval = self.alpha_beta_max(depth - 1, alpha, beta, i)[0]
            if cur_eval < min_eval:
                min_eval = cur_eval
                best_move = i
                if cur_eval < beta:
                    beta = cur_eval
            if cur_eval <= alpha:
                print("PRUNES")
                self.board.pop()
                print(f"SCORE {cur_eval}")
                return (cur_eval, best_move)

        if move is not None:
            print("POP1")
            self.board.pop()

        print(f"SCORE {min_eval}")
        return (min_eval, best_move)
