

class Bot:
    def __init__(self):
        pass
    
    # reset needs to happen in main at gameover
    
    # reward

    # play(action) -> move
    def move(self, valid_moves):
        # heuristics should be implemented based 
        # on valid_moves
        
        # for now the bot will simply return the 
        # first valid move
        (row, col) = (valid_moves[0][0], valid_moves[0][1])
        return (row, col)
    
    # game_iteration should be counted in main
    
    # is_gameover is checked for in main