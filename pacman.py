import pygame

from draw.game_engine import GameEngine
from global_variables import WIDTH, HEIGHT, FPS
from levels.level_1 import level_1
from model.direction import Direction
from model.player import Player, PLAYER_SPRITE_SIZE


def load_player():
    player_images = []
    for i in range(1, 5):
        player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'),
                                                    (PLAYER_SPRITE_SIZE, PLAYER_SPRITE_SIZE)))
    return Player(player_images, (WIDTH // 2), (HEIGHT // 2))

run = True

pygame.init()
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])


player = load_player()

game_engine = GameEngine(screen, level_1, player)

while run:

    timer.tick(FPS)
    screen.fill('black')

    game_engine.draw_level(level_1)
    game_engine.draw_player()
    game_engine.draw_misc()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game_engine.direction_command = Direction.LEFT
            if event.key == pygame.K_RIGHT:
                game_engine.direction_command = Direction.RIGHT
            if event.key == pygame.K_DOWN:
                game_engine.direction_command = Direction.DOWN
            if event.key == pygame.K_UP:
                game_engine.direction_command = Direction.UP
    pygame.display.flip()

pygame.quit()
