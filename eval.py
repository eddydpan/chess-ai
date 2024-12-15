"""
Evaluates the state of a chess board depending on the material difference, pawn
structure, piece development, etc. and returns an int that's positive if white
is better, and negative if black is better.
"""

import chess
import logging
import numpy as np

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

BOARD_SIZE = 64
# piece_vals = {"P": 100, "N": 280, "B": 320, "R": 479, "Q": 929, "K": 60000,
#               "p": -100, "n": -280, "b": -320, "r": -479, "q": -929, "k": -60000}
piece_vals = {"P": 100, "N": 280, "B": 320, "R": 479, "Q": 929, "K": 60000}


b_pawn_pst = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [78, 83, 86, 73, 102, 82, 85, 90],
        [7, 29, 21, 44, 40, 31, 44, 7],
        [-17, 16, -2, 15, 14, 0, 15, -13],
        [-26, 3, 10, 9, 6, 1, 0, -23],
        [-22, 9, 5, -11, -10, -2, 3, -19],
        [-31, 8, -7, -37, -36, -14, 3, -31],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
)
w_pawn_pst = np.flipud(b_pawn_pst)

b_knight_pst = np.array(
    [
        [-66, -53, -75, -75, -10, -55, -58, -70],
        [-3, -6, 100, -36, 4, 62, -4, -14],
        [10, 67, 1, 74, 73, 27, 62, -2],
        [24, 24, 45, 37, 33, 41, 25, 17],
        [-1, 5, 31, 21, 22, 35, 2, 0],
        [-18, 10, 13, 22, 18, 15, 11, -14],
        [-23, -15, 2, 0, 2, 0, -23, -20],
        [-74, -23, -26, -24, -19, -35, -22, -69],
    ]
)
w_knight_pst = np.flipud(b_knight_pst)

b_bishop_pst = np.array(
    [
        [-59, -78, -82, -76, -23, -107, -37, -50],
        [-11, 20, 35, -42, -39, 31, 2, -22],
        [-9, 39, -32, 41, 52, -10, 28, -14],
        [25, 17, 20, 34, 26, 25, 15, 10],
        [13, 10, 17, 23, 17, 16, 0, 7],
        [14, 25, 24, 15, 8, 25, 20, 15],
        [19, 20, 11, 6, 7, 6, 20, 16],
        [-7, 2, -15, -12, -14, -15, -10, -10],
    ]
)

w_bishop_pst = np.flipud(b_bishop_pst)

