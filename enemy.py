
import pygame
import os
import math
from gameWall import walls
from pathfind import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites):
        super().__init__()
        self.x = x
        self.y = y
        self.HEIGHT = 25
        self.WIDTH = 25
        self.IMAGE_WIDTH = 50
        self.IMAGE_HEIGHT = 50
        self.rot = 0
        self.health = 100
        self.sprites = sprites
        self.currentimage = 0

        self.originalImage = pygame.transform.scale(
        self.sprites[self.currentimage%len(self.sprites)], (self.WIDTH, self.HEIGHT)
        )
        
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
       
        rot = 0
        self.rect.center = (self.x, self.y)
        if self.prev != None:
            rot = math.atan2((self.y - self.prev[1]),
                             (self.x - self.prev[0]))*180/math.pi * -1
        self.currentimage += 1
            # rot = math.atan(
            #     (self.prev[1] - self.y) / (self.prev[0] - self.x)) if (self.x - self.prev[0]) != 0 else 0
           
        self.originalImage = self.sprites[ self.currentimage%len(self.sprites) ]
        self.image =pygame.transform.rotate(
            self.originalImage, rot)
        self.prev = self.x, self.y



    def visible(self, player):
        path = []
        x= self.x
        y = self.y
        rot = math.atan((self.y - player.y) / (self.x - player.y))*180/math.pi
        m = (player.y-self.y)/(player.x-self.x)
        while (abs(x - player.x) > 50 or abs(y - player.y) > 50) and 0 < x < WIDTH and 0 < y < HEIGHT:
            path.append((x,y))
            x += VEL
            y = m*x - m*player.x + player.y

            for wall in walls:
                if wall.rect.colliderect(pygame.Rect(x,y, 50, 50)):
                    return []
  
        if (abs(x - player.x) < 50 and abs(y - player.y) < 50):
            return path


    def update(self, target, WIDTH, HEIGHT, SHOOTING_RADIUS, player, SEARCH_RADIUS):
        alternatepath = []
        
        if SHOOTING_RADIUS < math.sqrt((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2) < SEARCH_RADIUS:
            target = player.rect

        if target != None and (self.pathlen < len(self.path)//2 or len(self.path) <= 1) and math.sqrt((self.rect.centerx - target.centerx) ** 2 + (self.rect.centery - target.centery) ** 2) > SHOOTING_RADIUS:
            self.path = findPath(self.rect, target, WIDTH, HEIGHT)
            self.pathlen = len(self.path)
            # self.path = path_find(self, targe
            # t[0], target[1], WIDTH, HEIGHT)
            self.previous_target = target
        # else:
        

        # else:
        #     alternatepath = self.visible(player)
        #     if alternatepath:
        #         self.path = alternatepath

        if self.path and SHOOTING_RADIUS < math.sqrt((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2) :
            # curx, cury = self.path[-1]
            # tarx, tary = self.path[0]
            # if math.sqrt((curx - tarx) ** 2 + (cury - tary) ** 2) > SHOOTING_RADIUS//2:
            self.move()
        
        