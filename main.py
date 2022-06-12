import os
import pygame


WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frist Game")
pygame.font.init()
pygame.mixer.init()


HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 40)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
FPS = 60
VEL = 5

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 44
ANGLE = 90
BULLET_VEL = 7
MAX_BULLETS = 5
BULLET_WIDTH, BULLET_HEIGHT = 5, 5

DAMAGE = 5


YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(
    "Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(
    "Assets", "Gun+Silencer.mp3"))


SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", 'space.png')), (WIDTH, HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png"))

YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), ANGLE)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_red.png"))

RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -ANGLE)


BORDER = pygame.Rect(WIDTH / 2 - 5, 0, 10, HEIGHT)


def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(winner_text, ((WIDTH // 2) -
                winner_text.get_width // 2, HEIGHT // 2))

    pygame.display.update()
    pygame.time.delay(5000)


def draw(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health):
    WINDOW.blit(SPACE, (0, 0))

    red_health_text = HEALTH_FONT.render(
        "HEALTH: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "HEALTH: " + str(yellow_health), 1, WHITE)

    WINDOW.blit(red_health_text, (WIDTH - red_health_text.get_width(), 0))
    WINDOW.blit(yellow_health_text, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    pygame.display.update()


def yellow_movement_handler(keys_pressed, yellow):
    if keys_pressed[pygame.K_d]:
        yellow.x += VEL if (yellow.x + VEL + SPACESHIP_WIDTH) < BORDER.x else 0
    if keys_pressed[pygame.K_a]:
        yellow.x -= VEL if (yellow.x - VEL) > 0 else 0
    if keys_pressed[pygame.K_w]:
        yellow.y -= VEL if (yellow.y - VEL) > 0 else 0
    if keys_pressed[pygame.K_s]:
        yellow.y += VEL if (yellow.y + VEL + SPACESHIP_HEIGHT) < HEIGHT else 0


def red_movement_handler(keys_pressed, red):
    if keys_pressed[pygame.K_RIGHT]:
        red.x += VEL if (red.x + VEL + SPACESHIP_WIDTH) < WIDTH else 0
    if keys_pressed[pygame.K_LEFT]:
        red.x -= VEL if (red.x - VEL) > BORDER.x + BORDER.width else 0

    if keys_pressed[pygame.K_UP]:
        red.y -= VEL if (red.y - VEL) > 0 else 0
    if keys_pressed[pygame.K_DOWN]:
        red.y += VEL if (red.y + VEL + SPACESHIP_HEIGHT) < HEIGHT else 0


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        if bullet == None:
            continue
        bullet.x += BULLET_VEL

        if red.colliderect(bullet):
            print("red has been shot")
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        if bullet == None:
            continue
        bullet.x -= BULLET_VEL

        if yellow.colliderect(bullet):
            print("yellow has been shot")
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def main():
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_bullets = []
    red_bullets = []

    yellow_health = 100
    red_health = 100

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x + red.width, red.y + (red.height / 2) - BULLET_HEIGHT / 2, BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + (yellow.height / 2) - BULLET_HEIGHT / 2, BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= DAMAGE
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= DAMAGE
                BULLET_HIT_SOUND.play()

            winner_text = ""

            if red_health <= 0:
                winner_text = "RED HAS WON"

            if red_health <= 0:
                winner_text = "YELLOW HAS WON"

            if winner_text:
                draw_winner(winner_text)
                break

        keys_pressed = pygame.key.get_pressed()
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        yellow_movement_handler(keys_pressed, yellow)
        red_movement_handler(keys_pressed, red)

        draw(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health)

    main()


if __name__ == "__main__":
    main()
