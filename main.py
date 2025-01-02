import pygame
from othello.globals import SCREEN_WIDTH, SCREEN_HEIGHT, SQUARE_SIZE
from othello.board import Board
from bot import Bot, train_bot
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Othello')
import time
import torch

FPS = 20

def get_mouse_pos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()

    path_to_bot = "./model/black_bot_v2"

    black_bot = Bot("Black")

    black_bot.model.load_state_dict(torch.load(path_to_bot))

    black_bot.model.eval()

    black_bot.epsilon = 0
    
    #print("Starting Board: ")
    #print(board.current_state)
    # frame_iteration = 0 # might be important for teaching the bot
    #bot1 = Bot("Black")
    #bot2 = Bot("White")
    #valid_moves = board.valid_moves() # initialize valid_moves
    #toggle = 1

    #train_bot()

    while run:
        clock.tick(FPS)
       
        current_state = board.current_state()
        valid_moves = board.valid_moves()
        board.draw_tiles(SCREEN)
        board.print_moves(valid_moves, SCREEN)
        pygame.display.update()
        
        # Play versus bot 
        if board.blacks_turn:
            time.sleep(2)
            move = black_bot.get_move(current_state, valid_moves, board)
            black_bot.move(move, board)

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
        #print(valid_moves)
        current_state = board.current_state()
        #print(current_state)
        #print()
        pygame.display.update()

        #time.sleep(2)

        if valid_moves == []:
            print("Black Tiles: ", board.black_tiles)
            print("White Tiles: ", board.white_tiles)

            if board.black_tiles > board.white_tiles:
                print("Black Wins!")
                #bot1.set_reward("white", 10)
                #bot2.set_reward("black", -10)
            else:
                print("White Wins!")
                #bot2.set_reward("white", 10)
                #bot1.set_reward("black", -10)
            print("Restarting Game in 5 seconds")
            time.sleep(5)
            #frame_iterations = 0 # resets the frame iterations
            board = Board()
            valid_moves = board.valid_moves()
            board.print_moves(valid_moves, SCREEN)
            pygame.display.update()
                   

    pygame.quit()
    

main()
