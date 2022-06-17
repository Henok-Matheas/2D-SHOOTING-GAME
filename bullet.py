import math
import os
import pygame


class Bullet:
    def __init__(self, x, y, rot, BULLET_VEL, BULLET_WIDTH, BULLET_HEIGHT):
        self.x = x
        self.y = y
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT

        self.rot = rot
        self.BULLET_VEL = BULLET_VEL
        self.originalImage = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "images", "bullet.png")), (self.width, self.height))
        self.image = self.originalImage
        self.image = pygame.transform.scale(
            self.originalImage, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self, WIDTH, HEIGHT):
        self.x += (self.BULLET_VEL * math.cos(self.to_radian()))
        self.y -= (self.BULLET_VEL * math.sin(self.to_radian()))
        self.rect.x = self.x
        self.rect.y = self.y
        self.image =pygame.transform.rotate(
            self.originalImage, self.rot)

    def to_radian(self):
        return math.pi * 2 * self.rot / 360
