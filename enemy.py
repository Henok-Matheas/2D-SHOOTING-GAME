
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

        self.path = []
        self.prev = None
        self.previous_target = None

        self.pathlen = 0

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
        rot = 0
        self.rect.center = (self.x, self.y)
        if self.prev != None:
            rot = math.atan2((self.y - self.prev[1]),
                             (self.x - self.prev[0]))*180/math.pi * -1
        self.currentimage += 1
            # rot = math.atan(
            #     (self.prev[1] - self.y) / (self.prev[0] - self.x)) if (self.x - self.prev[0]) != 0 else 0
            # print("the roatation", rot)
        self.originalImage = self.sprites[self.currentimage%len(self.sprites)]
        self.image =pygame.transform.rotate(
            self.originalImage, rot)
        self.prev = self.x, self.y

    def update(self, target, WIDTH, HEIGHT, SHOOTING_RADIUS):
        if target != None and (self.pathlen < len(self.path)//2 or len(self.path) <= 1) and math.sqrt((self.rect.centerx - target.centerx) ** 2 + (self.rect.centery - target.centery) ** 2) > SHOOTING_RADIUS:
            self.path = findPath(self.rect, target, WIDTH, HEIGHT)
            self.pathlen = len(self.path)
            # self.path = path_find(self, target[0], target[1], WIDTH, HEIGHT)
            self.previous_target = target
        if self.path :
            # curx, cury = self.path[-1]
            # tarx, tary = self.path[0]
            # if math.sqrt((curx - tarx) ** 2 + (cury - tary) ** 2) > SHOOTING_RADIUS//2:
            self.move()