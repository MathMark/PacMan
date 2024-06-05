import pygame

from model.direction import Direction
from model.entity.ghost.ghost import Ghost


class Pinky(Ghost):

    def follow_target(self, screen):
        # pinky is going to turn left or right whenever advantageous, but only up or down on collision
        target = self.target()
        pygame.draw.circle(screen, 'pink', target, 10)
        x = self.location_x
        y = self.location_y
        self._check_borders_ahead()
        if self.direction == Direction.RIGHT:
            if target[0] > x and self.turns.right:
                self._move(Direction.RIGHT)
            elif not self.turns.right:
                if target[1] > y and self.turns.down:
                    self._move(Direction.DOWN)
                elif target[1] < y and self.turns.up:
                    self._move(Direction.UP)
                elif target[0] < x and self.turns.left:
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
            if target[1] > y and self.turns.down:
                self._move(Direction.DOWN)
            elif target[0] < x and self.turns.left:
                self._move(Direction.LEFT)
            elif not self.turns.left:
                if target[0] > y and self.turns.down:
                    self._move(Direction.DOWN)
                elif target[0] < y and self.turns.up:
                    self._move(Direction.UP)
                elif target[0] > x and self.turns.right:
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
            if self.target()[0] < x and self.turns.left:
                self._move(Direction.LEFT)
            elif self.target()[0] < y and self.turns.up:
                self._move(Direction.UP)
            elif not self.turns.up:
                if target[0] > x and self.turns.right:
                    self._move(Direction.RIGHT)
                elif target[0] < x and self.turns.left:
                    self._move(Direction.LEFT)
                elif target[0] > y and self.turns.down:
                    self._move(Direction.DOWN)
                elif self.turns.left:
                    self._move(Direction.LEFT)
                elif self.turns.down:
                    self._move(Direction.DOWN)
                elif self.turns.right:
                    self._move(Direction.RIGHT)
            elif self.turns.up:
                if target[0] > x and self.turns.right:
                    self._move(Direction.RIGHT)
                elif target[0] < x and self.turns.left:
                    self._move(Direction.LEFT)
                else:
                    self._move(Direction.UP)
        elif self.direction == Direction.DOWN:
            if target[1] > y and self.turns.down:
                self._move(Direction.DOWN)
            elif not self.turns.down:
                if target[0] > x and self.turns.right:
                    self._move(Direction.RIGHT)
                elif target[0] < x and self.turns.left:
                    self._move(Direction.LEFT)
                elif target[1] < y and self.turns.up:
                    self._move(Direction.UP)
                elif self.turns.up:
                    self._move(Direction.UP)
                elif self.turns.left:
                    self._move(Direction.LEFT)
                elif self.turns.right:
                    self._move(Direction.RIGHT)
            elif self.turns.down:
                if target[0] > x and self.turns.right:
                    self._move(Direction.RIGHT)
                elif target[0] < x and self.turns.left:
                    self._move(Direction.LEFT)
                else:
                    self._move(Direction.DOWN)

    def target(self):
        if self.player.direction == Direction.LEFT:
            return self.player.location_x - 4 * self.space_params.tile_width, self.player.location_y
        elif self.player.direction == Direction.RIGHT:
            return self.player.location_x + 4 * self.space_params.tile_width, self.player.location_y
        elif self.player.direction == Direction.UP:
            return self.player.location_x - 4 * self.space_params.tile_width, self.player.location_y - 4 * self.space_params.tile_height
        elif self.player.direction == Direction.DOWN:
            return self.player.location_x, self.player.location_y + 4 * self.space_params.tile_height


