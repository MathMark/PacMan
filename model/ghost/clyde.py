from model.direction import Direction
from model.ghost.ghost import Ghost


class Clyde(Ghost):
    def move(self):
        self._teleport_if_board_limit_reached()
        self._check_collisions()
        if self.direction == Direction.RIGHT:
            if self.target.center_x > self.x_pos and self.turns.right:
                self._move_right()
            elif not self.turns.right:
                if self.target.center_y > self.y_pos and self.turns.down:
                    self.direction = Direction.DOWN
                    self._move_down()
                elif self.target.center_y < self.y_pos and self.turns.up:
                    self.direction = Direction.UP
                    self._move_up()
                elif self.target.center_x < self.x_pos and self.turns.left:
                    self.direction = Direction.LEFT
                    self._move_left()
                elif self.turns.down:
                    self.direction = Direction.DOWN
                    self._move_down()
                elif self.turns.up:
                    self.direction = Direction.UP
                    self._move_up()
                elif self.turns.left:
                    self.direction = Direction.LEFT
                    self._move_left()
            elif self.turns.right:
                if self.target.center_y > self.y_pos and self.turns.down:
                    self.direction = Direction.DOWN
                    self._move_down()
                if self.target.center_y < self.y_pos and self.turns.up:
                    self.direction = Direction.UP
                    self._move_up()
                else:
                    self._move_right()
        elif self.direction == Direction.LEFT:
            if self.target.center_y > self.y_pos and self.turns.down:
                self.direction = Direction.DOWN
            elif self.target.center_x < self.x_pos and self.turns.left:
                self._move_left()
            elif not self.turns.left:
                if self.target.center_y > self.y_pos and self.turns.down:
                    self.direction = Direction.DOWN
                    self._move_down()
                elif self.target.center_y < self.y_pos and self.turns.up:
                    self.direction = Direction.UP
                    self._move_up()
                elif self.target.center_x > self.x_pos and self.turns.right:
                    self.direction = Direction.RIGHT
                    self._move_right()
                elif self.turns.down:
                    self.direction = Direction.DOWN
                    self._move_down()
                elif self.turns.up:
                    self.direction = Direction.UP
                    self._move_up()
                elif self.turns.right:
                    self.direction = Direction.RIGHT
                    self._move_right()
            elif self.turns.left:
                if self.target.center_y > self.y_pos and self.turns.down:
                    self.direction = Direction.DOWN
                    self._move_down()
                if self.target.center_y < self.y_pos and self.turns.up:
                    self.direction = Direction.UP
                    self._move_up()
                else:
                    self._move_left()
        elif self.direction == Direction.UP:
            if self.target.center_x < self.x_pos and self.turns.left:
                self.direction = Direction.LEFT
                self._move_left()
            elif self.target.center_y < self.y_pos and self.turns.up:
                self.direction = Direction.UP
                self._move_up()
            elif not self.turns.up:
                if self.target.center_x > self.x_pos and self.turns.right:
                    self.direction = Direction.RIGHT
                    self._move_right()
                elif self.target.center_x < self.x_pos and self.turns.left:
                    self.direction = Direction.LEFT
                    self._move_left()
                elif self.target.center_y > self.y_pos and self.turns.down:
                    self.direction = Direction.DOWN
                    self._move_down()
                elif self.turns.left:
                    self.direction = Direction.LEFT
                    self._move_left()
                elif self.turns.down:
                    self.direction = Direction.DOWN
                    self._move_down()
                elif self.turns.right:
                    self.direction = Direction.RIGHT
                    self._move_right()
            elif self.turns.up:
                if self.target.center_x > self.x_pos and self.turns.right:
                    self.direction = Direction.RIGHT
                    self._move_right()
                elif self.target.center_x < self.x_pos and self.turns.left:
                    self.direction = Direction.LEFT
                    self._move_left()
                else:
                    self._move_up()
        elif self.direction == Direction.DOWN:
            if self.target.center_y > self.y_pos and self.turns.down:
                self._move_down()
            elif not self.turns.down:
                if self.target.center_x > self.x_pos and self.turns.right:
                    self.direction = Direction.RIGHT
                    self._move_right()
                elif self.target.center_x < self.x_pos and self.turns.left:
                    self.direction = Direction.LEFT
                    self._move_left()
                elif self.target.center_y < self.y_pos and self.turns.up:
                    self.direction = Direction.UP
                    self._move_up()
                elif self.turns.up:
                    self.direction = Direction.UP
                    self._move_up()
                elif self.turns.left:
                    self.direction = Direction.LEFT
                    self._move_left()
                elif self.turns.right:
                    self.direction = Direction.RIGHT
                    self._move_right()
            elif self.turns.down:
                if self.target.center_x > self.x_pos and self.turns.right:
                    self.direction = Direction.RIGHT
                    self._move_right()
                elif self.target.center_x < self.x_pos and self.turns.left:
                    self.direction = Direction.LEFT
                    self._move_left()
                else:
                    self._move_right()