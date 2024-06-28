import enum
from typing import Tuple

import pygame

from model.board_structure import BoardStructure
from model.direction import Direction
from model.eaten_object import EatenObject
from model.entity.entity import Entity
from model.space_params.space_params import SpaceParams
from model.turns import Turns
from settings import *


class Player(Entity):
    def __init__(self, sprites: list, center_position: Tuple, turns: Turns, space_params: SpaceParams, death_sprites: list, velocity=2,
                 lives=3):
        super().__init__(center_position, turns, space_params, velocity)
        self.sprites = sprites
        self.death_sprites = death_sprites
        self.sprite_index = 0
        self.death_animation_sprite_index = 0
        self.death_sprite_counter = 0
        self.velocity = velocity
        self.direction = Direction.RIGHT
        self.lives = lives
        self.sprite_counter = 0
        self.state = self.State.READY
        self.score_multiplier = 1

        self.powerup = False
        self.powerup_counter = 0

    def set_to_ready(self):
        self.state = self.State.READY
        self.reset_position()

    def reset_position(self):
        super().reset_position()
        self.direction = Direction.RIGHT

    def set_to_eaten(self):
        self.state = self.State.EATEN

    def set_to_chase(self):
        self.state = self.State.CHASE

    def is_ready(self):
        return self.state == self.State.READY

    def is_eaten(self):
        return self.state == self.State.EATEN

    def is_chasing(self):
        return self.state == self.State.CHASE

    def eat(self):
        self.__calc_power_up_counter()
        i = (self.location_y // self.space_params.tile_height)
        j = (self.location_x // self.space_params.tile_width)

        if self.board[i][j] == BoardStructure.DOT.value:
            self.sfx.play_munch()
            self.board[i][j] = 0
            return EatenObject.DOT
        elif self.board[i][j] == BoardStructure.BIG_DOT.value:
            self.sfx.power_pellet.play()
            self.board[i][j] = 0
            self.powerup = True
            return EatenObject.BIG_DOT
        return EatenObject.NOTHING

    def __calc_power_up_counter(self):
        if self.powerup:
            if self.powerup_counter <= 0:
                self.powerup = False
                self.score_multiplier = 1
                self.powerup_counter = 0
        self.powerup_counter -= 1

    def play_death_animation(self, screen):
        self.__calculate_death_sprite_index()
        screen.blit(self.death_sprites[self.death_animation_sprite_index],
                    (self.top_left_x, self.top_left_y))
        if self.death_animation_sprite_index == len(self.death_sprites) - 2:
            self.set_to_ready()
            self.death_animation_sprite_index = 0
            self.lives -= 1

    def render(self, screen):
        self.__calculate_sprite_index()
        if self.direction == Direction.LEFT:
            self.__draw_face_left(screen)
        elif self.direction == Direction.RIGHT:
            self.__draw_face_right(screen)
        elif self.direction == Direction.DOWN:
            self.__draw_face_down(screen)
        elif self.direction == Direction.UP:
            self.__draw_face_up(screen)

    def move(self, screen, direction_command: Direction):
        self._teleport_if_board_limit_reached()
        self._check_borders_ahead()

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
        if self.sprite_counter % PLAYER_SPRITE_FREQUENCY == 0:
            self.sprite_index += 1
        if self.sprite_counter % ((len(self.sprites) - 1) * PLAYER_SPRITE_FREQUENCY) == 0:
            self.sprite_index = 0

    def __calculate_death_sprite_index(self):
        self.death_sprite_counter += 1
        if self.death_sprite_counter % PLAYER_SPRITE_FREQUENCY == 0:
            self.death_animation_sprite_index += 1
        if self.death_sprite_counter % ((len(self.death_sprites) - 1) * PLAYER_SPRITE_FREQUENCY) == 0:
            self.death_animation_sprite_index = 0

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

    class State(enum.Enum):
        READY = 0
        EATEN = 1
        CHASE = 2
