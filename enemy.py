import pygame
import os
import math
from gameWall import walls
from pathfind import findPath


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.HEIGHT = 50
        self.WIDTH = 50
        self.rot = 0
        self.health = 100
        self.originalImage = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", "images", image)), (self.WIDTH, self.HEIGHT))
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.path = []

    def shoot(self):
        pass

    def to_radian(self, rot):
        return math.pi * 2 * rot / 360

    def move(self, destination, WIDTH, HEIGHT, VEL, prev):

        initialx, initialy = self.x, self.y
        self.x = destination[0]
        self.y = destination[1]
        self.rect.center = self.x, self.y
        # if keys_pressed[pygame.K_a]:
        angle = 0
        if self.path:
            point = self.path[0]
            angle = math.atan2((point[1]-self.rect.y),(point[0]-self.x))*180/math.pi * -1
    
        self.image = pygame.transform.rotate(self.image, angle)
        
        # if keys_pressed[pygame.K_d]:
        #     self.rot = (self.rot - 5) % 360

        # if keys_pressed[pygame.K_w]:
        #     self.x += (VEL * math.cos(self.to_radian(self.rot))) if 0 < (self.x +
        #                                                                  VEL * math.cos(self.to_radian(self.rot))) < WIDTH else 0
        #     self.y -= (VEL * math.sin(self.to_radian(self.rot))) if 0 < (self.y -
        #                                                                  VEL * math.sin(self.to_radian(self.rot))) < WIDTH else 0

        # if keys_pressed[pygame.K_s]:
        #     self.x -= (VEL * math.cos(self.to_radian(self.rot))) if 0 < (self.x -
        #                                                                  VEL * math.cos(self.to_radian(self.rot))) < WIDTH else 0
        #     self.y += (VEL * math.sin(self.to_radian(self.rot))) if 0 < (self.y +
        #                                                                  VEL * math.sin(self.to_radian(self.rot))) < WIDTH else 0
        

    def update(self, target, WIDTH, HEIGHT, VEL):
        prev = self.rot
        self.image = pygame.transform.rotate(
            self.originalImage, self.rot)


        
        if target:
            self.path= findPath(self.rect, target.rect)
            # print("i have got a new target: ", target)
            # print("obv i should get a path: ", self.path)
            if self.path == []:
                for i in walls:
                    
                    if i.rect.colliderect(self.rect):
                        iscollide = True
                        print(iscollide)
                        break
        if self.path:
            
            self.move(self.path.pop(), WIDTH, HEIGHT, 5, prev)
