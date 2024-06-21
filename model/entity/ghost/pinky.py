from model.direction import Direction
from model.entity.ghost.ghost import Ghost


class Pinky(Ghost):

    def target(self):
        if self.is_in_house():
            return self.ghost_house_exit
        else:
            if self.is_chasing() or self.is_frightened():
                if self.player.direction == Direction.LEFT:
                    return self.player.location_x - 4 * self.space_params.tile_width, self.player.location_y
                elif self.player.direction == Direction.RIGHT:
                    return self.player.location_x + 4 * self.space_params.tile_width, self.player.location_y
                elif self.player.direction == Direction.UP:
                    return self.player.location_x - 4 * self.space_params.tile_width, self.player.location_y - 4 * self.space_params.tile_height
                elif self.player.direction == Direction.DOWN:
                    return self.player.location_x, self.player.location_y + 4 * self.space_params.tile_height
            elif self.is_eaten():
                return self.ghost_house_location
            elif self.is_scatter():
                return self.home_corner


