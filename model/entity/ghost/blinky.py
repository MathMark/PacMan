from model.entity.ghost.ghost import Ghost


class Blinky(Ghost):

    def target(self):
        if self.is_chasing():
            return self.player.location_x, self.player.location_y
        if self.is_frightened():
            return self.home_corner







