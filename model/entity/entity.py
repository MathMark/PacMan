from typing import Tuple

from settings import SPRITE_SIZE, DISTANCE_FACTOR
from model.direction import Direction
from model.space_params.space_params import SpaceParams
from model.turns import Turns


class Entity:
    def __init__(self, center_position: Tuple, turns: Turns, space_params: SpaceParams, velocity=2):
        # entity location aligned by tile center
        self.location_x = center_position[0]
        self.location_y = center_position[1]

        # entity top left point - to know where to draw entity sprite
        self.top_left_x = self.location_x - SPRITE_SIZE // 2
        self.top_left_y = self.location_y - SPRITE_SIZE // 2

        self.velocity = velocity
        self.direction = Direction.LEFT
        self.turns = turns
        self.space_params = space_params
        self.board = space_params.board_definition.board

    def _move_right(self):
        self.location_x += self.velocity
        self.top_left_x += self.velocity


    def _move_left(self):
        self.location_x -= self.velocity
        self.top_left_x -= self.velocity

    def _move_up(self):
        self.location_y -= self.velocity
        self.top_left_y -= self.velocity

    def _move_down(self):
        self.location_y += self.velocity
        self.top_left_y += self.velocity


    def _check_borders_ahead(self):
        # Checks next cell based on current entity position and direction and
        # permits or prohibits to turn in certain direction depending on obstacles ahead
        x = self.location_x
        y = self.location_y
        i = (y // self.space_params.tile_height)
        j = ((x + DISTANCE_FACTOR) // self.space_params.tile_width) - 1
        if self.space_params.board_definition.check_coordinate_within(i, j) and self.board[i][j] < 3:
            self.turns.left = True
        else:
            self.turns.left = False

        i = (y // self.space_params.tile_height)
        j = ((x - DISTANCE_FACTOR) // self.space_params.tile_width) + 1
        if self.space_params.board_definition.check_coordinate_within(i, j) and self.board[i][j] < 3:
            self.turns.right = True
        else:
            self.turns.right = False
        i = ((y + DISTANCE_FACTOR) // self.space_params.tile_height) - 1
        j = (x // self.space_params.tile_width)
        if self.space_params.board_definition.check_coordinate_within(i, j) \
                and (self.board[i][j] < 3 or self.board[i][j] == 9):
            self.turns.up = True
        else:
            self.turns.up = False

        i = ((y - DISTANCE_FACTOR) // self.space_params.tile_height) + 1
        j = (x // self.space_params.tile_width)
        if self.space_params.board_definition.check_coordinate_within(i, j) and self.board[i][j] < 3:
            self.turns.down = True
        else:
            self.turns.down = False

    def _align_movement_to_cell_center(self, direction_command):
        # Ensures entity moves strictly by cell centers and not blocked in corners.

        if direction_command == Direction.LEFT and self.turns.left:
            if self.direction == Direction.RIGHT:
                self.direction = direction_command
            else:
                if self._is_at_center(self.space_params.tile_width, self.space_params.tile_height):
                    self.direction = direction_command
            return True
        elif direction_command == Direction.RIGHT and self.turns.right:
            if self.direction == Direction.LEFT:
                self.direction = direction_command
            else:
                if self._is_at_center(self.space_params.tile_width, self.space_params.tile_height):
                    self.direction = direction_command
            return True
        elif direction_command == Direction.UP and self.turns.up:
            if self.direction == Direction.DOWN:
                self.direction = direction_command
            else:
                if self._is_at_center(self.space_params.tile_width, self.space_params.tile_height):
                    self.direction = direction_command
            return True
        elif direction_command == Direction.DOWN and self.turns.down:
            if self.direction == Direction.UP:
                self.direction = direction_command
            else:
                if self._is_at_center(self.space_params.tile_width, self.space_params.tile_height):
                    self.direction = direction_command
            return True
        else:
            return False

    def _snap_to_center(self, cell_width, cell_height):
        self.location_x = round(self.location_x // cell_width) * cell_width + cell_width // 2
        self.location_y = round(self.location_y // cell_height) * cell_height + cell_height // 2
        self.top_left_x = self.location_x - SPRITE_SIZE // 2
        self.top_left_y = self.location_y - SPRITE_SIZE // 2

    def _is_at_center(self, cell_width, cell_height):
        return (self.location_x - cell_width // 2) % cell_width < 2 and \
            (self.location_y - cell_height // 2) % cell_height < 2

    def _teleport_if_board_limit_reached(self):
        i = (self.top_left_y // self.space_params.tile_height)
        j = (self.top_left_x // self.space_params.tile_width)
        if j >= self.space_params.board_definition.width - 1:
            self.__teleport(self.space_params.tile_width, self.top_left_y)
        if j < 1:
            self.__teleport((self.space_params.board_definition.width - 1) * self.space_params.tile_width,
                            self.top_left_y)
        if i >= self.space_params.board_definition.height - 1:
            self.__teleport(self.top_left_x, self.space_params.tile_height)
        if i < 1:
            self.__teleport(self.top_left_x,
                            (self.space_params.board_definition.height - 1) * self.space_params.tile_height)

    def __teleport(self, x, y):
        # TODO: fix it. we should pass coordinates aligned by tile center!
        self.top_left_x = x
        self.top_left_y = y
        self.location_x = self.top_left_x + SPRITE_SIZE // 2
        self.location_y = self.top_left_y + SPRITE_SIZE // 2