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
        
        up = tile.row - 1

        if up < 0:
            return None

        if self.board[up][tile.column] == 0:
            return None

        if self.board[up][tile.column].color != opposite_color:
            return None
        
        while self.board[up][tile.column].color == opposite_color and up > 0:
                
            up -= 1
            if self.board[up][tile.column] == 0:
                return (up, tile.column)
            
        return None
                

    def check_down(self, tile, opposite_color):

        down = tile.row + 1

        if down > ROWS - 1:
            return None
        
        if self.board[down][tile.column] == 0:
            return None
        
        
        if self.board[down][tile.column].color != opposite_color:
            return None
        
       
        while self.board[down][tile.column].color == opposite_color and down < ROWS-1:
                
            down += 1
            if self.board[down][tile.column] == 0:
                return (down, tile.column)
            
        return None

    def check_left(self, tile, opposite_color):
        left = tile.column - 1

        if left < 0:
            return None

        if self.board[tile.row][left] == 0:
            return None
        if self.board[tile.row][left].color != opposite_color:
            return None
        
        
        while self.board[tile.row][left].color == opposite_color and left > 0:
                
            left -= 1
            if self.board[tile.row][left] == 0:
                return (tile.row, left)
            
        return None
                

    def check_right(self, tile, opposite_color):
        right = tile.column + 1
        

        if right > COLUMNS - 1:
            return None
        
        if self.board[tile.row][right] == 0:
            return None
        
        if self.board[tile.row][right].color != opposite_color:
            return None
        
        while self.board[tile.row][right].color == opposite_color and right < COLUMNS-1:
                
            right += 1
            if self.board[tile.row][right] == 0:
                return (tile.row, right)

        return None  
                

    def check_left_up(self, tile, opposite_color):
        left = tile.column - 1
        up = tile.row - 1

        if up < 0 or left < 0:
            return None

        if self.board[up][left] == 0:
            return None
        
        if self.board[up][left].color != opposite_color:
            return None
        
        while self.board[up][left].color == opposite_color and left > 0 and up > 0:
                
            left -= 1
            up -= 1
            if self.board[up][left] == 0:
                return (up, left)
        
        return None
                

    def check_right_up(self, tile, opposite_color):
        right = tile.column + 1
        up = tile.row - 1

        if right > COLUMNS - 1 or up < 0:
            return None

        if self.board[up][right] == 0:
            return None
        if self.board[up][right].color != opposite_color:
            return None
       
        while self.board[up][right].color == opposite_color and right < COLUMNS-1 and up > 0:
                
            right += 1
            up -= 1
            if self.board[up][right] == 0:
                return (up, right)
            
        return None
                

    def check_left_down(self, tile, opposite_color):
        left = tile.column - 1
        down = tile.row + 1

        if left < 0 or down > ROWS - 1:
            return None

        if self.board[down][left] == 0:
            return None
        if self.board[down][left].color != opposite_color:
            return None

        
        while self.board[down][left].color == opposite_color and left > 0 and down < ROWS-1:
                
            left -= 1
            down += 1
            if self.board[down][left] == 0:
                return (down, left)
            
        return None
                

    def check_right_down(self, tile, opposite_color):
        right = tile.column + 1
        down = tile.row + 1

        if right > COLUMNS - 1 or down > ROWS - 1:
            return None

        if self.board[down][right] == 0:
            return None
        if self.board[down][right].color != opposite_color:
            return None
        
        while self.board[down][right].color == opposite_color and right < COLUMNS-1 and down < ROWS-1:
                
            right += 1
            down += 1
            if self.board[down][right] == 0:
                return (down, right)
        
        return None
                
    
    def find_moves(self, tile, opposite_color):
        possible_moves = []
        if (up := self.check_up(tile, opposite_color)) and tile.row != 0:
            possible_moves.append(up)

        if (down := self.check_down(tile, opposite_color)) and tile.row != ROWS - 1:
            possible_moves.append(down)

        if (left := self.check_left(tile, opposite_color)) and tile.column != 0:
            possible_moves.append(left)

        if (right := self.check_right(tile, opposite_color)) and tile.column != COLUMNS - 1:
            possible_moves.append(right)

        if (left_up := self.check_left_up(tile, opposite_color)) and tile.row != 0 and tile.column != 0:
            possible_moves.append(left_up)

        if (right_up := self.check_right_up(tile, opposite_color)) and tile.row != 0 and tile.column != COLUMNS - 1:
            possible_moves.append(right_up)

        if (left_down := self.check_left_down(tile, opposite_color)) and tile.row != ROWS - 1 and tile.column !=0:
            possible_moves.append(left_down)

        if (right_down := self.check_right_down(tile, opposite_color)) and tile.row != ROWS - 1 and tile.column != COLUMNS - 1:
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
        
        return valid_moves

    def print_moves(self, valid_moves, screen):

        for (row, col) in valid_moves:
           
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2

            radius = SQUARE_SIZE//2 - 30

            pygame.draw.circle(screen, YELLOW, (x, y), radius)
            
            
    def make_move(self, row, col):
        if self.blacks_turn:
            # Replace the tile at (row, col) with a new black tile
            self.board[row][col] = Tile(row, col, BLACK)
            self.print_board()
            self.flip_tiles(row, col)
            self.blacks_turn = False
        else:
            # Replace the tile at (row, col) with a new white tile
            self.board[row][col] = Tile(row, col, WHITE)
            self.flip_tiles(row, col)
            self.print_board()
            self.blacks_turn = True

    def flip_tiles(self, row, col):
        
        if row != 0 and hasattr(self.board[row - 1][col], 'color'):
            self.flip_up(row, col)

        if row != ROWS - 1 and hasattr(self.board[row + 1][col], 'color'):
            self.flip_down(row, col)

        if col != 0 and hasattr(self.board[row][col - 1], 'color'):
            self.flip_left(row, col)

        if col != COLUMNS - 1 and hasattr(self.board[row][col + 1], 'color'):
            self.flip_right(row, col)

    def flip_up(self, row, col):
        tiles_to_flip = []
        up = row - 1
        
        while self.board[up][col].color != self.board[row][col].color:
            tiles_to_flip.append(self.board[up][col])
            #print(tiles_to_flip[0].color)
            up -= 1
            if(self.board[up][col] == 0):
                break
            
            if self.board[up][col].color == self.board[row][col].color:
                for tile in tiles_to_flip:
                    tile.color = self.board[row][col].color

    def flip_down(self, row, col):
        tiles_to_flip = []
        down = row + 1
        
        while self.board[down][col].color != self.board[row][col].color:
            tiles_to_flip.append(self.board[down][col])
            #print(tiles_to_flip[0].color)
            down += 1
            if(self.board[down][col] == 0):
                break
            
            if self.board[down][col].color == self.board[row][col].color:
                for tile in tiles_to_flip:
                    tile.color = self.board[row][col].color

    def flip_left(self, row, col):
        tiles_to_flip = []
        left = col - 1
        
        while self.board[row][left].color != self.board[row][col].color:
            tiles_to_flip.append(self.board[row][left])
            #print(tiles_to_flip[0].color)
            left -= 1
            if(self.board[row][left] == 0):
                break
            
            if self.board[row][left].color == self.board[row][col].color:
                for tile in tiles_to_flip:
                    tile.color = self.board[row][col].color

    def flip_right(self, row, col):
        tiles_to_flip = []
        right = col + 1
        
        while self.board[row][right].color != self.board[row][col].color:
            tiles_to_flip.append(self.board[row][right])
            #print(tiles_to_flip[0].color)
            right += 1
            if(self.board[row][right] == 0):
                break
            
            if self.board[row][right].color == self.board[row][col].color:
                for tile in tiles_to_flip:
                    tile.color = self.board[row][col].color

    def print_board(self):
    
        for row in self.board:
            row_str = ""
            for tile in row:
                if tile == 0:  # Empty space
                    row_str += "0 "  # Print '0' for empty space
                else:
                    row_str += f"{tile.color} "  # Print the color of the tile
            print(row_str)  # Strip any trailing space for clean output
                
        print()


        
            

            
                        


