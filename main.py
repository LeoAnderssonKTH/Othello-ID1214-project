import pygame
from othello.globals import SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE
from othello.board import Board
from bot import Bot
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
    frame_iteration = 0 #important for teaching the bot
    bot1 = Bot()
    bot2 = Bot()

    while run:
        clock.tick(FPS)
        valid_moves = board.valid_moves(SCREEN)
        # Bot 1 moves first
        # Handle events first
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            (row1, col1) = bot1.move(valid_moves)
            if (row1, col1) in valid_moves:
                board.make_move(row1, col1)
                break
# ====================================================================
#    
#            if event.type == pygame.MOUSEBUTTONDOWN:
#                pos = pygame.mouse.get_pos()
#                row, col = get_mouse_pos(pos)
#                #print(valid_moves)
#            
#                # Check if the clicked position is a valid move
#               
#                if (row, col) in valid_moves:
#                    board.make_move(row, col)
#                    break 
#
# ====================================================================

        # Update the board display
        board.draw_tiles(SCREEN)
        valid_moves = board.valid_moves(SCREEN)  # Re-calculate valid moves
        
        pygame.display.update()

        if valid_moves == []:
            print("gameover")
            #break

        # Bot 2 moves second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            (row2, col2) = bot2.move(valid_moves)
            if (row2, col2) in valid_moves:
                board.make_move(row2, col2)
                break
        
        board.draw_tiles(SCREEN)
        valid_moves = board.valid_moves(SCREEN)  # Re-calculate valid moves
        
        pygame.display.update()

        if valid_moves == []:
            print("gameover")
            #break

    pygame.quit()
    

main()
