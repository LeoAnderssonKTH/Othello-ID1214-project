from collections import deque # where we store data
from othello.board import Board
import random
import numpy as np
from model import QNetwork, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Bot:
    def __init__(self, color):
        self.game_iterations = 0
        self.epsilon = 0 # in oder to controll randomness
        self.reward = 0.9
        self.color = color
        self.gamma = 0 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # if we exeede memory we popleft()
        #self.model = QNetwork(64, 128, 60)
        #self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    
    #def get_board(self, board):
        #nr_white_tiles = board.white_tiles
        #nr_black_tiles = board.black_tiles
        #current_board = board.current_state()
        #return current_board
        # valid moves
        # current board

    def add_move_to_memory(self, current_board, move, reward, next_board, game_over):
        self.memory.append((current_board, move, reward, next_board, game_over))

    def long_memory_training(self):
        if self.memory > BATCH_SIZE:
            sample = random.sample(self.memory, BATCH_SIZE)
        else: 
            sample = self.memory

        boards, moves, rewards, next_boards, game_overs = zip(*sample) #unzipps sample data
        self.model.train(boards, moves, rewards, next_boards, game_overs)

    def short_memory_training(self, current_board, move, reward, next_board, game_over):
        self.model.train(current_board, move, reward, next_board, game_over)

    def move_heuristics(self, move):
        if move == (0, 0) or move == (0, 7) or move == (7, 0) or move == (7, 7):
            return 100
        elif (move[0] == 0 or move[0] == 7) or (move[1] == 0 or move[1] == 7):
            return 50
        #lägg till så den koller för mest flippade movet också
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
        elif move[0] == 0 or move[0] == 7 or move[1] == 0 or move[1] == 7:
            reward += 5
        #lägg till så den koller för mest flippade movet också
        else:
            reward -= 2

        #if self.color == "Black":
        #    reward += board.black_tiles - old_score
        #else:
        #    reward += board.white_tiles - old_score

        #if self.color == "Black":
        #    score = board.black_tiles - board.white_tiles
        #else:
        #    score = board.white_tiles - board.black_tiles

        return reward


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
        current_board = board.current_state()
        valid_moves = board.valid_moves

        if board.blacks_turn:
            final_move = agent_black.get_move(valid_moves)#gets a move based on heuristics
            reward = agent_black.move(final_move, board)#makes a move and gets the reward and score from the move made
            #next_board = agent_black.get_board(board)
            next_board = board.current_state()#gets updates board after move
            
            valid_moves = board.valid_moves()#updates valid_moves after bot's move
            if valid_moves == []:#checks if game is over
                game_over = True

            #trains short memory and adds the move to the memory
            agent_black.short_memory_training(current_board, final_move, reward, next_board, game_over)
            agent_black.add_move_to_memory(current_board, final_move, reward, next_board, game_over)

        else:
            final_move = agent_white.get_move(valid_moves)#gets a move based on heuristics
            reward, score = agent_white.move(final_move, board)#makes a move and gets the reward and score from the move made
            #next_board = agent_white.get_board(board)
            next_board = board.current_state()#gets updates board after move

            valid_moves = board.valid_moves()#updates valid_moves after bot's move
            if valid_moves == []:#checks if game is over
                game_over = True

            #trains short memory and adds the move to the memory
            agent_white.short_memory_training(current_board, final_move, reward, next_board, game_over)
            agent_white.add_move_to_memory(current_board, final_move, reward, next_board, game_over)

        if game_over:
            # train long memory, plot result
            #board = Board()
            black_score = board.black_tiles
            white_score = board.white_tiles

            black_reward = 0
            white_reward = 0

            board = Board()#resets board
            agent_black.game_iterations += 1
            agent_black.long_memory_training()#trains the bot's long memory
            agent_white.game_iterations += 1
            agent_white.long_memory_training()#trains the bot's long memory

            if black_score > record_black:
                record_black = black_score
                # agent.model.save()

            if white_score > record_white:
                record_white = white_score

            if black_score > white_score:
                black_reward = 1
                white_reward = -1
            
            if white_score > black_score:
                white_reward = 1
                black_reward = -1

            #print('Game:', agent.game_iterations, 'Score:', score, 'Record:', record)

            # TODO: plot

#if __name__ == '__main__':
#    train_bot()