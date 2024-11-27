import pygame
from .globals import BLACK, WHITE, ROWS, COLUMNS, SQUARE_SIZE,GREEN

class Board:
    def __init__(self):
        self.board = []
    
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
        
        
