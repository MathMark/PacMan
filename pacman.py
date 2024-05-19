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
direction = Direction.LEFT

draw_manager = DrawManager(screen, level_1, player)

center_x = player.position_x + 23
center_y = player.position_y + 24

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
                player.direction = Direction.LEFT
            if event.key == pygame.K_RIGHT:
                player.direction = Direction.RIGHT
            if event.key == pygame.K_DOWN:
                player.direction = Direction.DOWN
            if event.key == pygame.K_UP:
                player.direction = Direction.UP
    pygame.display.flip()

pygame.quit()
