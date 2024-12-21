import pygame
from othello.globals import SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE
from othello.board import Board
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Othello')
import time

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
            
                # Check if the clicked position is a valid move
               
                if (row, col) in valid_moves:
                    board.make_move(row, col)
                    break

        # Update the board display
        board.draw_tiles(SCREEN)
        valid_moves = board.valid_moves(SCREEN)  # Re-calculate valid moves
        
        pygame.display.update()

        if valid_moves == []:
            print("Black Tiles: ", board.black_tiles)
            print("White Tiles: ", board.white_tiles)

            if board.black_tiles > board.white_tiles:
                print("Black Wins!")
            else:
                print("White Wins!")
            print("Restarting Game in 5 seconds")
            time.sleep(5)
            board = Board()
            

    pygame.quit()
    

main()
