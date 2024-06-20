import math

import pygame.draw

from model.direction import Direction
from model.entity.ghost.ghost import Ghost


class Clyde(Ghost):

    def follow_target(self, screen):
        pygame.draw.circle(screen, 'yellow', self.target(), 10)
        super().follow_target(screen)

    def target(self):
        if self.is_in_house():
            return self.ghost_house_exit
        else:
            if self.is_chasing():
                player_x, player_y = self._calc_tile_location(self.player.location_x, self.player.location_y)
                mine_x, mine_y = self._calc_tile_location(self.location_x, self.location_y)
                distance = math.sqrt(math.pow((player_x - mine_x), 2) + math.pow((player_y - mine_y), 2))
                if distance <= 8:
                    return self.player.location_x, self.player.location_y
                else:
                    return 10, 10
            elif self.is_frightened():
                return self.home_corner
            elif self.is_eaten():
                return self.ghost_house_location






