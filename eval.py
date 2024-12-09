"""
Evaluates the state of a chess board depending on the material difference, pawn
structure, piece development, etc. and returns an int that's positive if white
is better, and negative if black is better.
"""

import chess
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

BOARD_SIZE = 64
# piece_vals = {"P": 100, "N": 280, "B": 320, "R": 479, "Q": 929, "K": 60000, 
#               "p": -100, "n": -280, "b": -320, "r": -479, "q": -929, "k": -60000}
piece_vals = {"P": 100, "N": 280, "B": 320, "R": 479, "Q": 929, "K": 60000}
pst = {
    # The bot is playing as black
    'P': (   0,   0,   0,   0,   0,   0,   0,   0,  #       ^ player | idx = 0
            78,  83,  86,  73, 102,  82,  85,  90,  #       |        |           .
             7,  29,  21,  44,  40,  31,  44,   7,  #       |        |            .
           -17,  16,  -2,  15,  14,   0,  15, -13,  #       |        |             .
           -26,   3,  10,   9,   6,   1,   0, -23,  #       |        |              .
           -22,   9,   5, -11, -10,  -2,   3, -19,  #       |        |               .
           -31,   8,  -7, -37, -36, -14,   3, -31,  #       |        |                .
             0,   0,   0,   0,   0,   0,   0,   0), #   BOT |        V                  idx = 63
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


# def sum_piece_vals(board_epd=chess.Board().epd()):
#     """
#     Sums up the piece values of all the pieces on the board.

#     Args:
#         board_epd: a chess.Board() object's epd string that represents all
#             pieces on the board.
#     Returns:
#         An integer that represents the difference between black's piece value
#         sum and white's.
#     """
#     sum = 0
#     for char in board_epd:
#         if (char.isalpha()):
#             sum += piece_vals[char]
#     return sum


def find_piece_index(board_epd="", idx=0):
    """
    Finds index of the piece on the board (0-63) given the board epd string and
    index in the epd String.

    Args:
        board_epd: a String representing the epd of the chess board object.
        idx: an int representing the idx of the piece in the epd String.
    Returns
        An int representing the index of the piece on the chess board.
    """
    index = 0
    for char in board_epd[:idx]:  # "rn"
        if char.isalpha():
            index += 1
        elif char == "/":
            continue
        else:
            index += int(char)
    return index


def calc_piece_activity(board=chess.Board()):
    """
    Computes the bonuses for each side given the position of the pieces on the
    board. From black's POV when using pychess indexing.

    Args:
        board: a chess.Board() object to access pieces' positions.
    Returns:
        An integer representing the difference between the piece values and
        peice activity bonuses for each side. A positive result means white is
        better, and vice versa for a negative result.
    """
    sum = 0
    epd = board.epd()
    board_epd = epd.split(" ")[0]
    for idx, char in enumerate(board_epd):
        if char.isalpha():
            if char.isupper():
                sum += pst[char][find_piece_index(board_epd, idx)] + piece_vals[char]

    ################################# ROTATE THE BOARD #################################
    reversed_board_epd = board_epd[
        ::-1
    ].swapcase()  # now white is black and black is white
    for idx, char in enumerate(reversed_board_epd):
        if char.isalpha():
            if char.isupper():
                sum -= (
                    pst[char][find_piece_index(reversed_board_epd, idx)]
                    + piece_vals[char]
                )
    # print(f"Score: {sum}")
    return sum


def evaluate_board(board=chess.Board(), move=chess.Move(chess.Move.null(), chess.Move.null()), score=0):
    """
    Computes the score of the chess board depending on which player's move it
    is, material difference, piece activity, pawn structure, king safety, etc.

    Args:
        board: a chess.Board() object to be evaluated. Defaults to starting
            game position.
    Returns:
        An int where a positive number means white is favored and a negative
        number means black is favored. The greater the magnitude of the int,
        the more favored the position is.
    """
    # Update the piece activity
    side = 2*board.turn - 1 # either 1 or -1
    # logging.info(f"Score: {score}")
    capture_dif = 0
    atk_piece = board.piece_at(move.from_square).symbol().upper() # get the piece, like "B"
    pst_dif = pst[atk_piece][-side * move.to_square] - pst[atk_piece][-side * move.from_square]

    # Update for captures
    if board.is_capture(move):
        logging.info("capture")
        # Only get a captured piece if there was a capture
        cptd_piece = board.piece_at(move.to_square).symbol().upper()
        # Sum piece value of captured piece with its activity, reverse the board with 63-move.to_square
        capture_dif = piece_vals[board.piece_at(move.to_square).symbol().upper()] + pst[cptd_piece][side * move.to_square]
        breakpoint()
    breakpoint()
    return score + (pst_dif + capture_dif) * side