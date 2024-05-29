from model.direction import Direction
from model.entity.ghost.ghost import Ghost


class Clyde(Ghost):
    def follow_target(self):
        self._check_borders_ahead()
        if self.direction == Direction.RIGHT:
            if self.target.x > self.x_pos and self.turns.right:
                self.move(Direction.RIGHT)
            elif not self.turns.right:
                if self.target.y > self.y_pos and self.turns.down:
                    self.move(Direction.DOWN)
                elif self.target.y < self.y_pos and self.turns.up:
                    self.move(Direction.UP)
                elif self.target.x < self.x_pos and self.turns.left:
                    self.move(Direction.LEFT)
                elif self.turns.down:
                    self.move(Direction.DOWN)
                elif self.turns.up:
                    self.move(Direction.UP)
                elif self.turns.left:
                    self.move(Direction.LEFT)
            elif self.turns.right:
                if self.target.y > self.y_pos and self.turns.down:
                    self.move(Direction.DOWN)
                if self.target.y < self.y_pos and self.turns.up:
                    self.move(Direction.UP)
                else:
                    self.move(Direction.RIGHT)
        elif self.direction == Direction.LEFT:
            if self.target.y > self.y_pos and self.turns.down:
                self.move(Direction.DOWN)
            elif self.target.x < self.x_pos and self.turns.left:
                self.move(Direction.LEFT)
            elif not self.turns.left:
                if self.target.y > self.y_pos and self.turns.down:
                    self.move(Direction.DOWN)
                elif self.target.y < self.y_pos and self.turns.up:
                    self.move(Direction.UP)
                elif self.target.x > self.x_pos and self.turns.right:
                    self.move(Direction.RIGHT)
                elif self.turns.down:
                    self.move(Direction.DOWN)
                elif self.turns.up:
                    self.move(Direction.UP)
                elif self.turns.right:
                    self.move(Direction.RIGHT)
            elif self.turns.left:
                if self.target.y > self.y_pos and self.turns.down:
                    self.move(Direction.DOWN)
                if self.target.y < self.y_pos and self.turns.up:
                    self.move(Direction.UP)
                else:
                    self.move(Direction.LEFT)
        elif self.direction == Direction.UP:
            if self.target.x < self.x_pos and self.turns.left:
                self.move(Direction.LEFT)
            elif self.target.y < self.y_pos and self.turns.up:
                self.direction = Direction.UP
                self.move(Direction.UP)
            elif not self.turns.up:
                if self.target.x > self.x_pos and self.turns.right:
                    self.move(Direction.RIGHT)
                elif self.target.x < self.x_pos and self.turns.left:
                    self.move(Direction.LEFT)
                elif self.target.y > self.y_pos and self.turns.down:
                    self.move(Direction.DOWN)
                elif self.turns.left:
                    self.move(Direction.LEFT)
                elif self.turns.down:
                    self.move(Direction.DOWN)
                elif self.turns.right:
                    self.move(Direction.RIGHT)
            elif self.turns.up:
                if self.target.x > self.x_pos and self.turns.right:
                    self.move(Direction.RIGHT)
                elif self.target.x < self.x_pos and self.turns.left:
                    self.move(Direction.LEFT)
                else:
                    self.move(Direction.UP)
        elif self.direction == Direction.DOWN:
            if self.target.y > self.y_pos and self.turns.down:
                self.move(Direction.DOWN)
            elif not self.turns.down:
                if self.target.x > self.x_pos and self.turns.right:
                    self.move(Direction.RIGHT)
                elif self.target.x < self.x_pos and self.turns.left:
                    self.move(Direction.LEFT)
                elif self.target.y < self.y_pos and self.turns.up:
                    self.move(Direction.UP)
                elif self.turns.up:
                    self.move(Direction.UP)
                elif self.turns.left:
                    self.move(Direction.LEFT)
                elif self.turns.right:
                    self.move(Direction.RIGHT)
            elif self.turns.down:
                if self.target.x > self.x_pos and self.turns.right:
                    self.move(Direction.RIGHT)
                elif self.target.x < self.x_pos and self.turns.left:
                    self.move(Direction.LEFT)
                else:
                    self.move(Direction.RIGHT)

    def move(self, direction_command: Direction):
        self._teleport_if_board_limit_reached()
        self._align_movement_to_cell_center(direction_command)

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



