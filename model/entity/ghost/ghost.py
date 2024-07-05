import enum
import math
from typing import Tuple
from model.asset import Asset
from model.direction import Direction
from model.entity.entity import Entity
from model.entity.player.player import Player
from model.space_params.space_params import SpaceParams
from model.turns import Turns
from settings import *


class Ghost(Entity):

    def __init__(self, center_position: Tuple, assets: Asset, frightened_assets: list, eaten_assets: Asset,
                 blink_assets: list, player: Player,
                 turns: Turns, space_params: SpaceParams, home_corner: Tuple, ghost_house_location: Tuple,
                 ghost_house_exit: Tuple,
                 velocity=DEFAULT_VELOCITY):
        super().__init__(center_position, turns, space_params, velocity)
        # sprites
        self.assets = assets
        self.eaten_assets = eaten_assets
        self.frightened_assets = frightened_assets
        self.blink_assets = blink_assets

        # surrounding awareness
        self.player = player
        self.home_corner = self.__recalculate_to_screen_coordinates(home_corner)
        self.ghost_house_location = self.__recalculate_to_screen_coordinates(ghost_house_location)
        self.ghost_house_exit = self.__recalculate_to_screen_coordinates(ghost_house_exit)

        # initial state
        self.direction = Direction.UP
        self.state = self.State.CHASE
        self.set_to_scatter()
        self.runaway = False
        self.scatter_counter_duration = 0
        self.enable_scatter_counter = 0
        self.sprite_counter = 0
        self.sprite_index = 0

    def __recalculate_to_screen_coordinates(self, board_coordinates):
        return board_coordinates[0] * self.space_params.tile_width - self.space_params.tile_width // 2, \
               board_coordinates[1] * self.space_params.tile_height + self.space_params.tile_height // 2

    def reset_position(self):
        self.__set_to_chase()
        super().reset_position()

    def is_in_house(self):
        x = self.location_x // self.space_params.tile_width
        y = self.location_y // self.space_params.tile_height
        return GHOST_HOUSE_COORDINATES_X[0] <= x <= GHOST_HOUSE_COORDINATES_X[1] \
            and GHOST_HOUSE_COORDINATES_Y[0] <= y <= GHOST_HOUSE_COORDINATES_Y[1]

    def is_frightened(self):
        return self.state == self.State.FRIGHTENED

    def is_eaten(self):
        return self.state == self.State.EATEN

    def is_chasing(self):
        return self.state == self.State.CHASE

    def is_scatter(self):
        return self.state == self.State.SCATTER

    def set_to_chase(self):
        if not self.is_eaten():
            self.__set_to_chase()

    def __set_to_chase(self):
        self.velocity = DEFAULT_VELOCITY
        self.state = self.State.CHASE

    def set_to_frightened(self):
        if not self.is_eaten():
            self.change_direction_to_opposite()
            self.velocity = SLOW_VELOCITY
            self.state = self.State.FRIGHTENED

    def set_to_scatter(self):
        if not self.is_eaten():
            self.velocity = DEFAULT_VELOCITY
            self.state = self.State.SCATTER

    def set_to_eaten(self):
        delay = self.sfx.ghost_eaten.get_length()
        self.sfx.ghost_eaten.play()
        pygame.time.set_timer(GHOST_EATEN_EVENT, int(delay * 1000), True)
        self.state = self.State.EATEN
        self.velocity = FAST_VELOCITY

    def __calculate_sprite_index(self):
        self.sprite_counter += 1
        if self.sprite_counter % GHOST_SPRITE_FREQUENCY == 0:
            self.sprite_index = 1
        if self.sprite_counter % (len(self.assets.left) * GHOST_SPRITE_FREQUENCY) == 0:
            self.sprite_index = 0

    def render(self, screen):
        self.__calculate_sprite_index()

        if self.is_chasing() or self.is_scatter():
            if self.direction == Direction.LEFT:
                screen.blit(self.assets.left[self.sprite_index],
                            (self.top_left_x, self.top_left_y))
            elif self.direction == Direction.RIGHT:
                screen.blit(self.assets.right[self.sprite_index],
                            (self.top_left_x, self.top_left_y))
            elif self.direction == Direction.UP:
                screen.blit(self.assets.up[self.sprite_index],
                            (self.top_left_x, self.top_left_y))
            elif self.direction == Direction.DOWN:
                screen.blit(self.assets.down[self.sprite_index],
                            (self.top_left_x, self.top_left_y))

        elif self.is_frightened():
            if self.player.powerup_counter < 3 * FPS:
                screen.blit(self.blink_assets[self.sprite_index],
                            (self.top_left_x, self.top_left_y))
            else:
                screen.blit(self.frightened_assets[self.sprite_index],
                                (self.top_left_x, self.top_left_y))
        elif self.is_eaten():
            if self.direction == Direction.LEFT:
                screen.blit(self.eaten_assets.left[0],
                            (self.top_left_x, self.top_left_y))
            elif self.direction == Direction.RIGHT:
                screen.blit(self.eaten_assets.right[0],
                            (self.top_left_x, self.top_left_y))
            elif self.direction == Direction.UP:
                screen.blit(self.eaten_assets.up[0],
                            (self.top_left_x, self.top_left_y))
            elif self.direction == Direction.DOWN:
                screen.blit(self.eaten_assets.down[0],
                            (self.top_left_x, self.top_left_y))

    def change_direction_to_opposite(self):
        if self.direction == Direction.LEFT:
            self._move(Direction.RIGHT)
        elif self.direction == Direction.RIGHT:
            self._move(Direction.LEFT)
        elif self.direction == Direction.DOWN:
            self._move(Direction.UP)
        elif self.direction == Direction.UP:
            self._move(Direction.DOWN)

    def follow_target(self):
        self._check_borders_ahead()
        if self.is_eaten() and self.is_in_house():
            self.__set_to_chase()

        if self.is_scatter():
            if self.scatter_counter_duration == SCATTER_DISABLE_TRIGGER:
                self.set_to_chase()
                self.scatter_counter_duration = 0
            else:
                self.scatter_counter_duration += 1

        if self.enable_scatter_counter == SCATTER_ENABLE_TRIGGER and self.is_chasing():
            self.set_to_scatter()
            self.enable_scatter_counter = 0
        else:
            self.enable_scatter_counter += 1

        if self.is_frightened():
            self.runaway = True
        else:
            self.runaway = False

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
        prioritized = sorted(possible_decisions, key=lambda x: x[0], reverse=self.runaway)
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
