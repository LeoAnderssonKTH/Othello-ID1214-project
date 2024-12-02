import pygame
from .globals import BLACK, WHITE, SQUARE_SIZE, GRAY

class Tile:
    PADDING = 10
    OUTLINE = 2

    def __init__(self, row, column, color):
        self.color = color
        self.column = column
        self.row = row
        self.x = 0
        self.y = 0
        self.find_pos()

    def find_pos(self):
        self.x = SQUARE_SIZE * self.column + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def flip_tiles(self):
        if self.color == BLACK:
            self.color = WHITE
        else:
            self.color = BLACK

    def draw_tile(self, screen):
        # Size of tile
        radius = SQUARE_SIZE//2 - self.PADDING
        # Outline/Boarder of the tile
        pygame.draw.circle(screen, GRAY, (self.x, self.y), radius + self.OUTLINE)
        # The tile
        pygame.draw.circle(screen, self.color, (self.x, self.y), radius)

    def __repr__(self):
        return self.color          