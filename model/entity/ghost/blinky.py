import pygame

from model.direction import Direction
from model.entity.ghost.ghost import Ghost


class Blinky(Ghost):



    def follow_target(self, screen):
        self._check_borders_ahead()
        target = self.target()
        pygame.draw.circle(screen, 'red', target, 10)
        if self.direction == Direction.RIGHT:
            if target[0] > self.location_x and self.turns.right:
                self._move(Direction.RIGHT)
            elif not self.turns.right:
                if target[1] > self.location_y and self.turns.down:
                    self._move(Direction.DOWN)
                elif target[1] < self.location_y and self.turns.up:
                    self._move(Direction.UP)
                elif target[0] < self.location_x and self.turns.left:
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
            if target[0] < self.location_x and self.turns.left:
                self._move(Direction.LEFT)
            elif not self.turns.left:
                if target[1] > self.location_y and self.turns.down:
                    self._move(Direction.DOWN)
                elif target[1] < self.location_y and self.turns.up:
                    self._move(Direction.UP)
                elif target[0] > self.location_x and self.turns.right:
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
            if target[1] < self.location_y and self.turns.up:
                self._move(Direction.UP)
            elif not self.turns.up:
                if target[0] > self.location_x and self.turns.right:
                    self._move(Direction.RIGHT)
                elif target[0] < self.location_x and self.turns.left:
                    self._move(Direction.LEFT)
                elif target[1] > self.location_y and self.turns.down:
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
            if target[1] > self.location_y and self.turns.down:
                self._move(Direction.DOWN)
            elif not self.turns.down:
                if target[0] > self.location_x and self.turns.right:
                    self._move(Direction.RIGHT)
                elif target[0] < self.location_x and self.turns.left:
                    self._move(Direction.LEFT)
                elif target[1] < self.location_y and self.turns.up:
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
        return self.player.location_x, self.player.location_y


