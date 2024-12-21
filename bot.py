from collections import deque # where we store data
from othello.board import Board

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Bot:
    def __init__(self):
        #self.game_iterations = 0
        #self.epsilon = 0 # in oder to controll randomness
        self.reward = 0
        #self.gamma = 0 #discount rate
        #self.memory = deque(maxlen=MAX_MEMORY) # if we exeede memory we popleft()
    
    def get_board_state(self, board):
        nr_white_tiles = board.white_tiles
        nr_black_tiles = board.black_tiles
        # valid moves
        # current board

    def remember(self, board_state, move, reward, next_board_state, game_over):
        pass

    def bot_trainer_long_memory(self):
        pass

    def bot_trainer_short_memory(self, board_state, move, reward, next_board_state, game_over):
        pass

    def get_move(self, board_state):
        pass

    # play(action) -> move
    def move(self, valid_moves):
        # heuristics should be implemented based 
        # on valid_moves
        
        # for now the bot will simply return the 
        # first valid move
        start_index = 0
        end_index = len(valid_moves) - 1
        (row, col) = (valid_moves[0][0], valid_moves[0][1])
        return (row, col)

    def set_reward(self, color, value):
        self.reward = value
        print(color + " reward: " + str(self.reward))

def train_bot():
    scores = [] # for plotting progress
    mean_scores = []
    total_score = 0
    record = 0
    agent = Bot()
    board = Board()

    # get old state
    state_old = agent.get_board_state(board)

    # get move
    final_move = agent.get_move(state_old)

    # perform move and get new state
    reward, game_over, score = board.make_move(final_move)
    state_new = agent.get_board_state(board)

    # train short memory
    agent.bot_trainer_short_memory(state_old,final_move, reward, state_new, game_over)

    # remember
    agent.remember(state_old,final_move, reward, state_new, game_over)

    if game_over:
        # train long memory, plot result
        board.reset
        agent.game_iterations += 1
        agent.bot_trainer_long_memory()

        if score > record:
            record = score
            # agent.model.save()

        print('Game:', agent.game_iterations, 'Score:', score, 'Record:', record)

        # TODO: plot

#if __name__ == '__main__':
#    train_bot()