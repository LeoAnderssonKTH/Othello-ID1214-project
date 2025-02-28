from collections import deque # where we store data
from othello.board import Board
import random
import numpy as np
from model import QNetwork, QTrainer
import copy
import torch
import pygame

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.01

class Bot:
    def __init__(self, color):
        self.game_iterations = 0
        self.epsilon = 1 # in oder to controll randomness
        self.reward = 0.9
        self.color = color
        self.gamma = 0.9 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # if we exeede memory we popleft()
        self.model = QNetwork(64, 128, 128, 64)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def load_model(self, path):
        self.model.load_state_dict(torch.load(path))
        

    def remember(self, board_state, move, reward, next_board_state, game_over):
        self.memory.append((board_state, move, reward, next_board_state, game_over))

    def long_memory_trainer(self):
        if len(self.memory) > BATCH_SIZE:
            sample = random.sample(self.memory, BATCH_SIZE)
        else: 
            sample = self.memory

        boards, moves, rewards, next_boards, game_overs = zip(*sample) #unzipps sample data
        self.trainer.train_step(boards, moves, rewards, next_boards, game_overs)

    def short_memory_trainer(self, board_state, move, reward, next_board_state, game_over):
        self.trainer.train_step(board_state, move, reward, next_board_state, game_over)

    def move_heuristics(self, move):
        if move == (0, 0) or move == (0, 7) or move == (7, 0) or move == (7, 7):
            return 100
        elif (move[0] == 0 or move[0] == 7) or (move[1] == 0 or move[1] == 7):
            return 50
        else:
            return 1

    def get_move(self, state, valid_moves, board):
        next_move = None
        best_score = -float('inf')
        #print(state)

        #for move in valid_moves:
            #move_score = self.move_heuristics(move)
            #if move_score > best_score:
             #   best_score = move_score
              #  next_move = move  

        #If a move is found in one of the corners, return it immediately
        #if next_move in [(0, 0), (0, 7), (7, 0), (7, 7)]:
           # return next_move
        #else:
            # If no corners found use model to decide move
           # best_score = -float('inf')

        for move in valid_moves:
            # Deep copy the board to simulate the move
            board_copy = copy.deepcopy(board)
            row, col = move
            board_copy.make_move(row, col)

            # Get the new state of the board after the move
            new_state = board_copy.current_state()

            # Convert the board state to 1D tensor so it can be passed to the model
            flattened_state = [tile for row in new_state for tile in row]

            state_tensor = torch.tensor(flattened_state, dtype=torch.float32).unsqueeze(0) 

            # Get Q-values from the model (model should output Q-values for all possible moves)
            q_values = self.model(state_tensor)

            # Get valid move indices in the flattened board representation
            valid_indices = [move[0] * 8 + move[1] for move in valid_moves]

            # Filter Q-values for valid moves
            valid_q_values = q_values[0][valid_indices]

            # Match each valid move to its Q-value
            for move, q_value in zip(valid_moves, valid_q_values):
                move_score = q_value.item()
                if move_score > best_score:
                    best_score = move_score
                    next_move = move

        return next_move

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
 #       elif move[0] == 0 or move[0] == 7 or move[1] == 0 or move[1] == 7:
  #          reward += 5
        #lägg till så den koller för mest flippade movet också
   #     else:
    #        reward -= 2

        #if self.color == "Black":
            #reward += board.black_tiles - old_score
        #else:
            #reward += board.white_tiles - old_score

        #if self.color == "Black":
            #score = board.black_tiles - board.white_tiles
        #else:
            #score = board.white_tiles - board.black_tiles
        
        return reward

    def set_reward(self, color, value):
        self.reward = value
        #print(color + " reward: " + str(self.reward))