b_rook_pst = np.array(
    [
        [35, 29, 33, 4, 37, 33, 56, 50],
        [55, 29, 56, 67, 55, 62, 34, 60],
        [19, 35, 28, 33, 45, 27, 25, 15],
        [0, 5, 16, 13, 18, -4, -9, -6],
        [-28, -35, -16, -21, -13, -29, -46, -30],
        [-42, -28, -42, -25, -25, -35, -26, -46],
        [-53, -38, -31, -26, -29, -43, -44, -53],
        [-30, -24, -18, 5, -2, -18, -31, -32],
    ]
)
w_rook_pst = np.flipud(b_rook_pst)
b_queen_pst = np.array(
    [
        [6, 1, -8, -104, 69, 24, 88, 26],
        [14, 32, 60, -10, 20, 76, 57, 24],
        [-2, 43, 32, 60, 72, 63, 43, 2],
        [1, -16, 22, 17, 25, 20, -13, -6],
        [-14, -15, -2, -5, -1, -10, -20, -22],
        [-30, -6, -13, -11, -16, -11, -16, -27],
        [-36, -18, 0, -19, -15, -15, -21, -38],
        [-39, -30, -31, -13, -31, -36, -34, -42],
    ]
)
w_queen_pst = np.flipud(b_queen_pst)
b_king_pst = np.array(
    [
        [4, 54, 47, -99, -99, 60, 83, -62],
        [-32, 10, 55, 56, 56, 55, 10, 3],
        [-62, 12, -57, 44, -67, 28, 37, -31],
        [-55, 50, 11, -4, -19, 13, 0, -49],
        [-55, -43, -52, -28, -51, -47, -8, -50],
        [-47, -42, -43, -79, -64, -32, -29, -32],
        [-4, 3, -14, -50, -57, -18, 13, 4],
        [17, 30, -3, -14, 6, -1, 40, 18],
    ]
)
w_king_pst = np.flipud(b_king_pst)
pst_dic = {
    # The bot is playing as black
    "P": (
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,  #       ^ player | idx = 0
        78,
        83,
        86,
        73,
        102,
        82,
        85,
        90,  #       |        |           .
        7,
        29,
        21,
        44,
        40,
        31,
        44,
        7,  #       |        |            .
        -17,
        16,
        -2,
        15,
        14,
        0,
        15,
        -13,  #       |        |             .
        -26,
        3,
        10,
        9,
        6,
        1,
        0,
        -23,  #       |        |              .
        -22,
        9,
        5,
        -11,
        -10,
        -2,
        3,
        -19,  #       |        |               .
        -31,
        8,
        -7,
        -37,
        -36,
        -14,
        3,
        -31,  #       |        |                .
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ),  #   BOT |        V                  idx = 63
    "N": (
        -66,
        -53,
        -75,
        -75,
        -10,
        -55,
        -58,
        -70,
        -3,
        -6,
        100,
        -36,
        4,
        62,
        -4,
        -14,
        10,
        67,
        1,
        74,
        73,
        27,
        62,
        -2,
        24,
        24,
        45,
        37,
        33,
        41,
        25,
        17,
        -1,
        5,
        31,
        21,
        22,
        35,
        2,
        0,
        -18,
        10,
        13,
        22,
        18,
        15,
        11,
        -14,
        -23,
        -15,
        2,
        0,
        2,
        0,
        -23,
        -20,
        -74,
        -23,
        -26,
        -24,
        -19,
        -35,
        -22,
        -69,
    ),
    "B": (
        -59,
        -78,
        -82,
        -76,
        -23,
        -107,
        -37,
        -50,
        -11,
        20,
        35,
        -42,
        -39,
        31,
        2,
        -22,
        -9,
        39,
        -32,
        41,
        52,
        -10,
        28,
        -14,
        25,
        17,
        20,
        34,
        26,
        25,
        15,
        10,
        13,
        10,
        17,
        23,
        17,
        16,
        0,
        7,
        14,
        25,
        24,
        15,
        8,
        25,
        20,
        15,
        19,
        20,
        11,
        6,
        7,
        6,
        20,
        16,
        -7,
        2,
        -15,
        -12,
        -14,
        -15,
        -10,
        -10,
    ),
    "R": (
        35,
        29,
        33,
        4,
        37,
        33,
        56,
        50,
        55,
        29,
        56,
        67,
        55,
        62,
        34,
        60,
        19,
        35,
        28,
        33,
        45,
        27,
        25,
        15,
        0,
        5,
        16,
        13,
        18,
        -4,
        -9,
        -6,
        -28,
        -35,
        -16,
        -21,
        -13,
        -29,
        -46,
        -30,
        -42,
        -28,
        -42,
        -25,
        -25,
        -35,
        -26,
        -46,
        -53,
        -38,
        -31,
        -26,
        -29,
        -43,
        -44,
        -53,
        -30,
        -24,
        -18,
        5,
        -2,
        -18,
        -31,
        -32,
    ),
    "Q": (
        6,
        1,
        -8,
        -104,
        69,
        24,
        88,
        26,
        14,
        32,
        60,
        -10,
        20,
        76,
        57,
        24,
        -2,
        43,
        32,
        60,
        72,
        63,
        43,
        2,
        1,
        -16,
        22,
        17,
        25,
        20,
        -13,
        -6,
        -14,
        -15,
        -2,
        -5,
        -1,
        -10,
        -20,
        -22,
        -30,
        -6,
        -13,
        -11,
        -16,
        -11,
        -16,
        -27,
        -36,
        -18,
        0,
        -19,
        -15,
        -15,
        -21,
        -38,
        -39,
        -30,
        -31,
        -13,
        -31,
        -36,
        -34,
        -42,
    ),
    "K": (
        4,
        54,
        47,
        -99,
        -99,
        60,
        83,
        -62,
        -32,
        10,
        55,
        56,
        56,
        55,
        10,
        3,
        -62,
        12,
        -57,
        44,
        -67,
        28,
        37,
        -31,
        -55,
        50,
        11,
        -4,
        -19,
        13,
        0,
        -49,
        -55,
        -43,
        -52,
        -28,
        -51,
        -47,
        -8,
        -50,
        -47,
        -42,
        -43,
        -79,
        -64,
        -32,
        -29,
        -32,
        -4,
        3,
        -14,
        -50,
        -57,
        -18,
        13,
        4,
        17,
        30,
        -3,
        -14,
        6,
        -1,
        40,
        18,
    ),
}

