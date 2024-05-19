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
        self.segment_height = ((screen.get_height() - 50) // self.board_height)
        self.segment_width = (screen.get_width() // self.board_width)
        self.counter = 0
        self.flicker_counter = 0
        self.flick = True
        self.player = player
        self.fudge_factor = 15
        self.direction_command = Direction.LEFT

    def __calculate_sprite_index(self):
        self.counter += 1
        if self.counter % SPRITE_FREQUENCY == 0:
            self.player.sprite_index += 1
        if self.counter % ((len(self.player.sprites) - 1) * SPRITE_FREQUENCY) == 0:
            self.player.sprite_index = 0

    def draw_player(self):
        self.__calculate_sprite_index()
        self.__check_turns_allowed()
        if self.player.direction == Direction.LEFT:
            self.screen.blit(pygame.transform.flip(self.player.sprites[self.player.sprite_index], True, False),
                             (self.player.position_x, self.player.position_y))
            if not self.__is_collision_left():
                self.player.move_left()

        if self.player.direction == Direction.RIGHT:
            self.screen.blit(self.player.sprites[self.player.sprite_index],
                             (self.player.position_x, self.player.position_y))
            if not self.__is_collision_right():
                self.player.move_right()

        if self.player.direction == Direction.DOWN:
            self.screen.blit(pygame.transform.rotate(self.player.sprites[self.player.sprite_index], 270),
                             (self.player.position_x, self.player.position_y))
            if not self.__is_collision_down():
                self.player.move_down()
        if self.player.direction == Direction.UP:
            self.screen.blit(pygame.transform.rotate(self.player.sprites[self.player.sprite_index], 90),
                             (self.player.position_x, self.player.position_y))
            if not self.__is_collision_up():
                self.player.move_up()
        self.__eat()

    def __check_turns_allowed(self):
        if self.direction_command == Direction.LEFT:
            coordinate_x = (self.player.center_y // self.segment_height)
            coordinate_y = ((self.player.center_x - self.fudge_factor) // self.segment_width)
        elif self.direction_command == Direction.RIGHT:
            coordinate_x = (self.player.center_y // self.segment_height)
            coordinate_y = ((self.player.center_x + self.fudge_factor) // self.segment_width)
        elif self.direction_command == Direction.UP:
            coordinate_x = ((self.player.center_y - self.fudge_factor) // self.segment_height)
            coordinate_y = (self.player.center_x // self.segment_width)
        else:  # direction == DOWN
            coordinate_x = ((self.player.center_y + self.fudge_factor) // self.segment_height)
            coordinate_y = (self.player.center_x // self.segment_width)

        if self.board[coordinate_x][coordinate_y] < 3:
            self.player.direction = self.direction_command
        else:
            self.direction_command = self.player.direction

    def __eat(self):
        x = (self.player.center_y // self.segment_height)
        y = (self.player.center_x // self.segment_width)
        self.board[x][y] = 0

    def __is_collision_down(self):
        # a bit below player center coordinate
        coordinate_x = (self.player.center_y + self.fudge_factor) // self.segment_height
        coordinate_y = self.player.center_x // self.segment_width
        return self.board[coordinate_x][coordinate_y] >= 3

    def __is_collision_up(self):
        # a bit upper player center coordinate
        coordinate_x = (self.player.center_y - self.fudge_factor) // self.segment_height
        coordinate_y = self.player.center_x // self.segment_width
        return self.board[coordinate_x][coordinate_y] >= 3

    def __is_collision_left(self):
        coordinate_x = self.player.center_y // self.segment_height
        coordinate_y = (self.player.center_x - self.fudge_factor) // self.segment_width
        return self.board[coordinate_x][coordinate_y] >= 3

    def __is_collision_right(self):
        coordinate_x = self.player.center_y // self.segment_height
        coordinate_y = (self.player.center_x + self.fudge_factor) // self.segment_width
        return self.board[coordinate_x][coordinate_y] >= 3

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
                        j * self.segment_width + (0.5 * self.segment_width),
                        i * self.segment_height + (0.5 * self.segment_height))
                    pygame.draw.circle(self.screen, level_config.gate_color, center, 4)
                if self.board[i][j] == BoardStructure.BIG_DOT.value and not self.flick:
                    center = (
                        j * self.segment_width + (0.5 * self.segment_width),
                        i * self.segment_height + (0.5 * self.segment_height))
                    pygame.draw.circle(self.screen, level_config.gate_color, center, 10)
                if self.board[i][j] == BoardStructure.VERTICAL_WALL.value:
                    pygame.draw.line(self.screen, level_config.wall_color,
                                     (j * self.segment_width + (0.5 * self.segment_width), i * self.segment_height),
                                     (j * self.segment_width + (0.5 * self.segment_width),
                                      i * self.segment_height + self.segment_height), 3)
                if self.board[i][j] == BoardStructure.HORIZONTAL_WALL.value:
                    pygame.draw.line(self.screen, level_config.wall_color,
                                     (j * self.segment_width, i * self.segment_height + (0.5 * self.segment_height)),
                                     (j * self.segment_width + self.segment_width,
                                      i * self.segment_height + (0.5 * self.segment_height)), 3)
                if self.board[i][j] == BoardStructure.TOP_RIGHT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * self.segment_width - (self.segment_width * 0.4)) - 2,
                                     (i * self.segment_height + (0.5 * self.segment_height)), self.segment_width,
                                     self.segment_height],
                                    0, PI / 2, 3)
                if self.board[i][j] == BoardStructure.TOP_LEFT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * self.segment_width + (self.segment_width * 0.5)),
                                     (i * self.segment_height + (0.5 * self.segment_height)),
                                     self.segment_width, self.segment_height], PI / 2, PI,
                                    3)
                if self.board[i][j] == BoardStructure.BOTTOM_LEFT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * self.segment_width + (self.segment_width * 0.5)),
                                     (i * self.segment_height - (0.4 * self.segment_height)),
                                     self.segment_width, self.segment_height], PI,
                                    3 * PI / 2, 3)
                if self.board[i][j] == BoardStructure.BOTTOM_RIGHT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * self.segment_width - (self.segment_width * 0.4)) - 2,
                                     (i * self.segment_height - (0.4 * self.segment_height)), self.segment_width,
                                     self.segment_height],
                                    3 * PI / 2,
                                    2 * PI, 3)
                if self.board[i][j] == BoardStructure.GATE.value:
                    pygame.draw.line(self.screen, level_config.gate_color,
                                     (j * self.segment_width, i * self.segment_height + (0.5 * self.segment_height)),
                                     (j * self.segment_width + self.segment_width,
                                      i * self.segment_height + (0.5 * self.segment_height)), 3)
