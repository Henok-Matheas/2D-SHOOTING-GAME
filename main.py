import os
import pygame
from pyparsing import col
from gameWalls import walls

WHITE = (255,255,255)
WIDTH, HEIGHT = 900, 500
WALL_THICKNESS = 20
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nigga")




def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        pygame.display.flip()
        walls.draw(WINDOW)

if __name__ == "__main__":
    main()
    

