import pygame
from othello.globals import SCREEN_WIDTH, SCREEN_HEIGHT

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Othello')

FPS = 60

def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
    
    pygame.quit()  # This should be aligned with the `while run:` block

main()
