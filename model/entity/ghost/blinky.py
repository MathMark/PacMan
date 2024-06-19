import pygame

from model.entity.ghost.ghost import Ghost
from settings import GHOST_HOUSE_EXIT


class Blinky(Ghost):

    def follow_target(self, screen):
        pygame.draw.circle(screen, 'red', self.target(), 10)
        super().follow_target(screen)

    def target(self):
        if self.is_in_house():
            return self.ghost_house_exit
        else:
            if self.is_chasing():
                return self.player.location_x, self.player.location_y
            elif self.is_frightened():
                return self.home_corner
            elif self.is_eaten():
                return self.ghost_house_location







