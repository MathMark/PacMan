import pygame

from draw.draw_manager import DrawManager
from levels.level_1 import level_1
from model.direction import Direction
from model.player import Player, PLAYER_SPRITE_SIZE


def load_player():
    player_images = []
    for i in range(1, 5):
        player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'),
                                                    (PLAYER_SPRITE_SIZE, PLAYER_SPRITE_SIZE)))
    return Player(player_images, WIDTH // 2, HEIGHT // 2)


fps = 60
WIDTH = 900
HEIGHT = 950

run = True

pygame.init()
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])


player = load_player()

draw_manager = DrawManager(screen, level_1, player)

while run:

    timer.tick(fps)
    screen.fill('black')

    draw_manager.draw_level(level_1)
    draw_manager.draw_player()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                draw_manager.direction_command = Direction.LEFT
            if event.key == pygame.K_RIGHT:
                draw_manager.direction_command = Direction.RIGHT
            if event.key == pygame.K_DOWN:
                draw_manager.direction_command = Direction.DOWN
            if event.key == pygame.K_UP:
                draw_manager.direction_command = Direction.UP
    pygame.display.flip()

pygame.quit()
