from model.direction import Direction
from model.entity.ghost.ghost import Ghost


class Blinky(Ghost):

    def follow_target(self, screen):
        self._check_borders_ahead()
        if self.direction == Direction.RIGHT:
            if self.target.x > self.center_x_pos and self.turns.right:
                self._move(Direction.RIGHT)
            elif not self.turns.right:
                if self.target.y > self.center_y_pos and self.turns.down:
                    self._move(Direction.DOWN)
                elif self.target.y < self.center_y_pos and self.turns.up:
                    self._move(Direction.UP)
                elif self.target.x < self.center_x_pos and self.turns.left:
                    self._move(Direction.LEFT)
                elif self.turns.down:
                    self._move(Direction.DOWN)
                elif self.turns.up:
                    self._move(Direction.UP)
                elif self.turns.left:
                    self._move(Direction.LEFT)
            elif self.turns.right:
                self._move(Direction.RIGHT)
        elif self.direction == Direction.LEFT:
            if self.target.x < self.center_x_pos and self.turns.left:
                self._move(Direction.LEFT)
            elif not self.turns.left:
                if self.target.y > self.center_y_pos and self.turns.down:
                    self._move(Direction.DOWN)
                elif self.target.y < self.center_y_pos and self.turns.up:
                    self._move(Direction.UP)
                elif self.target.x > self.center_x_pos and self.turns.right:
                    self._move(Direction.RIGHT)
                elif self.turns.down:
                    self._move(Direction.DOWN)
                elif self.turns.up:
                    self._move(Direction.UP)
                elif self.turns.right:
                    self._move(Direction.RIGHT)
            elif self.turns.left:
                self._move(Direction.LEFT)
        elif self.direction == Direction.UP:
            if self.target.y < self.center_y_pos and self.turns.up:
                self._move(Direction.UP)
            elif not self.turns.up:
                if self.target.x > self.center_x_pos and self.turns.right:
                    self._move(Direction.RIGHT)
                elif self.target.x < self.center_x_pos and self.turns.left:
                    self._move(Direction.LEFT)
                elif self.target.y > self.center_y_pos and self.turns.down:
                    self._move(Direction.DOWN)
                elif self.turns.down:
                    self._move(Direction.DOWN)
                elif self.turns.right:
                    self._move(Direction.RIGHT)
                elif self.turns.left:
                    self._move(Direction.LEFT)
            elif self.turns.up:
                self._move(Direction.UP)
        elif self.direction == Direction.DOWN:
            if self.target.y > self.center_y_pos and self.turns.down:
                self._move(Direction.DOWN)
            elif not self.turns.down:
                if self.target.x > self.center_x_pos and self.turns.right:
                    self._move(Direction.RIGHT)
                elif self.target.x < self.center_x_pos and self.turns.left:
                    self._move(Direction.LEFT)
                elif self.target.y < self.center_y_pos and self.turns.up:
                    self._move(Direction.UP)
                elif self.turns.up:
                    self._move(Direction.UP)
                elif self.turns.right:
                    self._move(Direction.RIGHT)
                elif self.turns.left:
                    self._move(Direction.LEFT)
            elif self.turns.down:
                self._move(Direction.DOWN)

    def target(self):
        if self.player.direction == Direction.LEFT:
            return self.player.top_left_x, self.player.top_left_y
        elif self.player.direction == Direction.RIGHT:
            return self.player.top_left_x + 4 * self.space_params.tile_width, self.player.top_left_y
        elif self.player.direction == Direction.UP:
            return self.player.top_left_x - 4 * self.space_params.tile_width, self.player.top_left_y - 4 * self.space_params.tile_height
        elif self.player.direction == Direction.DOWN:
            return self.player.top_left_x, self.player.top_left_y + 4 * self.space_params.tile_height


