import pygame

from global_variables import WIDTH, HEIGHT
from levels.level_1 import *
from levels.level_content_initializer import LevelContentInitializer
from model.direction import Direction

run = True

pygame.init()
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

level1_init = LevelContentInitializer(level_1, screen)
game_engine = level1_init.init_game_engine()

while run:

    timer.tick(FPS)
    screen.fill('black')

    game_engine.tick()

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
