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
        self.originalImage = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets", image)), (self.WIDTH, self.HEIGHT))
        self.image = self.originalImage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def degree(self):
        x2, y2 = pygame.mouse.get_pos()
        hypotenuse = math.sqrt(
            ((x2 - self.x) ** 2) + ((y2 - self.y) ** 2))
        ecs = (x2 - self.x)

        theta = math.atan((y2 - self.y) // (x2 - self.x)
                          ) if self.x != x2 else 0

        return theta * 360 / (2 * math.pi)

    def move(self, keys_pressed, WIDTH, HEIGHT, VEL):
        degree = self.degree()

        self.x += int(VEL * math.cos(degree))
        self.y += int(VEL * math.sin(degree))

        # if keys_pressed[pygame.K_d]:
        #     self.x += VEL if (self.x + VEL +
        #                       self.WIDTH) < WIDTH else 0
        # if keys_pressed[pygame.K_a]:
        #     self.x -= VEL if (self.x - VEL) > 0 else 0
        # if keys_pressed[pygame.K_w]:
        #     self.y -= VEL if (self.y - VEL) > 0 else 0
        # if keys_pressed[pygame.K_s]:
        #     self.y += VEL if (self.y + VEL +
        #                       self.HEIGHT) < HEIGHT else 0
        self.rect.center = (self.x, self.y)

    def update(self, keys_pressed, WIDTH, HEIGHT, VEL):
        self.move(keys_pressed, WIDTH, HEIGHT, VEL)
        self.image = pygame.transform.rotate(
            self.originalImage, -self.degree())
