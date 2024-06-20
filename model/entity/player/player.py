from typing import Tuple

import pygame

from model.board_structure import BoardStructure
from model.direction import Direction
from model.eaten_object import EatenObject
from model.entity.entity import Entity
from model.space_params.space_params import SpaceParams
from model.turns import Turns
from settings import DISTANCE_FACTOR

PLAYER_SPRITE_SIZE = 45
SPRITE_FREQUENCY = 7


class Player(Entity):
    def __init__(self, sprites: list, center_position: Tuple, turns: Turns, space_params: SpaceParams, velocity=2,
                 lives=3):
        super().__init__(center_position, turns, space_params, velocity)
        self.sprites = sprites
        self.sprite_index = 0
        self.velocity = velocity
        self.direction = Direction.LEFT
        self.power_up = False
        self.lives = lives
        self.sprite_counter = 0

    def eat(self):
        i = (self.location_y // self.space_params.tile_height)
        j = (self.location_x // self.space_params.tile_width)
        if self.board[i][j] == BoardStructure.DOT.value:
            self.board[i][j] = 0
            return EatenObject.DOT
        elif self.board[i][j] == BoardStructure.BIG_DOT.value:
            self.board[i][j] = 0
            self.power_up = True
            return EatenObject.BIG_DOT
        return EatenObject.NOTHING

    def move(self, screen, direction_command: Direction):
        self._teleport_if_board_limit_reached()
        self._check_borders_ahead()
        self.__calculate_sprite_index()

        turned = self._align_movement_to_cell_center(direction_command)

        if self.direction == Direction.LEFT:
            self.__draw_face_left(screen)
            if self.turns.left:
                self._move_left()
            else:
                self._snap_to_center(self.space_params.tile_width, self.space_params.tile_height)

        if self.direction == Direction.RIGHT:
            self.__draw_face_right(screen)
            if self.turns.right:
                self._move_right()
            else:
                self._snap_to_center(self.space_params.tile_width, self.space_params.tile_height)

        if self.direction == Direction.DOWN:
            self.__draw_face_down(screen)
            if self.turns.down:
                self._move_down()
            else:
                self._snap_to_center(self.space_params.tile_width, self.space_params.tile_height)
        if self.direction == Direction.UP:
            self.__draw_face_up(screen)
            if self.turns.up:
                self._move_up()
            else:
                self._snap_to_center(self.space_params.tile_width, self.space_params.tile_height)
        return turned

    def __calculate_sprite_index(self):
        self.sprite_counter += 1
        if self.sprite_counter % SPRITE_FREQUENCY == 0:
            self.sprite_index += 1
        if self.sprite_counter % ((len(self.sprites) - 1) * SPRITE_FREQUENCY) == 0:
            self.sprite_index = 0

    def __draw_face_left(self, screen):
        screen.blit(pygame.transform.flip(self.sprites[self.sprite_index], True, False),
                    (self.top_left_x, self.top_left_y))

    def __draw_face_right(self, screen):
        screen.blit(self.sprites[self.sprite_index],
                    (self.top_left_x, self.top_left_y))

    def __draw_face_down(self, screen):
        screen.blit(pygame.transform.rotate(self.sprites[self.sprite_index], 270),
                    (self.top_left_x, self.top_left_y))

    def __draw_face_up(self, screen):
        screen.blit(pygame.transform.rotate(self.sprites[self.sprite_index], 90),
                    (self.top_left_x, self.top_left_y))

    def _check_borders_ahead(self):
        # Checks next cell based on current entity position and direction and
        # permits or prohibits to turn in certain direction depending on obstacles ahead
        x = self.location_x
        y = self.location_y
        i = (y // self.space_params.tile_height)
        j = ((x + DISTANCE_FACTOR) // self.space_params.tile_width) - 1

        if self._is_asle_ahead(i, j):
            self.turns.left = True
        else:
            self.turns.left = False

        i = (y // self.space_params.tile_height)
        j = ((x - DISTANCE_FACTOR) // self.space_params.tile_width) + 1
        if self._is_asle_ahead(i, j):
            self.turns.right = True
        else:
            self.turns.right = False
        i = ((y + DISTANCE_FACTOR) // self.space_params.tile_height) - 1
        j = (x // self.space_params.tile_width)
        if self._is_asle_ahead(i, j):
            self.turns.up = True
        else:
            self.turns.up = False

        i = ((y - DISTANCE_FACTOR) // self.space_params.tile_height) + 1
        j = (x // self.space_params.tile_width)
        if self._is_asle_ahead(i, j):
            self.turns.down = True
        else:
            self.turns.down = False
