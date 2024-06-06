import math

import pygame

from model.direction import Direction
from model.entity.ghost.ghost import Ghost


class Blinky(Ghost):

    def calc_distance(self, x, y):
        target = self.target()
        target_x = target[0]
        target_y = target[1]
        return math.pow((target_x - x), 2) + math.pow((target_y - y), 2)

    def follow_target(self, screen):
        self._check_borders_ahead()
        target = self.target()
        pygame.draw.circle(screen, 'red', target, 10)

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

    def target(self):
        return self.player.location_x, self.player.location_y

    def calc_next_turn(self, possible_decisions):
        prioritized = sorted(possible_decisions, key=lambda x: x[0], reverse=False)
        for i in range(len(prioritized)):
            if prioritized[i][2]:
                return prioritized[i][1]





