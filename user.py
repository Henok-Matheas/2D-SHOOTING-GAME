import pygame
import os
import math


class User(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.HEIGHT = 50
        self.WIDTH = 50
        self.rot = 0
        self.originalImage = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", image)), (self.WIDTH, self.HEIGHT))
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def move(self, keys_pressed, WIDTH, HEIGHT, VEL, prev):
        if keys_pressed[pygame.K_d]:
            self.rot = (self.rot + 5) % 360

        if keys_pressed[pygame.K_a]:
            self.rot = (self.rot - 5) % 360

        if keys_pressed[pygame.K_w]:
            self.x += (VEL * math.cos(math.pi * 2 * self.rot / 360))
            self.y -= (VEL * math.sin(math.pi * 2 * self.rot / 360))

        if keys_pressed[pygame.K_s]:
            self.x -= (VEL * math.cos(math.pi * 2 * self.rot / 360))
            self.y += (VEL * math.sin(math.pi * 2 * self.rot / 360))

    def update(self, keys_pressed, WIDTH, HEIGHT, VEL):
        prev = self.rot
        self.image = pygame.transform.rotate(
            self.originalImage, self.rot)
        self.move(keys_pressed, WIDTH, HEIGHT, VEL, prev)
        self.rect.center = (self.x, self.y)
