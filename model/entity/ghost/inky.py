from typing import Tuple

from model.asset import Asset
from model.direction import Direction
from model.entity.ghost.blinky import Blinky
from model.entity.ghost.ghost import Ghost
from model.entity.player.player import Player
from model.space_params.space_params import SpaceParams
from model.turns import Turns


class Inky(Ghost):

    def __init__(self, center_position: Tuple, assets: Asset, frightened_assets: list, eaten_assets: Asset,
                 blink_assets: list, player: Player, turns: Turns,
                 space_params: SpaceParams, home_corner: Tuple, ghost_house_location: Tuple, blinky: Blinky,
                 ghost_house_exit,
                 velocity=2):
        super().__init__(center_position, assets, frightened_assets, eaten_assets, blink_assets, player, turns, space_params, home_corner,
                         ghost_house_location, ghost_house_exit, velocity)
        self.blinky = blinky

    def target(self):
        if self.is_in_house():
            return self.ghost_house_exit
        else:
            if self.is_chasing() or self.is_frightened():
                middle_point = self.__calculate_middle_target_point()
                delta_x = self.blinky.location_x - middle_point[0]
                delta_y = self.blinky.location_y - middle_point[1]
                return self.blinky.location_x - (-1 * delta_x), self.blinky.location_y - (-1 * delta_y)
            elif self.is_eaten():
                return self.ghost_house_location
            elif self.is_scatter():
                return self.home_corner

    def __calculate_middle_target_point(self):
        if self.player.direction == Direction.LEFT:
            return self.player.location_x - 2 * self.space_params.tile_width, self.player.location_y
        elif self.player.direction == Direction.RIGHT:
            return self.player.location_x + 2 * self.space_params.tile_width, self.player.location_y
        elif self.player.direction == Direction.UP:
            return self.player.location_x - 2 * self.space_params.tile_width, self.player.location_y - 2 * self.space_params.tile_height
        elif self.player.direction == Direction.DOWN:
            return self.player.location_x, self.player.location_y + 2 * self.space_params.tile_height




