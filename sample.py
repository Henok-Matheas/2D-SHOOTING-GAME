import os
import pygame
from gameWalls import walls
from collections import deque, defaultdict
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
VEL = 10

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 44
ANGLE = 90
BULLET_VEL = 7
MAX_BULLETS = 5
BULLET_WIDTH, BULLET_HEIGHT = 5, 5

DAMAGE = 5


YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(
#     "Assets", "Grenade+1.mp3"))
# BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join(
#     "Assets", "Gun+Silencer.mp3"))


# SPACE = pygame.transform.scale(
#     pygame.image.load(os.path.join("Assets", 'space.png')), (WIDTH, HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png"))

YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), ANGLE)

YELLOW_SPACESHIP2 = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), ANGLE)

YELLOW_SPACESHIP3 = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), ANGLE)

# RED_SPACESHIP_IMAGE = pygame.image.load(
#     os.path.join("Assets", "spaceship_red.png"))

# RED_SPACESHIP = pygame.transform.rotate(
#     pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -ANGLE)


BORDER = pygame.Rect(WIDTH / 2 - 5, 0, 10, HEIGHT)


def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(winner_text, ((WIDTH // 2) -
                winner_text.get_width // 2, HEIGHT // 2))

    pygame.display.update()
    pygame.time.delay(5000)


def draw(yellow2, yellow3, yellow):
    WINDOW.fill(BLACK)
    walls.draw(WINDOW)

    # red_health_text = HEALTH_FONT.render(
    #     "HEALTH: " + str(red_health), 1, WHITE)
    # yellow_health_text = HEALTH_FONT.render(
    #     "HEALTH: " + str(yellow_health), 1, WHITE)

    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(YELLOW_SPACESHIP2, (yellow2.x, yellow2.y))
    WINDOW.blit(YELLOW_SPACESHIP3, (yellow3.x, yellow3.y))


    pygame.display.update()


def yellow_movement_handler(yellow, p):
    yellow.x = p[0]
    yellow.y = p[1]

    # initialx, initialy = yellow.x, yellow.y
    
    
    # if keys_pressed[pygame.K_d] and yellow.x+ yellow.height + VEL < WIDTH:
    #     yellow.x += VEL
    # if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
    #     yellow.x -= VEL 
    # if keys_pressed[pygame.K_w] and  yellow.y - VEL  > 0:
    #     yellow.y -= VEL 
    # if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.width < HEIGHT:
    #     yellow.y += VEL 

    # for i in walls:
    #     if yellow.colliderect(i.rect):
    #         yellow.x = initialx
    #         yellow.y = initialy
    #         break
def retrace(start, paths):

        cur = start
        path = []

        while cur != None:
            path.append(cur) 
            cur = paths[cur][0]
            
        return path

dirc = [[0, VEL], [VEL, 0], [VEL,VEL], [-VEL, -VEL], [0,-VEL],[-VEL,0],[-VEL, VEL], [VEL, -VEL]]
def s(yellow, target):
    paths = defaultdict(list)
    q = deque()
    q.append([(yellow.x, yellow.y), None])
    visited = set()
    while q:
        
        print(q)
        current = q.popleft()
      
        if current[0] not in paths:
            paths[current[0]] = [current[1]]
        
        visited.add(current[0])
        if abs(target[0] -current[0][0]) < 10 and abs(target[1] -current[0][1]) < 10:
            return retrace(current[0], paths)

        for d in dirc:
            new = (current[0][0]+d[0] , current[0][1]+d[1])
            if new not in visited and new[0] >= 0 and new[0] <= WIDTH and new[1] >= 0 and new[1] <= HEIGHT:
                pos = pygame.Rect(new[0], new[1], 20, 20)
                coll = False
                for i in walls:
                    if pos.colliderect(i.rect):
                        coll = True
                        break
                if not coll:
                    visited.add(new)
                    q.append([new, current[0]])
    return []



# def red_movement_handler(keys_pressed, red):
#     if keys_pressed[pygame.K_RIGHT]:
#         red.x += VEL if (red.x + VEL + SPACESHIP_WIDTH) < WIDTH else 0
#     if keys_pressed[pygame.K_LEFT]:
#         red.x -= VEL if (red.x - VEL) > BORDER.x + BORDER.width else 0

#     if keys_pressed[pygame.K_UP]:
#         red.y -= VEL if (red.y - VEL) > 0 else 0
#     if keys_pressed[pygame.K_DOWN]:
#         red.y += VEL if (red.y + VEL + SPACESHIP_HEIGHT) < HEIGHT else 0


def handle_bullets(yellow_bullets,yellow):
    for bullet in yellow_bullets:
        if bullet == None:
            continue
        bullet.x += BULLET_VEL

        # if red.colliderect(bullet):
        #     print("red has been shot")
        #     pygame.event.post(pygame.event.Event(RED_HIT))
        # #     yellow_bullets.remove(bullet)

        # elif bullet.x > WIDTH:
        #     yellow_bullets.remove(bullet)

    # for bullet in red_bullets:
    #     if bullet == None:
    #         continue
    #     bullet.x -= BULLET_VEL

    #     if yellow.colliderect(bullet):
    #         print("yellow has been shot")
    #         pygame.event.post(pygame.event.Event(YELLOW_HIT))
    #         red_bullets.remove(bullet)
    #     elif bullet.x < 0:
    #         red_bullets.remove(bullet)


def main():
    yellow = pygame.Rect(850, 450, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow2 = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow3 = pygame.Rect(400, 400, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_bullets = []
    red_bullets = []
    path = s(yellow, [yellow2.x,yellow2.y])
    print(path)
    yellow_health = 100
    red_health = 100

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                #     bullet = pygame.Rect(
                #         red.x + red.width, red.y + (red.height / 2) - BULLET_HEIGHT / 2, BULLET_WIDTH, BULLET_HEIGHT)
                #     red_bullets.append(bullet)
                #     BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + (yellow.height / 2) - BULLET_HEIGHT / 2, BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()

            # if event.type == RED_HIT:
            #     red_health -= DAMAGE
            #     BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= DAMAGE
                # BULLET_HIT_SOUND.play()

            # winner_text = ""

            # if red_health <= 0:
            #     winner_text = "RED HAS WON"

            # if red_health <= 0:
            #     winner_text = "YELLOW HAS WON"

            # if winner_text:
            #     draw_winner(winner_text)
            #     break

        keys_pressed = pygame.key.get_pressed()
        # handle_bullets(yellow_bullets, red_bullets, yellow, red)
        if path:
            yellow_movement_handler(yellow, path.pop())
        # red_movement_handler(keys_pressed, red)

        draw(yellow2, yellow3, yellow)


if __name__ == "__main__":
    main()