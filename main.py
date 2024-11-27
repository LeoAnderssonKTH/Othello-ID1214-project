import pygame
from othello.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from othello.board import Board
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Othello')

FPS = 60

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
                
        board.draw_board(SCREEN)
        pygame.display.update()
        
    pygame.quit()  # This should be aligned with the `while run:` block

main()
