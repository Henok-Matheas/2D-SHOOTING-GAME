import pygame

WIDTH, HEIGHT = 900, 500


class Wall(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, color):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.rect.topleft = [x, y]


WHITE = (255, 255, 255)
WALL_THICKNESS = 20


wall = Wall(WIDTH//2, WALL_THICKNESS, 0, HEIGHT//2, (255, 255, 255))
wall2 = Wall(WALL_THICKNESS, HEIGHT//4, wall.rect.width-20, wall.rect.y, WHITE)

wall4 = Wall(WALL_THICKNESS, HEIGHT//5, WIDTH//6, 0, WHITE)

wall3 = Wall(WIDTH//5, WALL_THICKNESS,  WALL_THICKNESS *
             3, wall4.rect.height, WHITE)

wall5 = Wall(WALL_THICKNESS, HEIGHT//4, WIDTH//2.5, WALL_THICKNESS*3, WHITE)

wall6 = Wall(WALL_THICKNESS, HEIGHT//4, WIDTH//1.75, 0, WHITE)
wall7 = Wall(WIDTH//3, WALL_THICKNESS, wall6.rect.x, wall6.rect.height, WHITE)

wall8 = Wall(WALL_THICKNESS, HEIGHT//3, WIDTH//1.25, HEIGHT//2, WHITE)
wall9 = Wall(WIDTH-wall8.rect.x, WALL_THICKNESS,
             wall8.rect.x, HEIGHT//1.5, WHITE)

walls = pygame.sprite.Group()

walls.add(wall)
walls.add(wall2)
walls.add(wall3)
walls.add(wall4)
walls.add(wall5)
walls.add(wall6)
walls.add(wall7)
walls.add(wall8)
walls.add(wall9)
