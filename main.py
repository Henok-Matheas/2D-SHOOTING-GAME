import asyncio
import math

import random
from user import User
from gameWall import walls
import os
import pygame
from bullet import Bullet
from enemy import Enemy

from character_menu import char_menu


USER_IMAGE = char_menu()
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
FPS = 60
VEL = 3

ANGLE = 90
BULLET_VEL = 7
MAX_BULLETS = 5
ENEMY_MAX_BULLETS = 1
BULLET_WIDTH, BULLET_HEIGHT = 10, 10
DAMAGE = 2
SHOOTING_RADIUS = 150

MAX_HEALTH = 100
MISS_RANGE = 10
USER_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 2

USER_DEAD = pygame.USEREVENT + 3
ENEMY_DEAD = pygame.USEREVENT + 4
SEARCH_RADIUS = 350
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
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "images", "bg2.png")), (WIDTH*2, HEIGHT*2))


def handle_bullets(user_bullets, enemy_bullets, user_group, enemy_group):
    for bullet in user_bullets:
        bullet.update(WIDTH, HEIGHT)

        for enemy in enemy_group:
            if enemy.rect.colliderect(bullet):
                pygame.event.post(pygame.event.Event(ENEMY_HIT))
                enemy.health -= 10
                BULLET_HIT_SOUND.play()
                ENEMY_HIT_SOUND.play()
                user_bullets.remove(bullet)
                break

            if enemy.health <= 0:
                ENEMY_DEAD_SOUND.play()
                enemy_group.remove(enemy)

        if 0 >= bullet.x or bullet.x >= WIDTH or 0 >= bullet.y or bullet.y >= HEIGHT and bullet in user_bullets:
            user_bullets.remove(bullet)
            continue

        for wall in walls:
            if bullet.rect.colliderect(wall) and bullet in user_bullets:
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

            if user.health <= 0:
                USER_DEAD_SOUND.play()
                user_group.remove(user)
                return

        if bullet in enemy_bullets and 0 >= bullet.x or bullet.x >= WIDTH or 0 >= bullet.y or bullet.y >= HEIGHT:
            enemy_bullets.remove(bullet)
            continue

        for wall in walls:
            if bullet in enemy_bullets and bullet.rect.colliderect(wall):
                enemy_bullets.remove(bullet)
                break


def draw(user_group, enemy_group, keys_pressed, user_bullets, enemy_bullets, target):
    WINDOW.blit(BACKGROUND, (0,0))
    walls.draw(WINDOW)
    user_group.draw(WINDOW)
    enemy_group.draw(WINDOW)
    user_group.update(keys_pressed, WIDTH, HEIGHT, VEL)
    # enemy_group.update(target, WIDTH, HEIGHT)

    for user in user_group:
        targt = user.rect if target else None
        enemy_group.update(targt, WIDTH, HEIGHT, SHOOTING_RADIUS, user, SEARCH_RADIUS)

    user_health_text = ""
    for user in user_group:
    
        x,y = user.rect.center
        pygame.draw.rect(WINDOW, YELLOW, pygame.Rect(x,y +30, 0.5* user.health*100/MAX_HEALTH, 10)) 
    for enemy in enemy_group:
        x,y = enemy.rect.center
        pygame.draw.rect(WINDOW, RED, pygame.Rect(x,y +30, 0.5* enemy.health*100/MAX_HEALTH, 10))

    
    for bullet in user_bullets:
        WINDOW.blit(bullet.image, (bullet.x, bullet.y))
        
    for bullet in enemy_bullets:
        WINDOW.blit(bullet.image, (bullet.x, bullet.y))
    pygame.display.update()


# pygame.mouse.set_visible = False
async def loadBullets(enemy,rot, enemy_bullets ):
    enemy_bullets.append(Bullet(enemy.rect.centerx, enemy.rect.centery, rot + random.uniform(0, MISS_RANGE), BULLET_VEL, BULLET_WIDTH, BULLET_HEIGHT))

