import os
from random import randint
import pygame

WIDTH, HEIGHT = 900, 500


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "images", "wall.png")), (50,50))
       
        self.rect = self.image.get_rect()

        self.rect.topleft = [x, y]




walls = pygame.sprite.Group()

while len(walls) < 20:
    x,y = randint(0,WIDTH), randint(0,HEIGHT)
    overlap = False
    for wall in walls:
        if wall.rect.colliderect(Wall(x, y).rect):
            overlap = True
            break
    if not overlap:
        walls.add(Wall(x, y))

