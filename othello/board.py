import pygame
from .globals import BLACK, WHITE, ROWS, COLUMNS, SQUARE_SIZE, GREEN, YELLOW
from .tile import Tile

class Board:
    def __init__(self):
        self.board = []
        self.white_tiles = 2
        self.black_tiles = 2
        self.starting_board()
        self.blacks_turn = True
    
    def draw_board(self, screen):
        
        for row in range(ROWS):
            for col in range(COLUMNS):
                # Calculate the position of each square based on row and column
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE

                # Draw the green square
                pygame.draw.rect(screen, GREEN, (x, y, SQUARE_SIZE, SQUARE_SIZE))

                # Draw the black border around each square
                pygame.draw.rect(screen, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE), 2)
        
    def starting_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLUMNS):
                if row == 3 and col == 3:
                    self.board[row].append(Tile(row, col, WHITE))
                elif row == 3 and col == 4:
                    self.board[row].append(Tile(row, col, BLACK))
                elif row == 4 and col == 3:
                    self.board[row].append(Tile(row, col, BLACK))
                elif row == 4 and col == 4:
                    self.board[row].append(Tile(row, col, WHITE))
                elif row == 2 and col == 3:
                    self.board[row].append(Tile(row, col, WHITE))
                elif row == 2 and col == 5:
                    self.board[row].append(Tile(row, col, WHITE))
                elif row == 5 and col == 2:
                    self.board[row].append(Tile(row, col, WHITE))
                elif row == 4 and col == 5:
                    self.board[row].append(Tile(row, col, WHITE))
                elif row == 4 and col == 6:
                    self.board[row].append(Tile(row, col, WHITE))
                elif row == 4 and col == 7:
                    self.board[row].append(Tile(row, col, WHITE))
                else:
                    self.board[row].append(0)
            else:
                self.board[row].append(0) 

    def draw_tiles(self, screen):
        self.draw_board(screen)
        for row in range(ROWS):
            for col in range(COLUMNS):
                tile = self.board[row][col]
                if tile != 0:
                    tile.draw_tile(screen)

    def get_tiles(self, color):
        list_of_tiles = []
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.board[row][col] != 0 and self.board[row][col].color == color:
                    list_of_tiles.append(self.board[row][col])
        return list_of_tiles

    def check_up(self, tile, opposite_color):
        #print("Checking Tile At: ", tile.row, tile.column)
        up = tile.row - 1
        if self.board[up][tile.column] != 0:
            while self.board[up][tile.column].color == opposite_color and up > 0:
                
                up -= 1
                if self.board[up][tile.column] == 0:
                    break
            
            if self.board[up][tile.column] == 0:
                return (up, tile.column)

    def check_down(self, tile, opposite_color):
        #print("Checking Tile At: ", tile.row, tile.column)
        down = tile.row + 1
        if self.board[down][tile.column] != 0:
            while self.board[down][tile.column].color == opposite_color and down < ROWS-1:
                
                down += 1
                if self.board[down][tile.column] == 0:
                    break
            
            if self.board[down][tile.column] == 0:
                return (down, tile.column)

    def check_left(self, tile, opposite_color):
        #print("Checking Tile At: ", tile.row, tile.column)
        left = tile.column - 1
        if self.board[tile.row][left] != 0:
            while self.board[tile.row][left].color == opposite_color and left > 0:
                
                left -= 1
                if self.board[tile.row][left] == 0:
                    break
            
            if self.board[tile.row][left] == 0:
                return (tile.row, left)

    def check_right(self, tile, opposite_color):
        #print("Checking Tile At: ", tile.row, tile.column)
        right = tile.column + 1
        if self.board[tile.row][right] != 0:
            while self.board[tile.row][right].color == opposite_color and right < COLUMNS-1:
                
                right += 1
                if self.board[tile.row][right] == 0:
                    break
            
            if self.board[tile.row][right] == 0:
                return (tile.row, right)

    def check_left_up(self, tile, opposite_color):
        #print("Checking Tile At: ", tile.row, tile.column)
        left = tile.column - 1
        up = tile.row - 1
        if self.board[up][left] != 0:
            while self.board[up][left].color == opposite_color and left > 0 and up > 0:
                
                left -= 1
                up -= 1
                if self.board[up][left] == 0:
                    break
            
            if self.board[up][left] == 0:
                return (up, left)

    def check_right_up(self, tile, opposite_color):
        #print("Checking Tile At: ", tile.row, tile.column)
        right = tile.column + 1
        up = tile.row - 1
        if self.board[up][right] != 0:
            while self.board[up][right].color == opposite_color and right < COLUMNS-1 and up > 0:
                
                right += 1
                up -= 1
                if self.board[up][right] == 0:
                    break
            
            if self.board[up][right] == 0:
                return (up, right)

    def check_left_down(self, tile, opposite_color):
        #print("Checking Tile At: ", tile.row, tile.column)
        left = tile.column - 1
        down = tile.row + 1
        if self.board[down][left] != 0:
            while self.board[down][left].color == opposite_color and left > 0 and down < ROWS-1:
                
                left -= 1
                down += 1
                if self.board[down][left] == 0:
                    break
            
            if self.board[down][left] == 0:
                return (down, left)

    def check_right_down(self, tile, opposite_color):
        #print("Checking Tile At: ", tile.row, tile.column)
        right = tile.column + 1
        down = tile.row + 1
        if self.board[down][right] != 0:
            while self.board[down][right].color == opposite_color and right < COLUMNS-1 and down < ROWS-1:
                
                right += 1
                down += 1
                if self.board[down][right] == 0:
                    break
            
            if self.board[down][right] == 0:
                return (down, right)
    
    def find_moves(self, tile, opposite_color):
        possible_moves = []
        if up := self.check_up(tile, opposite_color):
            possible_moves.append(up)
        if down := self.check_down(tile, opposite_color):
            possible_moves.append(down)
        if left := self.check_left(tile, opposite_color):
            possible_moves.append(left)
        if right := self.check_right(tile, opposite_color):
            possible_moves.append(right)
        if left_up := self.check_left_up(tile, opposite_color):
            possible_moves.append(left_up)
        if right_up := self.check_right_up(tile, opposite_color):
            possible_moves.append(right_up)
        if left_down := self.check_left_down(tile, opposite_color):
            possible_moves.append(left_down)
        if right_down := self.check_right_down(tile, opposite_color):
            possible_moves.append(right_down)

        if possible_moves:
            return possible_moves

    def valid_moves(self, screen):
        valid_moves = []

        if self.blacks_turn == True:
            black_tiles = self.get_tiles(BLACK)
            for tile in black_tiles:
                if black_moves := self.find_moves(tile, WHITE):
                    valid_moves.append(black_moves)
                
                
        else:
            white_tiles = self.get_tiles(WHITE)
            for tile in white_tiles:
                if white_moves := self.find_moves(tile, BLACK):
                    valid_moves.append(white_moves)
        
        if valid_moves:
            valid_moves = [item for sublist in valid_moves for item in sublist] #collapses the earlier valid_moves
            #print(valid_moves)
            self.print_moves(valid_moves, screen)

    def print_moves(self, valid_moves, screen):

        for (row, col) in valid_moves:
           
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2

            radius = SQUARE_SIZE//2 - 30

            pygame.draw.circle(screen, YELLOW, (x, y), radius)
            
            
            
            
                        


