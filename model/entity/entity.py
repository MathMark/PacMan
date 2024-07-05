from typing import Tuple

import pygame

from settings import *
from model.direction import Direction
from model.space_params.space_params import SpaceParams
from model.turns import Turns


class Entity:
    def __init__(self, center_position: Tuple, turns: Turns, space_params: SpaceParams,
                 velocity=DEFAULT_VELOCITY):
        self.space_params = space_params
        # entity location aligned by tile center
        self.location_x = center_position[0]
        self.location_y = center_position[1]

        # entity top left point - to know where to draw entity sprite
        self.top_left_x = self.location_x - SPRITE_SIZE[0] // 2
        self.top_left_y = self.location_y - SPRITE_SIZE[1] // 2

        self.initial_pos = self.location_x, self.location_y

        self.velocity = velocity
        self.direction = Direction.RIGHT
        self.turns = turns

        self.board = space_params.board_definition.board
        self.sfx = self.SoundEffects()

    def reset_position(self):
        self.location_x = self.initial_pos[0]
        self.location_y = self.initial_pos[1]
        self.top_left_x = self.location_x - SPRITE_SIZE[0] // 2
        self.top_left_y = self.location_y - SPRITE_SIZE[1] // 2

    def render(self, screen):
        pass

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
        pass

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
        self.top_left_x = self.location_x - SPRITE_SIZE[0] // 2
        self.top_left_y = self.location_y - SPRITE_SIZE[1] // 2

    def _is_at_center(self, cell_width, cell_height):
        return (self.location_x - cell_width // 2) % cell_width < 2 and \
            (self.location_y - cell_height // 2) % cell_height < 2

    def _teleport_if_board_limit_reached(self):
        left_i = (self.top_left_y // self.space_params.tile_height)
        left_j = (self.top_left_x // self.space_params.tile_width)

        right_i = ((self.top_left_y + SPRITE_SIZE[0]) // self.space_params.tile_height)
        right_j = ((self.top_left_x + SPRITE_SIZE[1]) // self.space_params.tile_width)

        if left_j >= self.space_params.board_definition.width - 1:
            self.__teleport(self.space_params.tile_width, self.top_left_y)
        if right_j < 1:
            self.__teleport((self.space_params.board_definition.width - 1) * self.space_params.tile_width,
                            self.top_left_y)
        if left_i >= self.space_params.board_definition.height - 1:
            self.__teleport(self.top_left_x, self.space_params.tile_height)
        if right_i < 1:
            self.__teleport(self.top_left_x,
                            (self.space_params.board_definition.height - 1) * self.space_params.tile_height)

    def _is_asle_ahead(self, i, j):
        if i > self.space_params.board_definition.height - 1 or j > self.space_params.board_definition.width - 1:
            return True
        else:
            return self.board[i][j] < 3

    def __teleport(self, x, y):
        self.top_left_x = x
        self.top_left_y = y
        self.location_x = self.top_left_x + SPRITE_SIZE[0] // 2
        self.location_y = self.top_left_y + SPRITE_SIZE[1] // 2

    class SoundEffects:
        def __init__(self):
            self.munch_i = False
            self.ghost_eaten = pygame.mixer.Sound('media/eat_ghost.wav')
            self.munch = [pygame.mixer.Sound('media/munch_1.wav'), pygame.mixer.Sound('media/munch_2.wav')]
            self.power_pellet = pygame.mixer.Sound('media/power_pellet.wav')
            self.retreating = pygame.mixer.Sound('media/retreating.wav')
            self.pacman_death = pygame.mixer.Sound('media/pacman_death.wav')

        def play_munch(self):
            if self.munch_i:
                self.munch[1].play()
                self.munch_i = False
            else:
                self.munch[0].play()
                self.munch_i = True

