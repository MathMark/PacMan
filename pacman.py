import sys

import pygame

from constants import WIDTH, HEIGHT
from levels.level_1 import *
from levels.level_content_initializer import LevelContentInitializer
from model.direction import Direction


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.timer = pygame.time.Clock()
        level1_init = LevelContentInitializer(level_1, self.screen)
        self.game_engine = level1_init.init_game_engine()

    def update(self):
        self.timer.tick(FPS)
        self.game_engine.tick()
        pygame.display.flip()

    def draw(self):
        self.screen.fill('black')

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.game_engine.direction_command = Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    self.game_engine.direction_command = Direction.RIGHT
                if event.key == pygame.K_DOWN:
                    self.game_engine.direction_command = Direction.DOWN
                if event.key == pygame.K_UP:
                    self.game_engine.direction_command = Direction.UP

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
