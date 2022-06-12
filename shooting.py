from user import User
from gameWall import walls
import os
import pygame
from bullet import Bullet


WIDTH, HEIGHT = 900, 600
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

USER_DEAD = pygame.USEREVENT + 3
ENEMY_DEAD = pygame.USEREVENT + 4

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(
    "Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(
    "Assets", "Gun+Silencer.mp3"))


def handle_bullets(user_bullets, enemy_bullets, user_group, enemy_group):
    for bullet in user_bullets:
        bullet.update(WIDTH, HEIGHT)

        # for enemy in enemy_group:
        #     if enemy.colliderect(bullet):
        #         print("enemy has been shot")
        #         pygame.event.post(pygame.event.Event(ENEMY_HIT))
        #         user_bullets.remove(bullet)

        if 0 > bullet.x or bullet.x > WIDTH or 0 > bullet.y or bullet.y > HEIGHT:
            user_bullets.remove(bullet)

        for wall in walls:
            if bullet.rect.colliderect(wall):
                user_bullets.remove(bullet)

    # for bullet in enemy_bullets:
    #     if bullet == None:
    #         continue
    #     bullet.x -= BULLET_VEL

    #     if user.colliderect(bullet):
    #         print("user has been shot")
    #         pygame.event.post(pygame.event.Event(user_HIT))
    #         enemy_bullets.remove(bullet)
    #     elif bullet.x < 0:
    #         enemy_bullets.remove(bullet)


def draw(user_group, keys_pressed, user_bullets):
    WINDOW.fill((0, 0, 0))
    walls.draw(WINDOW)
    user_group.draw(WINDOW)
    user_group.update(keys_pressed, WIDTH, HEIGHT, VEL)

    user_health_text = ""
    for user in user_group:
        user_health_text = HEALTH_FONT.render(
            "HEALTH: " + str(user.health), 1, WHITE)

    WINDOW.blit(user_health_text, (0,
                HEIGHT - user_health_text.get_height()))

    for bullet in user_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet.rect)
    pygame.display.update()


# pygame.mouse.set_visible = False


def main():
    user = User(50, 50, "survivor-idle_rifle_0.png")
    user_bullets = []
    enemy_bullets = []
    user_group = pygame.sprite.Group()
    user_group.add(user)
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for user in user_group:
                        user_bullets.append(
                            Bullet(user.rect.centerx, user.rect.centery, user.rot, BULLET_VEL, BULLET_WIDTH, BULLET_HEIGHT))
                    BULLET_FIRE_SOUND.play()

        keys_pressed = pygame.key.get_pressed()
        handle_bullets(user_bullets, None, user_group, None)
        draw(user_group, keys_pressed, user_bullets)


if __name__ == "__main__":
    main()
