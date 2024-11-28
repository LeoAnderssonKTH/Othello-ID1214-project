import pygame
from .globals import BLACK, WHITE, ROWS, COLUMNS, SQUARE_SIZE,GREEN
from .tile import Tile

class Board:
    def __init__(self):
        self.board = []
        self.white_tiles = 2
        self.black_tiles = 2
        self.starting_board()
    
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
