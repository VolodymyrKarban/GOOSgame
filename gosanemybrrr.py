import random
from random import randint
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_ESCAPE, K_END

pygame.init()

FPS = pygame.time.Clock()
FONT = pygame.font.SysFont("Verdana", 20)
END = pygame.font.SysFont("Verdana", 250)
HEIGHT = 1000
WIDTH = 1800

COLOR_PLAYER = (0, 0, 255)
COLOR_DISPLAY = (0, 200, 250)
COLOR_RED = (255, 0, 100)
COLOR_GREAN = (100, 255, 0)
COLOR_TEXT = (0, 0, 0)

my_display = pygame.display.set_mode((WIDTH, HEIGHT))
scenery = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))
scenery_x1 = 0
scenery_x2 = scenery.get_width()
scenery_move = 2

goos_size = (120, 50)
# goos = pygame.Surface(goos_size)
# goos.fill((COLOR_PLAYER))
goos = pygame.transform.scale(
    pygame.image.load("player.png"), (goos_size)).convert_alpha()
goos_rect = goos.get_rect()

petriot_size = (70, 50)
petriot = pygame.transform.scale(
    pygame.image.load("Petriot.png"), (petriot_size)).convert_alpha()
petriot_rect = (0, HEIGHT - 50, 70, 50)

grad_size = (80, 50)
grad = pygame.transform.scale(
    pygame.image.load("grad.png"), (grad_size)).convert_alpha()
grad_rect = (WIDTH - 80, HEIGHT - 50, WIDTH, HEIGHT)

enemies = []
bonuses = []
brrres_1 = []
brrres_2 = []
goos_brrres = []
score = 0

def create_enemy():
    enemy_size = (120, 25)
    enemy = pygame.transform.scale(
        pygame.image.load("enemy.png"), (120, 25)
    ).convert_alpha()
    # enemy = pygame.Surface(enemy_size)
    # enemy.fill(COLOR_RED)
    enemy_rect = pygame.Rect(WIDTH, randint(50, HEIGHT - 50), *enemy_size)
    enemy_move = [randint(-8, -1), randint(-1, 1)]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

def create_bonus():
    bonus_size = (40, 50)
    bonus = pygame.transform.scale(
        pygame.image.load("bonus.png"), (bonus_size)
    ).convert_alpha()
    # bonus = pygame.Surface(bonus_size)
    # bonus.fill(COLOR_GREAN)
    bonus_rect = pygame.Rect(randint(200, WIDTH - 200), 0, *bonus_size)
    bonus_move = [randint(-2, 2), randint(1, 4)]
    return [bonus, bonus_rect, bonus_move]

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1000)

def create_brrr_1():
    brrr_size = (40, 10)
    # brrr = pygame.Surface(brrr_size)
    # brrr.fill((255, 55, 55))
    brrr = pygame.transform.scale(
        pygame.image.load("enemy.png"), (brrr_size)
    ).convert_alpha()
    brrr_rect = pygame.Rect(WIDTH, HEIGHT, *brrr_size)
    brrr_move = [-10, randint(-9, -2)]
    return [brrr, brrr_rect, brrr_move]


CREATE_BRRR_1 = pygame.USEREVENT + 3
pygame.time.set_timer(CREATE_BRRR_1, 1000)


def create_brrr_2():
    brrr_size = (10, 2)
    brrr = pygame.Surface(brrr_size)
    brrr.fill((255, 50, 200))
    brrr_rect = pygame.Rect(0, HEIGHT, *brrr_size)
    brrr_move = [10, randint(-12, -8)]
    return [brrr, brrr_rect, brrr_move]


CREATE_BRRR_2 = pygame.USEREVENT + 4
pygame.time.set_timer(CREATE_BRRR_2, 100)


