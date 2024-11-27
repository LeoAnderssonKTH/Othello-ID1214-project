import pygame
import random
import copy

class Othello:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(1200, 1200)
        pygame.display.set_caption('Othello')

        self.RUN = True

def run(game):
    while game.RUN == True:
        game.input()
        game.update()

def input(game):
    pass

def update(game):
    pass

def print(game):
    pass