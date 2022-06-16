import math
from user import User
from gameWall import walls
import os
import pygame
from bullet import Bullet
from enemy import Enemy


WIDTH, HEIGHT = 900, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game")
pygame.font.init()
pygame.mixer.init()

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 40)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
FPS = 120
VEL = 5

ANGLE = 90
BULLET_VEL = 7
MAX_BULLETS = 5
ENEMY_MAX_BULLETS = 1
BULLET_WIDTH, BULLET_HEIGHT = 5, 5
DAMAGE = 5
SHOOTING_RADIUS = 150


USER_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 2

USER_DEAD = pygame.USEREVENT + 3
ENEMY_DEAD = pygame.USEREVENT + 4

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(
    "Assets", "sounds", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(
    "Assets", "sounds", "Gun+Silencer.mp3"))

USER_HIT_SOUND = pygame.mixer.Sound(os.path.join(
    "Assets", "sounds", "3grunt4.wav"))

USER_DEAD_SOUND = pygame.mixer.Sound(os.path.join(
    "Assets", "sounds", "yell12.wav"))

ENEMY_HIT_SOUND = pygame.mixer.Sound(os.path.join(
    "Assets", "sounds", "3grunt4.wav"))

ENEMY_DEAD_SOUND = pygame.mixer.Sound(os.path.join(
    "Assets", "sounds", "yell12.wav"))

WALKING_SOUND = pygame.mixer.Sound(os.path.join(
    "Assets", "sounds", "Grenade+1.mp3"))


def handle_bullets(user_bullets, enemy_bullets, user_group, enemy_group):
    for bullet in user_bullets:
        bullet.update(WIDTH, HEIGHT)

        for enemy in enemy_group:
            if enemy.rect.colliderect(bullet):
                pygame.event.post(pygame.event.Event(ENEMY_HIT))
                enemy.health -= DAMAGE
                BULLET_HIT_SOUND.play()
                ENEMY_HIT_SOUND.play()
                user_bullets.remove(bullet)
                break

            if enemy.health <= 0:
                ENEMY_DEAD_SOUND.play()
                enemy_group.remove(enemy)

        if 0 >= bullet.x or bullet.x >= WIDTH or 0 >= bullet.y or bullet.y >= HEIGHT:
            user_bullets.remove(bullet)
            continue

        for wall in walls:
            if bullet.rect.colliderect(wall):
                user_bullets.remove(bullet)
                break

    for bullet in enemy_bullets:
        bullet.update(WIDTH, HEIGHT)

        for user in user_group:
            if user.rect.colliderect(bullet):
                pygame.event.post(pygame.event.Event(USER_HIT))
                user.health -= DAMAGE
                BULLET_HIT_SOUND.play()
                USER_HIT_SOUND.play()
                enemy_bullets.remove(bullet)
                break

            if user.health <= 0:
                USER_DEAD_SOUND.play()
                user_group.remove(user)

        if 0 >= bullet.x or bullet.x >= WIDTH or 0 >= bullet.y or bullet.y >= HEIGHT:
            enemy_bullets.remove(bullet)
            continue

        for wall in walls:
            if bullet.rect.colliderect(wall):
                enemy_bullets.remove(bullet)
                break


def draw(user_group, enemy_group, keys_pressed, user_bullets, enemy_bullets, target):
    WINDOW.fill((0, 0, 0))
    walls.draw(WINDOW)
    user_group.draw(WINDOW)
    enemy_group.draw(WINDOW)
    user_group.update(keys_pressed, WIDTH, HEIGHT, VEL)
    enemy_group.update(target, WIDTH, HEIGHT)

    user_health_text = ""
    for user in user_group:
        user_health_text = HEALTH_FONT.render(
            "HEALTH: " + str(user.health), 1, WHITE)

    WINDOW.blit(user_health_text, (0,
                HEIGHT - user_health_text.get_height()))

    for bullet in user_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet.rect)
    for bullet in enemy_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet.rect)
    pygame.display.update()


# pygame.mouse.set_visible = False


def main():
    user_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    user = User(50, 50, "survivor-idle_rifle_0.png")
    enemy1 = Enemy(600, 450, "survivor-idle_rifle_0.png")
    enemy2 = Enemy(450, 50, "survivor-idle_rifle_0.png")
    user_bullets = []
    enemy_bullets = []
    enemy_group.add(enemy1, enemy2)
    user_group.add(user)
    target = None

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
                    target = user.rect.centerx, user.rect.centery

        # clock.tick(24)w
        for user in user_group:
            for enemy in enemy_group:
                if math.sqrt((enemy.rect.x - user.rect.x) ** 2 + (enemy.rect.y - user.rect.y) ** 2) <= SHOOTING_RADIUS and len(enemy_bullets) < ENEMY_MAX_BULLETS:
                    rot = math.atan(
                        (enemy.rect.centery - user.rect.centery) / (enemy.rect.centerx - user.rect.centerx)) if (enemy.rect.centerx - user.rect.centerx) != 0 else 0
                    # rot = math.atan(
                    #     (enemy.rect.x - user.rect.x) / (enemy.rect.y - user.rect.y)) if (enemy.rect.y - user.rect.y) != 0 else 0
                    print("the rotation is", rot)
                    enemy_bullets.append(
                        Bullet(enemy.rect.centerx, enemy.rect.centery, math.pi * 2 * rot / 360, BULLET_VEL, BULLET_WIDTH, BULLET_HEIGHT))
                    BULLET_FIRE_SOUND.play()

        keys_pressed = pygame.key.get_pressed()

        handle_bullets(user_bullets, enemy_bullets, user_group, enemy_group)
        draw(user_group, enemy_group, keys_pressed,
             user_bullets, enemy_bullets, target)
        target = None


if __name__ == "__main__":
    main()