def goos_brrr(x_y):
    brrr_size = (20, 2)
    brrr = pygame.Surface(brrr_size)
    brrr.fill((255, 55, 55))
    brrr_rect = pygame.Rect(x_y.move((65, 25)))
    brrr_move = [15, 0]
    return [brrr, brrr_rect, brrr_move]


GOOS_BRRR = pygame.USEREVENT + 5
pygame.time.set_timer(GOOS_BRRR, 100)

goos_rect = goos_rect.move(randint(200, 800), randint(100, HEIGHT - 100))

play_game = True
while play_game:
    FPS.tick(150)

    for event in pygame.event.get():
        if event.type == QUIT:
            play_game = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CREATE_BRRR_1:
            brrres_1.append(create_brrr_1())
        if event.type == CREATE_BRRR_2:
            brrres_2.append(create_brrr_2())

        keys = pygame.key.get_pressed()

        if event.type == GOOS_BRRR and keys[K_END]:
            goos_brrres.append(goos_brrr(goos_rect))

    scenery_x1 -= scenery_move
    scenery_x2 -= scenery_move

    if scenery_x1 < -scenery.get_width():
        scenery_x1 = scenery.get_width()

    if scenery_x2 < -scenery.get_width():
        scenery_x2 = scenery.get_width()

    my_display.blit(scenery, (scenery_x1, 0))
    my_display.blit(scenery, (scenery_x2, 0))

    if keys[K_ESCAPE]:
        play_game = False

    if keys[K_DOWN] and goos_rect.bottom < HEIGHT:
        goos_rect = goos_rect.move(0, 5)
    if keys[K_RIGHT] and goos_rect.right < WIDTH:
        goos_rect = goos_rect.move(5, 0)
    if keys[K_LEFT] and goos_rect.left > 0:
        goos_rect = goos_rect.move(-5, 0)
    if keys[K_UP] and goos_rect.top > 0:
        goos_rect = goos_rect.move(0, -5)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        my_display.blit(enemy[0], enemy[1])
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))
        if goos_rect.colliderect(enemy[1]):
            play_game = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        my_display.blit(bonus[0], bonus[1])
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
        if goos_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score = score + 1

    for brrr in brrres_1:
        brrr[1] = brrr[1].move(brrr[2])
        my_display.blit(brrr[0], brrr[1])
        if brrr[1].top < 0:
            brrres_1.pop(brrres_1.index(brrr))
        if goos_rect.colliderect(brrr[1]):
            play_game = False

    for brrr in brrres_2:
        brrr[1] = brrr[1].move(brrr[2])
        my_display.blit(brrr[0], brrr[1])
        if brrr[1].top < 0:
            brrres_2.pop(brrres_2.index(brrr))

    for brrr in goos_brrres:
        brrr[1] = brrr[1].move(brrr[2])
        my_display.blit(brrr[0], brrr[1])
        if brrr[1].top > WIDTH:
            brrres_2.pop(brrres_2.index(brrr))
        for match in enemies:
            if match[1].colliderect(brrr[1]):
                enemies.pop(enemies.index(match))
                score = score + 1

    for brrr in brrres_2:
        brrr[1] = brrr[1].move(brrr[2])
        my_display.blit(brrr[0], brrr[1])
        if brrr[1].top > WIDTH:
            brrres_2.pop(brrres_2.index(brrr))
        for match in enemies:
            if match[1].colliderect(brrr[1]):
                enemies.pop(enemies.index(match))
                score = score + 1

    my_display.blit(goos, goos_rect)
    my_display.blit(petriot, petriot_rect)
    my_display.blit(grad, grad_rect)

    text = f"Bonus: {str(score)}"
    my_display.blit(FONT.render((text), True, COLOR_TEXT), (5, 5))

    if play_game == False:
        my_display.blit(END.render(("BOOOM"), True, (0, 255, 0)), (410, 200))
        my_display.blit(END.render(("GAME OVER"), True, (0, 255, 0)), (130, 500))
        pygame.display.flip()
        FPS.tick(0.25)

    pygame.display.flip()
