import enum
import math
from typing import Tuple
import pygame
from model.direction import Direction
from model.entity.entity import Entity
from model.entity.player.player import Player
from model.space_params.space_params import SpaceParams
from model.turns import Turns
from settings import DISTANCE_FACTOR, GHOST_HOUSE_COORDINATES_X, GHOST_HOUSE_COORDINATES_Y

GHOST_SPRITE_SIZE = (45, 45)
RUN_POSITION_CHANGE_FREQUENCY = 2


class Ghost(Entity):
    def __init__(self, center_position: Tuple, img, frightened_img, eaten_img, player: Player,
                 turns: Turns, space_params: SpaceParams, home_corner: Tuple, ghost_house_location: Tuple,
                 ghost_house_exit: Tuple,
                 velocity=2):
        super().__init__(center_position, turns, space_params, velocity)
        self.img = img
        self.eaten_img = eaten_img
        self.frightened_img = frightened_img
        self.direction = Direction.UP
        self.player = player
        self.condition = self.State.CHASE
        self.home_corner = home_corner[0] * self.space_params.tile_width - self.space_params.tile_width // 2, \
                           home_corner[1] * self.space_params.tile_height + self.space_params.tile_height // 2
        self.ghost_house_location = ghost_house_location[
                                        0] * self.space_params.tile_width - self.space_params.tile_width // 2, \
                                    ghost_house_location[
                                        1] * self.space_params.tile_height + self.space_params.tile_height // 2
        self.ghost_house_exit = ghost_house_exit[0] * self.space_params.tile_width - self.space_params.tile_width // 2, \
                                ghost_house_exit[1] * self.space_params.tile_height + self.space_params.tile_height // 2

    def is_in_house(self):
        x = self.location_x // self.space_params.tile_width
        y = self.location_y // self.space_params.tile_height
        return GHOST_HOUSE_COORDINATES_X[0] <= x <= GHOST_HOUSE_COORDINATES_X[1] \
            and GHOST_HOUSE_COORDINATES_Y[0] <= y <= GHOST_HOUSE_COORDINATES_Y[1]

    def is_frightened(self):
        return self.condition == self.State.FRIGHTENED

    def is_eaten(self):
        return self.condition == self.State.EATEN

    def is_chasing(self):
        return self.condition == self.State.CHASE

    def set_to_chase(self):
        self.velocity = 2
        self.condition = self.State.CHASE

    def set_to_frightened(self):
        self.velocity = 1
        self.condition = self.State.FRIGHTENED

    def set_to_eaten(self):
        self.condition = self.State.EATEN
        self.velocity = 8

    def draw(self, screen):
        if self.condition == self.State.CHASE:
            screen.blit(pygame.transform.flip(self.img, True, False),
                        (self.top_left_x, self.top_left_y))
        elif self.condition == self.State.FRIGHTENED:
            screen.blit(pygame.transform.flip(self.frightened_img, True, False),
                        (self.top_left_x, self.top_left_y))
        else:  # eaten
            screen.blit(pygame.transform.flip(self.eaten_img, True, False),
                        (self.top_left_x, self.top_left_y))

    def follow_target(self, screen):
        self._check_borders_ahead()
        if self.is_eaten() and self.is_in_house():
            self.set_to_chase()

        right_distance = self.calc_distance(self.location_x + self.space_params.tile_width, self.location_y)
        left_distance = self.calc_distance(self.location_x - self.space_params.tile_width, self.location_y)
        up_distance = self.calc_distance(self.location_x, self.location_y - self.space_params.tile_height)
        down_distance = self.calc_distance(self.location_x, self.location_y + self.space_params.tile_height)

        right = right_distance, Direction.RIGHT, self.turns.right
        left = left_distance, Direction.LEFT, self.turns.left
        up = up_distance, Direction.UP, self.turns.up
        down = down_distance, Direction.DOWN, self.turns.down

        if self.direction == Direction.RIGHT:
            next_turn = self.calc_next_turn([right, up, down])
            self._move(next_turn)
        elif self.direction == Direction.LEFT:
            next_turn = self.calc_next_turn([left, up, down])
            self._move(next_turn)
        elif self.direction == Direction.UP:
            next_turn = self.calc_next_turn([right, left, up])
            self._move(next_turn)
        elif self.direction == Direction.DOWN:
            next_turn = self.calc_next_turn([right, left, down])
            self._move(next_turn)

    def calc_next_turn(self, possible_decisions):
        prioritized = sorted(possible_decisions, key=lambda x: x[0], reverse=False)
        for i in range(len(prioritized)):
            if prioritized[i][2]:
                return prioritized[i][1]

    def calc_distance(self, x, y):
        target = self.target()
        target = self._calc_tile_location(target[0], target[1])
        self_location = self._calc_tile_location(x, y)
        return math.pow((target[0] - self_location[0]), 2) + math.pow((target[1] - self_location[1]), 2)

    def _calc_tile_location(self, x, y):
        return x // self.space_params.tile_width, y // self.space_params.tile_height

    def target(self) -> Tuple:
        pass

    def _move(self, direction_command: Direction):
        self._teleport_if_board_limit_reached()
        self._align_movement_to_cell_center(direction_command)

        if self.direction == Direction.LEFT:
            if self.turns.left:
                self._move_left()
            else:
                self._snap_to_center(self.space_params.tile_width, self.space_params.tile_height)

        if self.direction == Direction.RIGHT:
            if self.turns.right:
                self._move_right()
            else:
                self._snap_to_center(self.space_params.tile_width, self.space_params.tile_height)

        if self.direction == Direction.DOWN:
            if self.turns.down:
                self._move_down()
            else:
                self._snap_to_center(self.space_params.tile_width, self.space_params.tile_height)
        if self.direction == Direction.UP:
            if self.turns.up:
                self._move_up()
            else:
                self._snap_to_center(self.space_params.tile_width, self.space_params.tile_height)

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
        if self._is_asle_ahead(i, j) or self.board[i][j] == 9:
            self.turns.up = True
        else:
            self.turns.up = False

        i = ((y - DISTANCE_FACTOR) // self.space_params.tile_height) + 1
        j = (x // self.space_params.tile_width)
        if self._is_asle_ahead(i, j) or (self.is_eaten() and self.board[i][j] == 9):
            self.turns.down = True
        else:
            self.turns.down = False

    class State(enum.Enum):
        # when a ghost is chasing pacman
        CHASE = 0
        # when a ghost is eaten by pacman
        EATEN = 1
        # when pacman ate a power pellet
        FRIGHTENED = 2
        # during this mode, a ghost does not attack pacman
        SCATTER = 3
