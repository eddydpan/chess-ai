import pygame
import chess
import controller
import eval


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
        self.potential_moves = []

    def draw(self):
        """
        Draw the chess board based on given chess model
        """
        # refresh screen
        self.draw_board()

        # draw the pieces
        self.draw_pieces()

        self.draw_captured_pieces()
        self.draw_evaluation_bar()

        # highlight selected square and potential moves
        if self.selected_square is not None:
            self.highlight_square(self.selected_square)
            self.highlight_moves(self.potential_moves)

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
                piece = self.board.piece_at(current_square)
                if self.selected_square is None:
                    if piece is not None:
                        self.selected_square = current_square
                        self.potential_moves = self.get_potential_moves(current_square)
                else:
                    move_successful = self.control.move(
                        self.selected_square, current_square
                    )
                    if move_successful:
                        self.selected_square = None
                        self.draw()
                        pygame.display.flip()
                        self.control.bot_move()
                    else:
                        if piece is not None and str(piece) in (
                            "B",
                            "K",
                            "N",
                            "P",
                            "Q",
                            "R",
                        ):
                            self.selected_square = current_square
                            self.potential_moves = self.get_potential_moves(
                                current_square
                            )
                        else:
                            self.selected_square = None

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

    def draw_captured_pieces(self):
        """
        Draw the captured pieces for both black and white players.
        """
        # Define the start positions for displaying captured pieces
        black_start_x, black_start_y = 1060, 100  # Top-right for black captured pieces
        white_start_x, white_start_y = (
            1060,
            600,
        )  # Bottom-right for white captured pieces
        piece_spacing_x = 30  # Spacing between captured pieces
        piece_spacing_y = 50

        # Draw captured black pieces
        for index, piece in enumerate(self.control.captured_pieces_black):
            x = (
                black_start_x + (index % 5) * piece_spacing_x
            )  # Wrap to next line after 8 pieces
            y = black_start_y + (index // 5) * piece_spacing_y
            self.screen.blit(self.piece_image[piece], (x, y))

        # Draw captured white pieces
        for index, piece in enumerate(self.control.captured_pieces_white):
            x = (
                white_start_x + (index % 5) * piece_spacing_x
            )  # Wrap to next line after 8 pieces
            y = white_start_y + (index // 5) * piece_spacing_y
            self.screen.blit(self.piece_image[piece], (x, y))

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

    def highlight_square(self, square):
        """
        Highlight the selected square.
        """
        x = square % 8
        y = square // 8
        pygame.draw.rect(
            self.screen,
            (175, 201, 210),  # Green highlight
            pygame.Rect(
                x * self.square_size + self.padding + 7,
                (7 - y) * self.square_size + self.padding + 7.2,
                self.square_size + 2,
                self.square_size + 2,
            ),
            9,  # Border thickness
        )

    def highlight_moves(self, moves):
        """
        Highlight the potential moves for the selected piece.
        """
        for move in moves:
            x = move % 8
            y = move // 8
            pygame.draw.circle(
                self.screen,
                (1, 71, 90),  # Yellow highlight for potential moves
                (
                    x * self.square_size + self.square_size // 2 + self.padding + 8.5,
                    (7 - y) * self.square_size
                    + self.square_size // 2
                    + self.padding
                    + 8.5,
                ),
                self.square_size // 4,  # Size of the circle
                5,  # Border thickness
            )

    def get_potential_moves(self, square):
        """
        Get all potential moves for a selected piece on the board.
        """
        piece = self.board.piece_at(square)
        if piece is None:
            return []

        # Get the moves for the piece (for simplicity, let's assume we use chess library's legal_moves)
        legal_moves = self.board.legal_moves
        potential_moves = [
            move.to_square for move in legal_moves if move.from_square == square
        ]
        return potential_moves

    def draw_evaluation_bar(self):
        """
        Draws an evaluation bar showing the game's evaluation score.
        """
        eval_score = eval.calc_piece_activity(
            self.board
        )  # Assuming you have an evaluation method in ControlGame
        bar_x = 970  # Positioning the bar on the right
        bar_y = 20
        bar_width = 50
        bar_height = 920

        # Normalize the evaluation score
        normalized_eval = max(-1500, min(1500, eval_score))
        percentage = (normalized_eval + 1500) / 3000  # Map to [0, 1] range
        black = (0, 0, 0)
        white = (255, 255, 255)

        white_height = int(bar_height * percentage)

        black_height = int(bar_height * (1 - percentage))

        # Draw bar background
        pygame.draw.rect(
            self.screen,
            (100, 100, 100),
            (bar_x - 5, bar_y - 5, bar_width + 10, bar_height + 10),
        )

        # Draw the filled part
        pygame.draw.rect(
            self.screen,
            black,
            (bar_x, bar_y, bar_width, black_height),
        )
        pygame.draw.rect(
            self.screen,
            white,
            (bar_x, bar_y + black_height, bar_width, white_height),
        )
