from typing import Tuple

import pygame

from model.direction import Direction
from model.entity.ghost.blinky import Blinky
from model.entity.ghost.ghost import Ghost
from model.entity.player.player import Player
from model.space_params.space_params import SpaceParams
from model.turns import Turns


class Inky(Ghost):

    def __init__(self, center_position: Tuple, img, frightened_img, eaten_img, player: Player, turns: Turns,
                 space_params: SpaceParams, home_corner: Tuple, ghost_house_location: Tuple, blinky: Blinky,
                 velocity=2):
        super().__init__(center_position, img, frightened_img, eaten_img, player, turns, space_params, home_corner,
                         ghost_house_location, velocity)
        self.blinky = blinky

    def follow_target(self, screen):
        pygame.draw.circle(screen, 'blue', self.target(), 10)
        super().follow_target(screen)

    def target(self):
        if self.is_chasing():
            middle_point = self.__calculate_middle_target_point()
            delta_x = self.blinky.location_x - middle_point[0]
            delta_y = self.blinky.location_y - middle_point[1]
            return self.blinky.location_x - (-1 * delta_x), self.blinky.location_y - (-1 * delta_y)
        elif self.is_frightened():
            return self.home_corner
        elif self.is_eaten():
            return self.ghost_house_location

    def __calculate_middle_target_point(self):
        if self.player.direction == Direction.LEFT:
            return self.player.location_x - 2 * self.space_params.tile_width, self.player.location_y
        elif self.player.direction == Direction.RIGHT:
            return self.player.location_x + 2 * self.space_params.tile_width, self.player.location_y
        elif self.player.direction == Direction.UP:
            return self.player.location_x - 2 * self.space_params.tile_width, self.player.location_y - 2 * self.space_params.tile_height
        elif self.player.direction == Direction.DOWN:
            return self.player.location_x, self.player.location_y + 2 * self.space_params.tile_height