def train_bot():
    scores_black = [] # for plotting progress
    scores_white = [] # for plotting progress

    black_won_last = False

    record_black = 0
    record_white = 0
    FPS = 500

    black_lose_streak = 0
    white_lose_streak = 0
    

    games_played = 0
    black_wins = 0
    white_wins = 0
    draws = 0

    agent_black = Bot("Black")
    agent_white = Bot("White")
    #agent_black.load_model("model/black_bot")
    #agent_white.load_model("model/white_bot")
    
    game_over = False
    board = Board()
    game_over = False
    #clock = pygame.time.Clock()
    run = True

    while run:
        #clock.tick(FPS)
        #for event in pygame.event.get():
            #if event.type == pygame.QUIT:
                #run = False
        
        #board.draw_tiles(screen)
        # get old state
        old_board = board.current_state()

        # get move
        valid_moves = board.valid_moves()
        #board.print_moves(valid_moves, screen)

        if board.blacks_turn:
            final_move = agent_black.get_move(old_board, valid_moves, board)#gets a move based on heuristics
            reward = agent_black.move(final_move, board)#makes a move and gets the reward and score from the move made
            next_board = board.current_state()#gets updates board after move
            
            valid_moves = board.valid_moves()#updates valid_moves after bot's move
            if valid_moves == []:#checks if game is over
                game_over = True

            #Check if we leave a corner open
            corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
            for corner in corners:
                if corner in valid_moves:
                    reward -= 10
                    break

            agent_black.short_memory_trainer(old_board, final_move, reward, next_board, game_over)# trains the bots short memory
            agent_black.remember(old_board, final_move, reward, next_board, game_over)#appends the game state, bot move and reward to memory

        else:
            #same thing as above but with the white player instead of black
            final_move = agent_white.get_move(old_board, valid_moves, board)
            reward = agent_white.move(final_move, board)
            next_board = board.current_state()

            valid_moves = board.valid_moves()
            if valid_moves == []:
                game_over = True

            corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
            for corner in corners:
                if corner in valid_moves:
                    reward -= 10
                    break

            agent_white.short_memory_trainer(old_board, final_move, reward, next_board, game_over)
            agent_white.remember(old_board, final_move, reward, next_board, game_over)

        #pygame.display.update()

        if game_over:
            games_played +=1

            agent_black.memory
          
            black_score = board.black_tiles
            white_score = board.white_tiles

            if black_score > record_black:
                record_black = black_score
                agent_black.model.save("black_bot_v2")

            if white_score > record_white:
                record_white = white_score
                agent_white.model.save("white_bot_v2")

            if black_score > white_score:
                black_wins += 1
                white_lose_streak += 1
                black_lose_streak = 0
                
                blacks_last_move = agent_black.memory[-1]
                board_state, move, reward, next_board_state, game_over = blacks_last_move
                agent_black.memory[-1] = (board_state, move, 100, next_board_state, game_over)

                whites_last_move = agent_white.memory[-1]
                board_state, move, reward, next_board_state, game_over = whites_last_move
                agent_white.memory[-1] = (board_state, move, -100, next_board_state, game_over)
                if black_won_last == False:
                    agent_black.model.save("black_bot_v2")
                    black_won_last = True

                #print("BLACK WINS")
            
            if white_score > black_score:
                white_wins += 1
                black_lose_streak += 1
                white_lose_streak = 0
                
                blacks_last_move = agent_black.memory[-1]
                board_state, move, reward, next_board_state, game_over = blacks_last_move
                agent_black.memory[-1] = (board_state, move, -100, next_board_state, game_over)

                whites_last_move = agent_white.memory[-1]
                board_state, move, reward, next_board_state, game_over = whites_last_move
                agent_white.memory[-1] = (board_state, move, 100, next_board_state, game_over)

                if black_won_last == True:
                    agent_white.model.save("white_bot_v2")
                    black_won_last = False
                
                #print("WHITE WINS")

            if white_score == black_score:
                draws += 1

                blacks_last_move = agent_black.memory[-1]
                board_state, move, reward, next_board_state, game_over = blacks_last_move
                agent_black.memory[-1] = (board_state, move, -50, next_board_state, game_over)

                whites_last_move = agent_white.memory[-1]
                board_state, move, reward, next_board_state, game_over = whites_last_move
                agent_white.memory[-1] = (board_state, move, -50, next_board_state, game_over)

                #print("DRAW")

            agent_black.game_iterations += 1
            agent_black.long_memory_trainer()
            agent_white.game_iterations += 1
            agent_white.long_memory_trainer()

            agent_black.epsilon = max(0.01, agent_black.epsilon * 0.9995)  # Exponential decay
            agent_white.epsilon = max(0.01, agent_white.epsilon * 0.9995)

            if black_lose_streak == 10 and agent_black.epsilon < 0.25:
                black_lose_streak = 0
                agent_black.epsilon = min(0.25, agent_black.epsilon + 0.05)

            if white_lose_streak == 10 and agent_white.epsilon < 0.25:
                white_lose_streak = 0
                agent_white.epsilon = min(0.25, agent_white.epsilon + 0.05)

            game_over = False
            board = Board()
            #pygame.display.update()
            print(games_played)

            if games_played % 100 == 0:
                print()
                print("Black Epsilon :", agent_black.epsilon)
                print("White Epsilon :", agent_white.epsilon)
                print()
                print("Amount of games: ", games_played)
                print("Black Wins: ", black_wins)
                print("White Wins: ", white_wins)
                print("Draws: ", draws)

