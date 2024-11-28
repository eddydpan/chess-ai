"""
Run a chess game
"""

import pygame
import view
import controller
import chess


def main():
    """
    Starts the game of chess!
    """
    pygame.init()
    clock = pygame.time.Clock()

    board = chess.Board()

    chess_view = view.DrawGame(board)

    run = True
    while run:

        for event in pygame.event.get():  # close game when x is pressed
            if event.type == pygame.QUIT:
                run = False
            # do things when user mouse presses something
            chess_view.user_interface(event)

        chess_view.draw()  # draw the chess board onto next screen

        pygame.display.flip()  # update the screen

        clock.tick(30)  # 30 fps

    pygame.quit()


if __name__ == "__main__":
    main()
