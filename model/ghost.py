import enum
from typing import Tuple

import pygame

GHOST_SPRITE_SIZE = (45, 45)


class Ghost:
    def __init__(self, init_position: Tuple, img, dead_img, spooked_img, direction, velocity=2):
        self.x_pos = init_position[0]
        self.y_pos = init_position[1]
        self.velocity = velocity
        self.img = img
        self.dead_img = dead_img
        self.spooked_img = spooked_img
        self.direction = direction
        self.condition = self.Condition.NORMAL

    def set_to_normal(self):
        self.condition = self.Condition.NORMAL

    def set_to_spooked(self):
        self.condition = self.Condition.SPOOKED

    def set_to_dead(self):
        self.condition = self.Condition.DEAD

    def draw(self, screen):
        if self.condition == self.Condition.NORMAL:
            screen.blit(pygame.transform.flip(self.img, True, False),
                        (self.x_pos, self.y_pos))
        elif self.condition == self.Condition.SPOOKED:
            screen.blit(pygame.transform.flip(self.spooked_img, True, False),
                        (self.x_pos, self.y_pos))
        else: #dead
            screen.blit(pygame.transform.flip(self.dead_img, True, False),
                        (self.x_pos, self.y_pos))


    class Condition(enum.Enum):
        NORMAL = 0
        DEAD = 1
        SPOOKED = 2


