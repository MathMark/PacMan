import enum
from typing import Tuple

import pygame

from model.player import Player
from model.space_params.space_params import SpaceParams
from model.turns import Turns

GHOST_SPRITE_SIZE = (45, 45)


class Ghost:
    def __init__(self, init_position: Tuple, img, dead_img, spooked_img,
                 direction, target: Player, turns: Turns, space_params: SpaceParams, velocity=2):
        self.center_x = init_position[0]
        self.center_y = init_position[1]
        self.x_pos = self.center_x - GHOST_SPRITE_SIZE[1] // 2
        self.y_pos = self.center_y - GHOST_SPRITE_SIZE[1] // 2
        self.velocity = velocity
        self.img = img
        self.dead_img = dead_img
        self.spooked_img = spooked_img
        self.direction = direction
        self.target = target
        self.condition = self.Condition.CHASE
        self.turns = turns
        self.space_params = space_params
        self.board = space_params.board_definition.board

    def set_to_chase(self):
        self.condition = self.Condition.CHASE

    def set_to_spooked(self):
        self.condition = self.Condition.SPOOKED

    def set_to_dead(self):
        self.condition = self.Condition.DEAD

    def draw(self, screen):
        if self.condition == self.Condition.CHASE:
            screen.blit(pygame.transform.flip(self.img, True, False),
                        (self.x_pos, self.y_pos))
        elif self.condition == self.Condition.SPOOKED:
            screen.blit(pygame.transform.flip(self.spooked_img, True, False),
                        (self.x_pos, self.y_pos))
        else: #dead
            screen.blit(pygame.transform.flip(self.dead_img, True, False),
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
        DEAD = 1
        SPOOKED = 2


