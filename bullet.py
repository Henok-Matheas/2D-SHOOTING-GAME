import math
import pygame


class Bullet:
    def __init__(self, x, y, rot, BULLET_VEL, BULLET_WIDTH, BULLET_HEIGHT):
        self.x = x
        self.y = y
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.rot = rot
        self.BULLET_VEL = BULLET_VEL
        self.rect = pygame.Rect(
            self.x + self.width, self.y + (self.height / 2) - BULLET_HEIGHT / 2, BULLET_WIDTH, BULLET_HEIGHT)

    def update(self, WIDTH, HEIGHT):
        self.x += (self.BULLET_VEL * math.cos(self.to_radian()))
        self.y -= (self.BULLET_VEL * math.sin(self.to_radian()))
        self.rect.x = self.x
        self.rect.y = self.y

    def to_radian(self):
        return math.pi * 2 * self.rot / 360
