import enum
from typing import Tuple, List

import pygame

from model.coordinates import Coordinates
from model.player import Player
from model.space_params.space_params import SpaceParams
from model.turns import Turns

GHOST_SPRITE_SIZE = (45, 45)


class Ghost:
    def __init__(self, init_position: Tuple, img, frightened_img, eaten_img,
                 direction, target: Coordinates, turns: Turns, space_params: SpaceParams, home_corner: Coordinates, velocity=2):
        self.center_x = init_position[0]
        self.center_y = init_position[1]
        self.x_pos = self.center_x - GHOST_SPRITE_SIZE[1] // 2
        self.y_pos = self.center_y - GHOST_SPRITE_SIZE[1] // 2
        self.velocity = velocity
        self.img = img
        self.eaten_img = eaten_img
        self.frightened_img = frightened_img
        self.direction = direction
        self.target = target
        self.condition = self.Condition.CHASE
        self.turns = turns
        self.space_params = space_params
        self.board = space_params.board_definition.board
        self.home_corner = home_corner

    def set_to_chase(self, target: Coordinates):
        self.target = target
        self.condition = self.Condition.CHASE

    def set_to_frightened(self):
        self.condition = self.Condition.FRIGHTENED
        self.target = self.home_corner

    def set_to_eaten(self):
        self.condition = self.Condition.EATEN

    def draw(self, screen):
        print(f'{self.target.x}, {self.target.y}')
        if self.condition == self.Condition.CHASE:
            screen.blit(pygame.transform.flip(self.img, True, False),
                        (self.x_pos, self.y_pos))
        elif self.condition == self.Condition.FRIGHTENED:
            screen.blit(pygame.transform.flip(self.frightened_img, True, False),
                        (self.x_pos, self.y_pos))
        else: #eaten
            screen.blit(pygame.transform.flip(self.eaten_img, True, False),
                        (self.x_pos, self.y_pos))

    def _move_right(self):
        self.x_pos += self.velocity
        self.center_x += self.velocity

    def _move_left(self):
        self.x_pos -= self.velocity
        self.center_x -= self.velocity

    def _move_up(self):
        self.y_pos -= self.velocity
        self.center_y -= self.velocity

    def _move_down(self):
        self.y_pos += self.velocity
        self.center_y += self.velocity

    def move(self):
        pass

    def _check_collisions(self):
        i = (self.center_y // self.space_params.segment_height)
        j = ((self.center_x - self.space_params.fudge_factor) // self.space_params.segment_width)
        if self.space_params.board_definition.check_coordinate_within(i, j) and \
                self.board[i][j] < 3:
            self.turns.left = True
        else:
            self.turns.left = False

        i = (self.center_y // self.space_params.segment_height)
        j = ((self.center_x + self.space_params.fudge_factor) // self.space_params.segment_width)
        if self.space_params.board_definition.check_coordinate_within(i, j) and \
                self.board[i][j] < 3:
            self.turns.right = True
        else:
            self.turns.right = False

        i = ((self.center_y - self.space_params.fudge_factor) // self.space_params.segment_height)
        j = (self.center_x // self.space_params.segment_width)
        if self.space_params.board_definition.check_coordinate_within(i, j) and\
                self.board[i][j] < 3 or self.board[i][j] == 9:
            self.turns.up = True
        else:
            self.turns.up = False

        i = ((self.center_y + self.space_params.fudge_factor) // self.space_params.segment_height)
        j = (self.center_x // self.space_params.segment_width)
        if self.space_params.board_definition.check_coordinate_within(i, j) and\
                self.board[i][j] < 3:
            self.turns.down = True
        else:
            self.turns.down = False

    def _teleport_if_board_limit_reached(self):
        i = (self.center_y // self.space_params.segment_height)
        j = (self.center_x // self.space_params.segment_width)
        if j >= self.space_params.board_definition.width - 1:
            self.teleport(self.space_params.segment_width, self.center_y)
        if j < 1:
            self.teleport((self.space_params.board_definition.width - 1) * self.space_params.segment_width, self.center_y)
        if i >= self.space_params.board_definition.height - 1:
            self.teleport(self.center_x, self.space_params.segment_height)
        if i < 1:
            self.teleport(self.center_y, (self.space_params.board_definition.height - 1) * self.space_params.segment_height)

    def teleport(self, x, y):
        self.center_x = x
        self.center_y = y
        self.x_pos = self.center_x - GHOST_SPRITE_SIZE[0] // 2
        self.y_pos = self.center_y - GHOST_SPRITE_SIZE[1] // 2

    class Condition(enum.Enum):
        CHASE = 0
        EATEN = 1
        FRIGHTENED = 2


