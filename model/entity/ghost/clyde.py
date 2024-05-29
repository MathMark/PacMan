from model.direction import Direction
from model.entity.ghost.ghost import Ghost


class Clyde(Ghost):
    def move(self):
        self._check_borders_ahead()
        if self.direction == Direction.RIGHT:
            if self.target.x > self.x_pos and self.turns.right:
                self.move_(Direction.RIGHT)
            elif not self.turns.right:
                if self.target.y > self.y_pos and self.turns.down:
                    self.move_(Direction.DOWN)
                elif self.target.y < self.y_pos and self.turns.up:
                    self.move_(Direction.UP)
                elif self.target.x < self.x_pos and self.turns.left:
                    self.move_(Direction.LEFT)
                elif self.turns.down:
                    self.move_(Direction.DOWN)
                elif self.turns.up:
                    self.move_(Direction.UP)
                elif self.turns.left:
                    self.move_(Direction.LEFT)
            elif self.turns.right:
                if self.target.y > self.y_pos and self.turns.down:
                    self.move_(Direction.DOWN)
                if self.target.y < self.y_pos and self.turns.up:
                    self.move_(Direction.UP)
                else:
                    self.move_(Direction.RIGHT)
        elif self.direction == Direction.LEFT:
            if self.target.y > self.y_pos and self.turns.down:
                self.move_(Direction.DOWN)
            elif self.target.x < self.x_pos and self.turns.left:
                self.move_(Direction.LEFT)
            elif not self.turns.left:
                if self.target.y > self.y_pos and self.turns.down:
                    self.move_(Direction.DOWN)
                elif self.target.y < self.y_pos and self.turns.up:
                    self.move_(Direction.UP)
                elif self.target.x > self.x_pos and self.turns.right:
                    self.move_(Direction.RIGHT)
                elif self.turns.down:
                    self.move_(Direction.DOWN)
                elif self.turns.up:
                    self.move_(Direction.UP)
                elif self.turns.right:
                    self.move_(Direction.RIGHT)
            elif self.turns.left:
                if self.target.y > self.y_pos and self.turns.down:
                    self.move_(Direction.DOWN)
                if self.target.y < self.y_pos and self.turns.up:
                    self.move_(Direction.UP)
                else:
                    self.move_(Direction.LEFT)
        elif self.direction == Direction.UP:
            if self.target.x < self.x_pos and self.turns.left:
                self.move_(Direction.LEFT)
            elif self.target.y < self.y_pos and self.turns.up:
                self.direction = Direction.UP
                self.move_(Direction.UP)
            elif not self.turns.up:
                if self.target.x > self.x_pos and self.turns.right:
                    self.move_(Direction.RIGHT)
                elif self.target.x < self.x_pos and self.turns.left:
                    self.move_(Direction.LEFT)
                elif self.target.y > self.y_pos and self.turns.down:
                    self.move_(Direction.DOWN)
                elif self.turns.left:
                    self.move_(Direction.LEFT)
                elif self.turns.down:
                    self.move_(Direction.DOWN)
                elif self.turns.right:
                    self.move_(Direction.RIGHT)
            elif self.turns.up:
                if self.target.x > self.x_pos and self.turns.right:
                    self.move_(Direction.RIGHT)
                elif self.target.x < self.x_pos and self.turns.left:

                    self.move_(Direction.LEFT)
                else:
                    self.move_(Direction.UP)
        elif self.direction == Direction.DOWN:
            if self.target.y > self.y_pos and self.turns.down:
                self.move_(Direction.DOWN)
            elif not self.turns.down:
                if self.target.x > self.x_pos and self.turns.right:
                    self.move_(Direction.RIGHT)
                elif self.target.x < self.x_pos and self.turns.left:
                    self.move_(Direction.LEFT)
                elif self.target.y < self.y_pos and self.turns.up:
                    self.move_(Direction.UP)
                elif self.turns.up:
                    self.move_(Direction.UP)
                elif self.turns.left:
                    self.move_(Direction.LEFT)
                elif self.turns.right:
                    self.move_(Direction.RIGHT)
            elif self.turns.down:
                if self.target.x > self.x_pos and self.turns.right:
                    self.move_(Direction.RIGHT)
                elif self.target.x < self.x_pos and self.turns.left:
                    self.move_(Direction.LEFT)
                else:
                    self.move_(Direction.RIGHT)
    def move_(self, direction_command: Direction):
        self._teleport_if_board_limit_reached()
        self.__check_turns_allowed(direction_command)

        if self.direction == Direction.LEFT:
            if self.turns.left:
                self._move_left()
            else:
                self._snap_to_center(self.space_params.segment_width, self.space_params.segment_height)

        if self.direction == Direction.RIGHT:
            if self.turns.right:
                self._move_right()
            else:
                self._snap_to_center(self.space_params.segment_width, self.space_params.segment_height)

        if self.direction == Direction.DOWN:
            if self.turns.down:
                self._move_down()
            else:
                self._snap_to_center(self.space_params.segment_width, self.space_params.segment_height)
        if self.direction == Direction.UP:
            if self.turns.up:
                self._move_up()
            else:
                self._snap_to_center(self.space_params.segment_width, self.space_params.segment_height)


    def __check_turns_allowed(self, direction_command):
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
