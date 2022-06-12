from user import User
import os
import pygame


WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")
pygame.font.init()
pygame.mixer.init()

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 40)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
FPS = 60
VEL = 1

ANGLE = 90
BULLET_VEL = 7
MAX_BULLETS = 5
BULLET_WIDTH, BULLET_HEIGHT = 5, 5
DAMAGE = 5


USER_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 2

# BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(
#     "Assets", "Grenade+1.mp3"))
# BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(
#     "Assets", "Gun+Silencer.mp3"))


def draw(user_group, keys_pressed):
    WINDOW.fill((0, 0, 0))
    user_group.draw(WINDOW)
    user_group.update(keys_pressed, WIDTH, HEIGHT, VEL)
    pygame.display.update()


# pygame.mouse.set_visible = False


def main():
    user = User(100, 100, "survivor-idle_rifle_0.png")
    user_group = pygame.sprite.Group()
    user_group.add(user)
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.pygame.MOUSEBUTTONDOWN:
                pass

        keys_pressed = pygame.key.get_pressed()
        draw(user_group, keys_pressed)


if __name__ == "__main__":
    main()