def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, YELLOW)
    WINDOW.blit(winner_text, ((WIDTH // 2) -
                winner_text.get_width() // 2, HEIGHT // 2))

    pygame.display.update()
    pygame.time.delay(6000)
    pygame.quit()
def to_radian( rot):
        return math.pi * 2 * rot / 360

def main():
  
    user_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    sprites1 = []
       
    sprites1.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 3","walk",  "enemy3walk1.png")), 90))
    sprites1.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 3","walk",  "enemy3walk1.png")), 90))
    sprites1.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 3","walk",  "enemy3walk2.png")), 90))
    
    sprites1.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 3","walk",  "enemy3walk2.png")), 90))
    sprites1.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 3","walk",  "enemy3walk3.png")), 90))
   
    sprites1.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 3","walk",  "enemy3walk3.png")), 90))
    sprites1.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 3","walk",  "enemy3walk4.png")), 90))
    sprites1.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 3","walk",  "enemy3walk4.png")), 90))
  
    sprites2 = []    
        
    sprites2.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 1","walk",  "enemy1walk1.png")), 90))
    sprites2.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 1","walk",  "enemy1walk1.png")), 90))
    sprites2.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 1","walk",  "enemy1walk2.png")), 90))
    sprites2.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 1","walk",  "enemy1walk2.png")), 90))
    sprites2.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 1","walk",  "enemy1walk3.png")), 90))
    sprites2.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 1","walk",  "enemy1walk3.png")), 90))
    sprites2.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 1","walk",  "enemy1walk4.png")), 90))
    sprites2.append(pygame.transform.rotate(pygame.image.load(os.path.join("Assets", "images", "enemy 1","walk",  "enemy1walk4.png")), 90))

    usersprites = sprites1 if USER_IMAGE == 1 else sprites2
    enemysprites = sprites2 if USER_IMAGE == 1 else sprites1
    user = User(0, 0, usersprites)

    enemies = [Enemy(750, 10, enemysprites), Enemy(750, 10, enemysprites), Enemy(750, 10, enemysprites)]
    
    user_bullets = []
    enemy_bullets = []
    enemy_group.add(enemies.pop())
    user_group.add(user)
    target = None

    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(user_bullets) < MAX_BULLETS:
                    for user in user_group:
                        x,y = user.rect.center
                        user_bullets.append(
                            Bullet(x, y-7, user.rot, BULLET_VEL, BULLET_WIDTH, BULLET_HEIGHT))
                    BULLET_FIRE_SOUND.play()
                    target = user.rect.centerx, user.rect.centery

        # clock.tick(30)
        for user in user_group:
            for enemy in enemy_group:
                if math.sqrt((enemy.rect.centerx - user.rect.centerx) ** 2 + (enemy.rect.centery - user.rect.centery) ** 2) <= SHOOTING_RADIUS and len(enemy_bullets) < ENEMY_MAX_BULLETS:
                    # rot = math.awwwentery - user.rect.centery) / (enemy.rect.centerx - user.rect.centerx)) if (enemy.rect.centerx - user.rect.centerx) != 0 else 0
                    rot = math.atan2(
                        (user.rect.centery - enemy.rect.centery), (user.rect.centerx - enemy.rect.centerx))*180/math.pi * -1
                    # enemy_bullets.apcentery - enemy.rect.centery), (user.rect.centerx - enemy.rect.centerx))*180/math.pi * -1
                    asyncio.run(loadBullets(enemy, rot, enemy_bullets))
                   
                    enemy.image = pygame.transform.rotate(
                        enemy.originalImage, rot)
                    BULLET_FIRE_SOUND.play()

        if len(user_group) < 1:
            draw_winner("ENEMIES HAVE WON")

        if len(enemy_group) < 1:
            if enemies:
                enemy_group.add(enemies.pop())
            else:
                draw_winner("You HAVE WON!")
  
        keys_pressed = pygame.key.get_pressed()

        handle_bullets(user_bullets, enemy_bullets, user_group, enemy_group)
        draw(user_group, enemy_group, keys_pressed,
             user_bullets, enemy_bullets, target)
        target = None


if __name__ == "__main__":
    main() 