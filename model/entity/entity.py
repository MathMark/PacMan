from settings import SPRITE_SIZE, DISTANCE_FACTOR
from model.coordinates import Coordinates
from model.direction import Direction
from model.space_params.space_params import SpaceParams
from model.turns import Turns


class Entity:
    def __init__(self, center_position: Coordinates, turns: Turns, space_params: SpaceParams, velocity=2):
        self.velocity = velocity
        self.coordinates = center_position
        self.center_x_pos = self.coordinates.x - SPRITE_SIZE // 2
        self.center_y_pos = self.coordinates.y - SPRITE_SIZE // 2
        self.direction = Direction.LEFT
        self.turns = turns
        self.space_params = space_params
        self.board = space_params.board_definition.board

    def _move_right(self):
        self.center_x_pos += self.velocity
        self.coordinates.x += self.velocity

    def _move_left(self):
        self.center_x_pos -= self.velocity
        self.coordinates.x -= self.velocity

    def _move_up(self):
        self.center_y_pos -= self.velocity
        self.coordinates.y -= self.velocity

    def _move_down(self):
        self.center_y_pos += self.velocity
        self.coordinates.y += self.velocity

    # Checks next cell based on current entity position and direction and
    # permits or prohibits to turn in certain direction depending on obstacles ahead
    def _check_borders_ahead(self):
        i = (self.coordinates.y // self.space_params.segment_height)
        j = ((self.coordinates.x + DISTANCE_FACTOR) // self.space_params.segment_width) - 1
        if self.space_params.board_definition.check_coordinate_within(i, j) and self.board[i][j] < 3:
            self.turns.left = True
        else:
            self.turns.left = False

        i = (self.coordinates.y // self.space_params.segment_height)
        j = ((self.coordinates.x - DISTANCE_FACTOR) // self.space_params.segment_width) + 1
        if self.space_params.board_definition.check_coordinate_within(i, j) and self.board[i][j] < 3:
            self.turns.right = True
        else:
            self.turns.right = False
        i = ((self.coordinates.y + DISTANCE_FACTOR) // self.space_params.segment_height) - 1
        j = (self.coordinates.x // self.space_params.segment_width)
        if self.space_params.board_definition.check_coordinate_within(i, j) \
                and (self.board[i][j] < 3 or self.board[i][j] == 9):
            self.turns.up = True
        else:
            self.turns.up = False

        i = ((self.coordinates.y - DISTANCE_FACTOR) // self.space_params.segment_height) + 1
        j = (self.coordinates.x // self.space_params.segment_width)
        if self.space_params.board_definition.check_coordinate_within(i, j) and self.board[i][j] < 3:
            self.turns.down = True
        else:
            self.turns.down = False

    # Ensures entity moves strictly by cell centers and not blocked in corners.
    def _align_movement_to_cell_center(self, direction_command):
        if direction_command == Direction.LEFT and self.turns.left:
            if self.direction == Direction.RIGHT:
                self.direction = direction_command
            else:
                if self._is_at_center(self.space_params.segment_width, self.space_params.segment_height):
                    self.direction = direction_command
            return True
        elif direction_command == Direction.RIGHT and self.turns.right:
            if self.direction == Direction.LEFT:
                self.direction = direction_command
            else:
                if self._is_at_center(self.space_params.segment_width, self.space_params.segment_height):
                    self.direction = direction_command
            return True
        elif direction_command == Direction.UP and self.turns.up:
            if self.direction == Direction.DOWN:
                self.direction = direction_command
            else:
                if self._is_at_center(self.space_params.segment_width, self.space_params.segment_height):
                    self.direction = direction_command
            return True
        elif direction_command == Direction.DOWN and self.turns.down:
            if self.direction == Direction.UP:
                self.direction = direction_command
            else:
                if self._is_at_center(self.space_params.segment_width, self.space_params.segment_height):
                    self.direction = direction_command
            return True
        else:
            return False

    def _snap_to_center(self, cell_width, cell_height):
        self.coordinates.x = round(self.coordinates.x // cell_width) * cell_width + cell_width // 2
        self.coordinates.y = round(self.coordinates.y // cell_height) * cell_height + cell_height // 2
        self.center_x_pos = self.coordinates.x - SPRITE_SIZE // 2
        self.center_y_pos = self.coordinates.y - SPRITE_SIZE // 2

    def _is_at_center(self, cell_width, cell_height):
        return (self.coordinates.x - cell_width // 2) % cell_width < 2 and \
            (self.coordinates.y - cell_height // 2) % cell_height < 2

    def _teleport_if_board_limit_reached(self):
        i = (self.center_y_pos // self.space_params.segment_height)
        j = (self.center_x_pos // self.space_params.segment_width)
        if j >= self.space_params.board_definition.width - 1:
            self.__teleport(self.space_params.segment_width, self.center_y_pos)
        if j < 1:
            self.__teleport((self.space_params.board_definition.width - 1) * self.space_params.segment_width,
                            self.center_y_pos)
        if i >= self.space_params.board_definition.height - 1:
            self.__teleport(self.center_x_pos, self.space_params.segment_height)
        if i < 1:
            self.__teleport(self.center_x_pos,
                            (self.space_params.board_definition.height - 1) * self.space_params.segment_height)

    def __teleport(self, x, y):
        self.center_x_pos = x
        self.center_y_pos = y
        self.coordinates.x = self.center_x_pos + SPRITE_SIZE // 2
        self.coordinates.y = self.center_y_pos + SPRITE_SIZE // 2