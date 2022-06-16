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
FPS = 60
VEL = 1
PI = 22/7
ANGLE = 90
BULLET_VEL = 7
MAX_BULLETS = 5
BULLET_WIDTH, BULLET_HEIGHT = 5, 5
DAMAGE = 5


USER_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 2

USER_SHOOT =  pygame.USEREVENT + 5

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

            if enemy.health <= 0:
                ENEMY_DEAD_SOUND.play()
                enemy_group.remove(enemy)

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


def draw(user_group, enemy_group, keys_pressed, user_bullets, target):
    WINDOW.fill((0, 0, 0))
    walls.draw(WINDOW)
    user_group.draw(WINDOW)
    enemy_group.draw(WINDOW)
    user_group.update(keys_pressed, WIDTH, HEIGHT, VEL)
    enemy_group.update(target, WIDTH, HEIGHT, VEL)
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
    enemy1 = Enemy(450, 50, "survivor-idle_rifle_0.png")
    enemy2 = Enemy(600, 450, "survivor-idle_rifle_0.png")
    user_bullets = []
    enemy_bullets = []
    user_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    enemy_group.add(enemy1, enemy2)
    user_group.add(user)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        target = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.event.post(pygame.event.Event(USER_SHOOT))
                    for user in user_group:
                        user_bullets.append(
                            Bullet(user.rect.centerx, user.rect.centery, user.rot, BULLET_VEL, BULLET_WIDTH, BULLET_HEIGHT))
                        target = user
                    BULLET_FIRE_SOUND.play()
                    

                    


        keys_pressed = pygame.key.get_pressed()
        if keys_pressed:
            pass

        handle_bullets(user_bullets, enemy_bullets, user_group, enemy_group)
        draw(user_group, enemy_group, keys_pressed, user_bullets, target)


if __name__ == "__main__":
    main()
