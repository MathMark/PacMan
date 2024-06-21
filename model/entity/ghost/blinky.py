from model.entity.ghost.ghost import Ghost


class Blinky(Ghost):

    def target(self):
        if self.is_in_house():
            return self.ghost_house_exit
        else:
            if self.is_chasing() or self.is_frightened():
                return self.player.location_x, self.player.location_y
            elif self.is_eaten():
                return self.ghost_house_location
            elif self.is_scatter():
                return self.home_corner







