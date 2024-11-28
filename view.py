"""
View of our chess board.
"""

import pygame
import chess
import controller


class DrawGame:
    """
    This class is used to create functions that will draw the view for the
    game. It takes in a model and uses that information to determine where
    to draw each chess piece.
    """

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 960
    piece_scale_ratio = 3.6

    square_size = 108
    padding = 40.5

    board_image = pygame.transform.scale(
        pygame.image.load("pixel chess_v1.2/boards/board_plain_03.png"),
        (SCREEN_HEIGHT, SCREEN_HEIGHT),
    )

    piece_image = {"BLACK": {}, "WHITE": {}}

    def __init__(self, board):
        # initiate controller
        self.board = board
        self.control = controller.ControlGame(board)

        # set screen size
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # initiate dictionary with all chess piece sprites
        pieces = ["bishop", "king", "knight", "pawn", "queen", "rook"]
        pieces_short = ["b", "k", "n", "p", "q", "r"]
        for i, ele in enumerate(pieces):
            self.piece_image[pieces_short[i]] = self.scaled_chess_piece(
                f"pixel chess_v1.2/16x32 pieces/B_{pieces[i].capitalize()}.png",
                self.piece_scale_ratio,
            )
            self.piece_image[pieces_short[i].upper()] = self.scaled_chess_piece(
                f"pixel chess_v1.2/16x32 pieces/W_{pieces[i].capitalize()}.png",
                self.piece_scale_ratio,
            )

        # set currently selected piece by player
        self.selected_square = None

    def draw(self):
        """
        Draw the chess board based on given chess model
        """
        # refresh screen
        self.draw_board()

        # draw the pieces
        self.draw_pieces()

    def user_interface(self, event):
        """
        Get user input (mousepressed) and move the chess pieces
        """
        # when mouse pressed
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            pos_x = pos[0]
            pos_y = pos[1]

            x = (pos_x - self.padding) // self.square_size
            y = 7 - (pos_y - self.padding) // self.square_size

            # mouse pressed somewhere in the chess board
            if x >= 0 and x <= 7 and y >= 0 and y <= 7:
                current_square = self.board_xy_to_num(x, y)
                if self.selected_square is None:
                    piece = self.board.piece_at(current_square)
                    if piece is not None:
                        self.selected_square = current_square
                else:
                    self.control.move(self.selected_square, current_square)
                    self.selected_square = None
                    self.control.bot_move()

    def draw_board(self):
        """
        Draw chess board
        """
        self.screen.blit(self.board_image, (0, 0))

    def draw_pieces(self):
        """
        Draw pieces onto board
        """
        for i in range(0, 64):
            piece = self.board.piece_at(i)
            y = i // 8
            x = i - (y * 8)
            if piece is not None:
                piece = str(piece)
                pos_x = x * self.square_size + self.padding + 33
                pos_y = (7 - y) * self.square_size + self.padding - 7
                self.screen.blit(
                    self.piece_image[piece],
                    (
                        pos_x,
                        pos_y,
                    ),
                )

    def scaled_chess_piece(self, image_link, scale_ratio):
        """
        Scale chess sprite by x times
        """
        return pygame.transform.scale_by(pygame.image.load(image_link), scale_ratio)

    def board_xy_to_num(self, x, y):
        """
        takes an x, y coordinate of a board returns a value from 0 to 63
        signifying the position of the piece
        """
        return int(y * 8 + x)
