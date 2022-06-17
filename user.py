import pygame
import os
import math
from gameWall import walls


ROTATION_VEL = 3


class User(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.HEIGHT = 25
        self.WIDTH = 25
        self.IMAGE_WIDTH = 40
        self.IMAGE_HEIGHT = 40
        self.rot = 0
        self.health = 10000
       
        self.sprites = []
       
        self.sprites.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 3","walk",  "enemy3walk1.png")), 90))
        self.sprites.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 3","walk",  "enemy3walk2.png")), 90))
        self.sprites.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 3","walk",  "enemy3walk3.png")), 90))
        self.sprites.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 3","walk",  "enemy3walk4.png")), 90))

        self.currentimage = 0

        self.originalImage = pygame.transform.scale(
        self.sprites[self.currentimage%len(self.sprites)], (self.WIDTH, self.HEIGHT))
        self.image = pygame.transform.scale(
            self.originalImage, (self.IMAGE_WIDTH, self.IMAGE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def shoot(self):
        pass

    def to_radian(self, rot):
        return math.pi * 2 * rot / 360

    def move(self, keys_pressed, WIDTH, HEIGHT, VEL, prev):

        initialx, initialy = self.x, self.y

        if keys_pressed[pygame.K_a]:
            self.rot = (self.rot + ROTATION_VEL) % 360

        if keys_pressed[pygame.K_d]:
            self.rot = (self.rot - ROTATION_VEL) % 360

        if keys_pressed[pygame.K_w]:
            self.currentimage += 1
            self.x += (VEL * math.cos(self.to_radian(self.rot))) if 0 < (self.x +
                                                                         VEL * math.cos(self.to_radian(self.rot))) < WIDTH else 0
            self.y -= (VEL * math.sin(self.to_radian(self.rot))) if 0 < (self.y -
                                                                         VEL * math.sin(self.to_radian(self.rot))) < WIDTH else 0

        if keys_pressed[pygame.K_s]:
            self.currentimage -= 1
            self.x -= (VEL * math.cos(self.to_radian(self.rot))) if 0 < (self.x -
                                                                         VEL * math.cos(self.to_radian(self.rot))) < WIDTH else 0
            self.y += (VEL * math.sin(self.to_radian(self.rot))) if 0 < (self.y +
                                                                         VEL * math.sin(self.to_radian(self.rot))) < WIDTH else 0
        self.rect.center = (self.x, self.y)

        for wall in walls:
            if self.rect.colliderect(wall):
                self.x, self.y = initialx, initialy

    def update(self, keys_pressed, WIDTH, HEIGHT, VEL):
        prev = self.rot
        
        self.originalImage = self.sprites[self.currentimage%len(self.sprites)]
        self.image = pygame.transform.rotate(
                self.originalImage, self.rot)
        self.move(keys_pressed, WIDTH, HEIGHT, VEL, prev)