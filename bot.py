from collections import deque # where we store data
from othello.board import Board
import random
import numpy as np

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Bot:
    def __init__(self, color):
        self.game_iterations = 0
        self.epsilon = 0 # in oder to controll randomness
        self.reward = 0
        self.color = color
        self.gamma = 0 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # if we exeede memory we popleft()
    
    def get_board_state(self, board):
        nr_white_tiles = board.white_tiles
        nr_black_tiles = board.black_tiles
        current_state = board.current_state

        return current_state
        # valid moves
        # current board

    def remember(self, board_state, move, reward, next_board_state, game_over):
        self.memory.append((board_state, move, reward, next_board_state, game_over))

    def bot_trainer_long_memory(self):
        pass

    def bot_trainer_short_memory(self, board_state, move, reward, next_board_state, game_over):
        pass

    def move_heuristics(self, move):
        if move == (0, 0) or move == (0, 7) or move == (7, 0) or move == (7, 7):
            return 100
        elif (move[0] == 0 or move[0] == 7) or (move[1] == 0 or move[1] == 7):
            return 50
        else:
            return 1

    def get_move(self, valid_moves):
        next_move = None
        best_score = 0 #-float('inf')

        for move in valid_moves:
            move_score = self.move_heuristics(move)
            print("move_score: ", move_score)
            if move_score > best_score:
                best_score = move_score
                next_move = move  

        if next_move in [(0, 0), (0, 7), (7, 0), (7, 7)]:
            return next_move
        else:
            return random.choice(valid_moves)
            

    # play(action) -> move
    def move(self, move, board):
        old_score = 0
        row, col = move
        reward = 0
        score = 0

        if self.color == "Black":
            old_score = board.black_tiles
        else:
            old_score = board.white_tiles
        
        board.make_move(row, col)

        if move == (0, 0) or move == (0, 7) or move == (7, 0) or move == (7, 7):
            reward += 10

        #if self.color == "Black":
        #    reward += board.black_tiles - old_score
        #else:
        #    reward += board.white_tiles - old_score

        #if self.color == "Black":
        #    score = board.black_tiles - board.white_tiles
        #else:
        #    score = board.white_tiles - board.black_tiles
        
        return reward, score


    def set_reward(self, color, value):
        self.reward = value
        print(color + " reward: " + str(self.reward))

def train_bot():
    scores_black = [] # for plotting progress
    scores_white = [] # for plotting progress
    
    record_black = 0
    record_white = 0

    agent_black = Bot("Black")
    agent_white = Bot("White")
    board = Board()
    game_over = False

    while True:
        # get old state
        state_old = board.current_state()

        # get move
        valid_moves = board.valid_moves()

        if board.blacks_turn:
            final_move = agent_black.get_move(state_old, valid_moves)

            # perform move and get new state
            reward, score = agent_black.move(final_move, board)
            state_new = agent_black.get_board_state(board)

            #Check if game is over
            valid_moves = board.valid_moves()
            if valid_moves == []:
                game_over = True

            # train short memory
            agent_black.bot_trainer_short_memory(state_old, final_move, reward, state_new, game_over)

            # remember
            agent_black.remember(state_old, final_move, reward, state_new, game_over)

        else:
            final_move = agent_white.get_move(state_old, valid_moves)

            # perform move and get new state
            reward, score = agent_white.move(final_move, board)
            state_new = agent_white.get_board_state(board)

            #Check if game is over
            valid_moves = board.valid_moves()
            if valid_moves == []:
                game_over = True

            # train short memory
            agent_white.bot_trainer_short_memory(state_old, final_move, reward, state_new, game_over)

            # remember
            agent_white.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            # train long memory, plot result
            black_score = board.black_tiles
            white_score = board.white_tiles

            board = Board()
            agent_black.game_iterations += 1
            agent_black.bot_trainer_long_memory()
            agent_white.game_iterations += 1
            agent_white.bot_trainer_long_memory()

            if black_score > record_black:
                record_black = black_score
                # agent.model.save()

            if white_score > record_white:
                record_white = white_score

            print('Game:', agent.game_iterations, 'Score:', score, 'Record:', record)

            # TODO: plot

#if __name__ == '__main__':
#    train_bot()