def train_bot_random():
    scores_black = [] # for plotting progress
    scores_white = [] # for plotting progress

    black_won_last = False

    record_black = 0
    record_white = 0
    FPS = 500

    black_lose_streak = 0
    white_lose_streak = 0

    black_best_winrate = 0

    games_played = 0
    black_wins = 0
    white_wins = 0
    draws = 0
   


    agent_black = Bot("Black")
    #agent_white = Bot("White")
    #agent_black.load_model("model/black_bot_v3")
    #agent_black.epsilon = 0.5
    #agent_white.load_model("model/white_bot")
    board = Board()
    game_over = False
    
    
    #clock = pygame.time.Clock()
    run = True

    while run:
        
        #clock.tick(FPS)
        #for event in pygame.event.get():
            #if event.type == pygame.QUIT:
                #run = False
        
        #board.draw_tiles(screen)
        # get old state
        old_board = board.current_state()

        # get move
        valid_moves = board.valid_moves()
        #board.print_moves(valid_moves, screen)

        if board.blacks_turn:
            final_move = agent_black.get_move(old_board, valid_moves, board)#gets a move based on heuristics
            reward = agent_black.move(final_move, board)#makes a move and gets the reward and score from the move made
            next_board = board.current_state()#gets updates board after move
            
            valid_moves = board.valid_moves()#updates valid_moves after bot's move
            if valid_moves == []:#checks if game is over
                game_over = True


            agent_black.short_memory_trainer(old_board, final_move, reward, next_board, game_over)# trains the bots short memory
            agent_black.remember(old_board, final_move, reward, next_board, game_over)#appends the game state, bot move and reward to memory

        else:
            move = None
            #time.sleep(2)
            corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
            for corner in corners:
                if corner in valid_moves:
                    move = corner
                    break
                
            if move:
                board.make_move(move[0], move[1])
            else:
                move = random.choice(valid_moves)
                board.make_move(move[0], move[1])

            valid_moves = board.valid_moves()#updates valid_moves after bot's move
            if valid_moves == []:#checks if game is over
                
                game_over = True
                


        #pygame.display.update()

        if game_over:
            games_played +=1

            agent_black.memory
          
            black_score = board.black_tiles
            white_score = board.white_tiles


            if black_score > white_score:
                black_wins += 1
                white_lose_streak += 1
                black_lose_streak = 0
                
                blacks_last_move = agent_black.memory[-1]
                board_state, move, reward, next_board_state, bot_memory_game_over = blacks_last_move
                agent_black.memory[-1] = (board_state, move, 100, next_board_state, True)


                #print("BLACK WINS")
            
            if white_score > black_score:
                white_wins += 1
                black_lose_streak += 1
                white_lose_streak = 0
                
                blacks_last_move = agent_black.memory[-1]
                board_state, move, reward, next_board_state, bot_memory_game_over = blacks_last_move
                agent_black.memory[-1] = (board_state, move, -100, next_board_state, True)

                
                #print("WHITE WINS")

            if white_score == black_score:
                draws += 1

                blacks_last_move = agent_black.memory[-1]
                board_state, move, reward, next_board_state, bot_memory_game_over = blacks_last_move
                agent_black.memory[-1] = (board_state, move, -50, next_board_state, True)


                #print("DRAW")

            agent_black.game_iterations += 1
            agent_black.long_memory_trainer()
           
            
            if games_played < 10000:
                agent_black.epsilon = max(0.1, agent_black.epsilon - 0.00001)
            elif games_played < 15000:
                agent_black.epsilon = max(0.05, agent_black.epsilon - 0.0001)
            else:
                agent_black.epsilon = max(0.01, agent_black.epsilon - 0.001)
           

            if black_lose_streak == 10 and agent_black.epsilon < 0.3:
                black_lose_streak = 0
                agent_black.epsilon = min(0.3, agent_black.epsilon + 0.1)

            game_over = False
            board = Board()
            #pygame.display.update()
            print(games_played)

            if games_played % 100 == 0:

                current_winrate = black_wins / 100

                if black_best_winrate < current_winrate and games_played > 10000 and agent_black.epsilon < 0.35:
                    black_best_winrate = current_winrate
                    agent_black.model.save("black_bot_v5")

                if current_winrate < 0.5 and agent_black.epsilon < 0.3:
                    agent_black.epsilon = min(0.3, agent_black.epsilon + 0.1)


                print()
                print("Black Epsilon :", agent_black.epsilon)
                print()
                print("Amount of games: ", games_played)
                print("Stats for the last 100 games")
                print("Black Wins: ", black_wins)
                print("White Wins: ", white_wins)
                print("Draws: ", draws)      
                print("Black Winrate: ", current_winrate)

                black_wins = 0
                white_wins = 0
                draws = 0     

            

if __name__ == '__main__':
   train_bot()
   train_bot_random()
