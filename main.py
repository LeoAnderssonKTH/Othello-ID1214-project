import pygame
from othello.globals import SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE
from othello.board import Board
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Othello')

FPS = 5

def get_mouse_pos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()

    while run:
        clock.tick(FPS)
        
        # Handle events first
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos)
                #print(valid_moves)
                #board.print_board()

                # Check if the clicked position is a valid move
                if (row, col) in valid_moves:
                    board.make_move(row, col)

        # Update the board display
        board.draw_tiles(SCREEN)
        valid_moves = board.valid_moves(SCREEN)  # Re-calculate valid moves
        
        pygame.display.update()

    pygame.quit()

main()