pst = {
    "P": (b_pawn_pst, w_pawn_pst),
    "N": (b_knight_pst, w_knight_pst),
    "B": (b_bishop_pst, w_bishop_pst),
    "R": (b_rook_pst, w_rook_pst),
    "Q": (b_queen_pst, w_queen_pst),
    "K": (b_king_pst, w_king_pst),
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
    Computes the score based on piece activity and material value using numpy arrays
    for PST lookup and evaluates from Black's perspective.

    Args:
        board: A `chess.Board()` object.
    Returns:
        An integer score; positive for White's advantage, negative for Black's advantage.
    """
    sum = 0
    board_epd = board.epd().split(" ")[0]  # Get only the board positions

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_symbol = piece.symbol()
            is_white = piece.color  # True if white, False if black
            pst_table = pst[piece_symbol.upper()][is_white]  # Get relevant PST
            pst_value = pst_table[square // 8, square % 8]
            piece_value = piece_vals[piece_symbol.upper()]

            # Accumulate score (positive for White, negative for Black)
            sum += (1 if is_white else -1) * (piece_value + pst_value)

    return sum


def evaluate_board(
    board=chess.Board(), move=chess.Move(chess.Move.null(), chess.Move.null()), score=0
):
    """
    Computes the score of the chess board depending on which player's move it
    is, material difference, piece activity, pawn structure, king safety, etc.

    Args:
        board: a chess.Board() object to be evaluated. Defaults to starting
            game position.
        move: a chess.Move object representing the move to evaluate.
        score: an optional base score to factor into evaluation.
    Returns:
        An int where a positive number means white is favored and a negative
        number means black is favored. The greater the magnitude of the int,
        the more favored the position is.
    """
    # Update the piece activity
    side = 2 * board.turn - 1  # either 1 (white) or -1 (black)
    score = side * score

    capture_dif = 0
    atk_piece = (
        board.piece_at(move.from_square).symbol().upper()
    )  # get the piece symbol

    # Calculate piece-square table difference (pst_dif)
    pst_dif = (
        pst[atk_piece][board.turn][move.to_square // 8][move.to_square % 8]
        - pst[atk_piece][board.turn][move.from_square // 8][move.from_square % 8]
    )

    # Update for captures
    if board.is_capture(move):
        capture_square = move.to_square

        # Handle en passant
        if board.is_en_passant(move):
            capture_square += (
                8  # the pawn that got en-passant'd would be behind the attacking pawn
            )

        # Only get a captured piece if there was a capture
        cptd_piece = board.piece_at(capture_square).symbol().upper()
        # Sum piece value of captured piece with its activity, reverse the board with 63 - square
        capture_dif = (
            piece_vals[cptd_piece]
            + pst[cptd_piece][board.turn][capture_square // 8][capture_square % 8]
        )

    # Quick check: Skip evaluation if the move doesn't deliver check or checkmate is impossible
    if not board.gives_check(move) or board.is_insufficient_material():
        return side * (score + pst_dif + capture_dif)

    # Optimize checkmate and stalemate evaluation by limiting push/pop usage
    legal_moves = list(board.legal_moves)
    if len(legal_moves) <= 5:  # Forced moves are rare; check for game-ending conditions
        board.push(move)
        if board.is_checkmate():
            board.pop()
            return 100000 * side
        if board.is_stalemate():
            board.pop()
            return 0
        board.pop()

    # Return the final evaluated score without additional overhead
    return side * (score + pst_dif + capture_dif)
