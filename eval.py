"""
Evaluates the state of a chess board depending on the material difference, pawn
structure, piece development, etc. and returns a float that's positive if white
is better, and negative if black is better.
"""
import chess

piece_vals = {"P": 100, "N": 280, "B": 320, "R": 479, "Q": 929, "K": 60000, 
              "p": -100, "n": -280, "b": -320, "r": -479, "q": -929, "k": -60000}
pst = {
    # The bot is playing as black
    'P': (   0,   0,   0,   0,   0,   0,   0,   0,  #       ^ player |
            78,  83,  86,  73, 102,  82,  85,  90,  #       |        |
             7,  29,  21,  44,  40,  31,  44,   7,  #       |        |
           -17,  16,  -2,  15,  14,   0,  15, -13,  #       |        |
           -26,   3,  10,   9,   6,   1,   0, -23,  #       |        |
           -22,   9,   5, -11, -10,  -2,   3, -19,  #       |        |
           -31,   8,  -7, -37, -36, -14,   3, -31,  #       |        |
             0,   0,   0,   0,   0,   0,   0,   0), #   BOT |        V
    'N': ( -66, -53, -75, -75, -10, -55, -58, -70,
            -3,  -6, 100, -36,   4,  62,  -4, -14,
            10,  67,   1,  74,  73,  27,  62,  -2,
            24,  24,  45,  37,  33,  41,  25,  17,
            -1,   5,  31,  21,  22,  35,   2,   0,
           -18,  10,  13,  22,  18,  15,  11, -14,
           -23, -15,   2,   0,   2,   0, -23, -20,
           -74, -23, -26, -24, -19, -35, -22, -69),
    'B': ( -59, -78, -82, -76, -23,-107, -37, -50,
           -11,  20,  35, -42, -39,  31,   2, -22,
            -9,  39, -32,  41,  52, -10,  28, -14,
            25,  17,  20,  34,  26,  25,  15,  10,
            13,  10,  17,  23,  17,  16,   0,   7,
            14,  25,  24,  15,   8,  25,  20,  15,
            19,  20,  11,   6,   7,   6,  20,  16,
            -7,   2, -15, -12, -14, -15, -10, -10),
    'R': (  35,  29,  33,   4,  37,  33,  56,  50,
            55,  29,  56,  67,  55,  62,  34,  60,
            19,  35,  28,  33,  45,  27,  25,  15,
             0,   5,  16,  13,  18,  -4,  -9,  -6,
           -28, -35, -16, -21, -13, -29, -46, -30,
           -42, -28, -42, -25, -25, -35, -26, -46,
           -53, -38, -31, -26, -29, -43, -44, -53,
           -30, -24, -18,   5,  -2, -18, -31, -32),
    'Q': (   6,   1,  -8,-104,  69,  24,  88,  26,
            14,  32,  60, -10,  20,  76,  57,  24,
            -2,  43,  32,  60,  72,  63,  43,   2,
             1, -16,  22,  17,  25,  20, -13,  -6,
           -14, -15,  -2,  -5,  -1, -10, -20, -22,
           -30,  -6, -13, -11, -16, -11, -16, -27,
           -36, -18,   0, -19, -15, -15, -21, -38,
           -39, -30, -31, -13, -31, -36, -34, -42),
    'K': (   4,  54,  47, -99, -99,  60,  83, -62,
           -32,  10,  55,  56,  56,  55,  10,   3,
           -62,  12, -57,  44, -67,  28,  37, -31,
           -55,  50,  11,  -4, -19,  13,   0, -49,
           -55, -43, -52, -28, -51, -47,  -8, -50,
           -47, -42, -43, -79, -64, -32, -29, -32,
            -4,   3, -14, -50, -57, -18,  13,   4,
            17,  30,  -3, -14,   6,  -1,  40,  18),
}


def sum_piece_vals(board_epd=chess.Board().epd()):
    """
    Sums up the piece values of all the pieces on the board.

    Args:
        board_epd: a chess.Board() object's epd string that represents all
            pieces on the board.
    Returns:
        An integer that represents the difference between black's piece value
        sum and white's.
    """
    sum = 0
    for char in board_epd:
        if (char.isalpha()):
            sum += piece_vals[char]
    return sum

def evaluate_board(board=chess.Board()):
    """
    Computes the score of the chess board depending on which player's move it
    is, material difference, piece activity, pawn structure, king safety, etc.

    Args:
        board: a chess.Board() object to be evaluated. Defaults to starting
            game position.
    Returns:
        A float where a positive number means white is favored and a negative
        number means black is favored. The greater the magnitude of the float,
        the more favored the position is.
    """

    legal_moves = [board.san(move) for move in board.legal_moves] # list of legal moves
    
    # CALCULATE MATERIAL DIFFERENCE: should be weighed pretty heavily, sum up material of each side 
    piece_val_sum = sum_piece_vals(board.epd())
    # CALCULATE PIECE ACTIVITY: sum up activity of both sides

    # CALCULATE KING SAFETY ... does this require knowledge of future positions? what if mate in 1?
    # OR king safety = position of 8x8 table of king position scores

    # FINAL SCORE CALCULATION:
    # score = c1 * material_diff + c2 * piece_activity + c3 * king_safety

    score = 0 # board score of how good black's position is

    for i in range(64):
        side = 1
        piece = str(board.piece_at(i))
        try:
            if (piece.islower()):
                    side = -1 # lowercase "pieces" are playing as white
                    continue

            # Access piece value and the weight of the piece at the position
            piece_pos_val = side * (piece_vals[piece.upper()] + pst[piece][i])
            score += piece_pos_val
        except KeyError: # catch a None, since None can't have islower() called on it
            continue
    return score