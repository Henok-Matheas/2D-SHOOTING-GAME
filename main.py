import os
import pygame
from pyparsing import col

class Wall(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
        self.rect.topleft = [x,y]



WHITE = (255,255,255)
WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nigga")

wall = Wall(600, 50, 0, 200, (255,255,255))
wall2 = Wall(50, 200, wall.rect.width-50, wall.rect.y, WHITE)
walls = pygame.sprite.Group()
walls.add(wall)
walls.add(wall2)




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
    

