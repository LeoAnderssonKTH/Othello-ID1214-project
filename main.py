import pygame
from othello.globals import SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE
from othello.board import Board
from bot import Bot
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Othello')
import time

FPS = 1

def get_mouse_pos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()
    # frame_iteration = 0 # might be important for teaching the bot
    bot1 = Bot("Black")
    bot2 = Bot("White")
    valid_moves = board.valid_moves() # initialize valid_moves
    toggle = 1

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Bot 1 moves first
        if toggle == 1:
            move = bot1.get_move(valid_moves)
            bot1.move(move, board)
            toggle = 2

        # Bot 2 moves second
        if toggle == 2:
            move = bot2.get_move(valid_moves)
            bot2.move(move, board)
            toggle = 1
        

# ====================================================================
#        
#        # Handle events first
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                run = False
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
        #frame_iterations += 1 # updates the frame iteration
        valid_moves = board.valid_moves()  # Re-calculate valid moves
        board.print_moves(valid_moves, SCREEN)
        print(valid_moves)
        current_state = board.current_state()
        #print(current_state)
        #print()
        
        pygame.display.update()

        if valid_moves == []:
            print("Black Tiles: ", board.black_tiles)
            print("White Tiles: ", board.white_tiles)

            if board.black_tiles > board.white_tiles:
                print("Black Wins!")
                bot1.set_reward("white", 10)
                bot2.set_reward("black", -10)
            else:
                print("White Wins!")
                bot2.set_reward("white", 10)
                bot1.set_reward("black", -10)
            print("Restarting Game in 5 seconds")
            #time.sleep(5)
            #frame_iterations = 0 # resets the frame iterations
            board = Board()
            valid_moves = board.valid_moves()
            board.print_moves(valid_moves, SCREEN)
                   

    pygame.quit()
    

main()
