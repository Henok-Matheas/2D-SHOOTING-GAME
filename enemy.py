import pygame
import os
import math
from gameWall import walls
from pathfind import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.HEIGHT = 25
        self.WIDTH = 25
        self.IMAGE_WIDTH = 50
        self.IMAGE_HEIGHT = 50
        self.rot = 0
        self.health = 100
        self.originalImage = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "images", image)), (self.WIDTH, self.HEIGHT))
        self.image = self.originalImage
        self.image = pygame.transform.scale(
            self.originalImage, (self.IMAGE_WIDTH, self.IMAGE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.path = []
        self.prev = None

    def shoot(self):
        pass

    def to_radian(self, rot):
        return math.pi * 2 * rot / 360

    # def move(self, step, WIDTH, HEIGHT, VEL):
    #     initialx, initialy = self.x, self.y
    #     self.x, self.y = step
    #     self.rect.center = (self.x, self.y)
    #     for wall in walls:
    #         if self.rect.colliderect(wall):
    #             self.x, self.y = initialx, initialy

    def find_rot(self, user):
        self.rot = math.atan((self.y - user.y) / (self.x - user.y))

    def move(self):

        self.x, self.y = self.path.pop()
        # print("the pervious is ", self.prev, " the next is ", self.x, self.y)
        self.rect.center = (self.x, self.y)
        if self.prev != None:
            rot = math.atan(
                (self.prev[1] - self.y) / (self.prev[0] - self.x)) if (self.x - self.prev[0]) != 0 else 0
            print("the roatation", rot)
            self.image = pygame.transform.scale(
                pygame.transform.rotate(self.originalImage, rot), (self.IMAGE_WIDTH, self.IMAGE_HEIGHT))
        self.prev = self.x, self.y

    def update(self, target, WIDTH, HEIGHT):
        if target != None:
            self.path = path_find(self, target[0], target[1], WIDTH, HEIGHT)
        if self.path:
            self.move()
