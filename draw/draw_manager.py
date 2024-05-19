import numpy as np
import pygame
from pygame import Surface

from model.board_structure import BoardStructure
from model.direction import Direction
from model.level_config import LevelConfig
import math

from model.player import Player

PI = math.pi
SPRITE_FREQUENCY = 7
FLICK_FREQUENCY = 20


class DrawManager:

    def __init__(self, screen: Surface, level: LevelConfig, player: Player):
        self.screen = screen
        self.board = level.board
        board_size = np.shape(self.board)
        self.board_height = board_size[0]
        self.board_width = board_size[1]
        self.height_ratio = ((screen.get_height() - 50) // self.board_height)
        self.width_ratio = (screen.get_width() // self.board_width)
        self.counter = 0
        self.flicker_counter = 0
        self.flick = True
        self.player = player

    def __calculate_sprite_index(self):
        self.counter += 1
        if self.counter % SPRITE_FREQUENCY == 0:
            self.player.sprite_index += 1
        if self.counter % ((len(self.player.sprites) - 1) * SPRITE_FREQUENCY) == 0:
            self.player.sprite_index = 0

    def draw_player(self):
        self.__calculate_sprite_index()

        if self.player.direction == Direction.LEFT:
            self.screen.blit(pygame.transform.flip(self.player.sprites[self.player.sprite_index], True, False),
                             (self.player.position_x, self.player.position_y))
            self.player.move_left()

        if self.player.direction == Direction.RIGHT:
            self.screen.blit(self.player.sprites[self.player.sprite_index],
                             (self.player.position_x, self.player.position_y))
            self.player.move_right()

        if self.player.direction == Direction.DOWN:
            self.screen.blit(pygame.transform.rotate(self.player.sprites[self.player.sprite_index], 270),
                             (self.player.position_x, self.player.position_y))
            self.player.move_down()
        if self.player.direction == Direction.UP:
            self.screen.blit(pygame.transform.rotate(self.player.sprites[self.player.sprite_index], 90),
                             (self.player.position_x, self.player.position_y))
            self.player.move_up()

    def __calculate_flick(self):
        self.flicker_counter += 1
        if self.flicker_counter % FLICK_FREQUENCY == 0:
            self.flick = not self.flick
        if self.flicker_counter == FLICK_FREQUENCY * 2:
            self.flicker_counter = 0

    def draw_level(self, level_config: LevelConfig):
        self.__calculate_flick()
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == BoardStructure.DOT.value:
                    center = (
                        j * self.width_ratio + (0.5 * self.width_ratio),
                        i * self.height_ratio + (0.5 * self.height_ratio))
                    pygame.draw.circle(self.screen, level_config.gate_color, center, 4)
                if self.board[i][j] == BoardStructure.BIG_DOT.value and not self.flick:
                    center = (
                        j * self.width_ratio + (0.5 * self.width_ratio),
                        i * self.height_ratio + (0.5 * self.height_ratio))
                    pygame.draw.circle(self.screen, level_config.gate_color, center, 10)
                if self.board[i][j] == BoardStructure.VERTICAL_WALL.value:
                    pygame.draw.line(self.screen, level_config.wall_color,
                                     (j * self.width_ratio + (0.5 * self.width_ratio), i * self.height_ratio),
                                     (j * self.width_ratio + (0.5 * self.width_ratio),
                                      i * self.height_ratio + self.height_ratio), 3)
                if self.board[i][j] == BoardStructure.HORIZONTAL_WALL.value:
                    pygame.draw.line(self.screen, level_config.wall_color,
                                     (j * self.width_ratio, i * self.height_ratio + (0.5 * self.height_ratio)),
                                     (j * self.width_ratio + self.width_ratio,
                                      i * self.height_ratio + (0.5 * self.height_ratio)), 3)
                if self.board[i][j] == BoardStructure.TOP_RIGHT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * self.width_ratio - (self.width_ratio * 0.4)) - 2,
                                     (i * self.height_ratio + (0.5 * self.height_ratio)), self.width_ratio,
                                     self.height_ratio],
                                    0, PI / 2, 3)
                if self.board[i][j] == BoardStructure.TOP_LEFT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * self.width_ratio + (self.width_ratio * 0.5)),
                                     (i * self.height_ratio + (0.5 * self.height_ratio)),
                                     self.width_ratio, self.height_ratio], PI / 2, PI,
                                    3)
                if self.board[i][j] == BoardStructure.BOTTOM_LEFT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * self.width_ratio + (self.width_ratio * 0.5)),
                                     (i * self.height_ratio - (0.4 * self.height_ratio)),
                                     self.width_ratio, self.height_ratio], PI,
                                    3 * PI / 2, 3)
                if self.board[i][j] == BoardStructure.BOTTOM_RIGHT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * self.width_ratio - (self.width_ratio * 0.4)) - 2,
                                     (i * self.height_ratio - (0.4 * self.height_ratio)), self.width_ratio,
                                     self.height_ratio],
                                    3 * PI / 2,
                                    2 * PI, 3)
                if self.board[i][j] == BoardStructure.GATE.value:
                    pygame.draw.line(self.screen, level_config.gate_color,
                                     (j * self.width_ratio, i * self.height_ratio + (0.5 * self.height_ratio)),
                                     (j * self.width_ratio + self.width_ratio,
                                      i * self.height_ratio + (0.5 * self.height_ratio)), 3)
