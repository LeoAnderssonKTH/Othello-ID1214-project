import pygame
from othello.globals import SCREEN_HEIGHT, SCREEN_WIDTH


class Othello:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Othello')

        self.RUN = True

    def run(game):
        while game.RUN == True:
            game.input()
            game.update()
            game.print()

    def input(game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.RUN = False

    def update(game):
        pass

    def print(game):
        game.screen.fill((0, 0, 0))

        pygame.display.update()
