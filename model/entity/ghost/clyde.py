import pygame.draw

from model.direction import Direction
from model.entity.ghost.ghost import Ghost


class Clyde(Ghost):

    def follow_target(self, screen):

        self._check_borders_ahead()
        if self.direction == Direction.RIGHT:
            if self.target_x() > self.center_x_pos and self.turns.right:
                self._move(Direction.RIGHT)
            elif not self.turns.right:
                if self.target_y() > self.center_y_pos and self.turns.down:
                    self._move(Direction.DOWN)
                elif self.target_y() < self.center_y_pos and self.turns.up:
                    self._move(Direction.UP)
                elif self.target_x() < self.center_x_pos and self.turns.left:
                    self._move(Direction.LEFT)
                elif self.turns.down:
                    self._move(Direction.DOWN)
                elif self.turns.up:
                    self._move(Direction.UP)
                elif self.turns.left:
                    self._move(Direction.LEFT)
            elif self.turns.right:
                if self.target_y() > self.center_y_pos and self.turns.down:
                    self._move(Direction.DOWN)
                if self.target_y() < self.center_y_pos and self.turns.up:
                    self._move(Direction.UP)
                else:
                    self._move(Direction.RIGHT)
        elif self.direction == Direction.LEFT:
            if self.target_y() > self.center_y_pos and self.turns.down:
                self._move(Direction.DOWN)
            elif self.target_x() < self.center_x_pos and self.turns.left:
                self._move(Direction.LEFT)
            elif not self.turns.left:
                if self.target_y() > self.center_y_pos and self.turns.down:
                    self._move(Direction.DOWN)
                elif self.target_y() < self.center_y_pos and self.turns.up:
                    self._move(Direction.UP)
                elif self.target_x() > self.center_x_pos and self.turns.right:
                    self._move(Direction.RIGHT)
                elif self.turns.down:
                    self._move(Direction.DOWN)
                elif self.turns.up:
                    self._move(Direction.UP)
                elif self.turns.right:
                    self._move(Direction.RIGHT)
            elif self.turns.left:
                if self.target_y() > self.center_y_pos and self.turns.down:
                    self._move(Direction.DOWN)
                if self.target_y() < self.center_y_pos and self.turns.up:
                    self._move(Direction.UP)
                else:
                    self._move(Direction.LEFT)
        elif self.direction == Direction.UP:
            if self.target_x() < self.center_x_pos and self.turns.left:
                self._move(Direction.LEFT)
            elif self.target_y() < self.center_y_pos and self.turns.up:
                self.direction = Direction.UP
                self._move(Direction.UP)
            elif not self.turns.up:
                if self.target_x() > self.center_x_pos and self.turns.right:
                    self._move(Direction.RIGHT)
                elif self.target_x() < self.center_x_pos and self.turns.left:
                    self._move(Direction.LEFT)
                elif self.target_y() > self.center_y_pos and self.turns.down:
                    self._move(Direction.DOWN)
                elif self.turns.left:
                    self._move(Direction.LEFT)
                elif self.turns.down:
                    self._move(Direction.DOWN)
                elif self.turns.right:
                    self._move(Direction.RIGHT)
            elif self.turns.up:
                if self.target_x() > self.center_x_pos and self.turns.right:
                    self._move(Direction.RIGHT)
                elif self.target_x() < self.center_x_pos and self.turns.left:
                    self._move(Direction.LEFT)
                else:
                    self._move(Direction.UP)
        elif self.direction == Direction.DOWN:
            if self.target_y() > self.center_y_pos and self.turns.down:
                self._move(Direction.DOWN)
            elif not self.turns.down:
                if self.target_x() > self.center_x_pos and self.turns.right:
                    self._move(Direction.RIGHT)
                elif self.target_x() < self.center_x_pos and self.turns.left:
                    self._move(Direction.LEFT)
                elif self.target_y() < self.center_y_pos and self.turns.up:
                    self._move(Direction.UP)
                elif self.turns.up:
                    self._move(Direction.UP)
                elif self.turns.left:
                    self._move(Direction.LEFT)
                elif self.turns.right:
                    self._move(Direction.RIGHT)
            elif self.turns.down:
                if self.target_x() > self.center_x_pos and self.turns.right:
                    self._move(Direction.RIGHT)
                elif self.target_x() < self.center_x_pos and self.turns.left:
                    self._move(Direction.LEFT)
                else:
                    self._move(Direction.RIGHT)
