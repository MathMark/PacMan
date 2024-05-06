import pygame

from draw.draw_manager import DrawManager
from levels.level_1 import level_1

fps = 60
WIDTH = 900
HEIGHT = 950

run = True

pygame.init()
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

draw_manager = DrawManager(screen, WIDTH, HEIGHT)

while run:
    timer.tick(fps)
    screen.fill('black')

    draw_manager.draw_level(level_1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
