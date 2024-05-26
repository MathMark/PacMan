import enum
import pygame
from model.coordinates import Coordinates
from model.direction import Direction
from model.entity.entity import Entity
from model.space_params.space_params import SpaceParams
from model.turns import Turns

GHOST_SPRITE_SIZE = (45, 45)


class Ghost(Entity):
    def __init__(self, center_position: Coordinates, img, frightened_img, eaten_img, target: Coordinates,
                 turns: Turns, space_params: SpaceParams, home_corner: Coordinates,
                 velocity=2):
        super().__init__(center_position, turns, space_params, velocity)
        self.img = img
        self.eaten_img = eaten_img
        self.frightened_img = frightened_img
        self.direction = Direction.UP
        self.target = target
        self.condition = self.Condition.CHASE
        self.home_corner = home_corner

    def is_frightened(self):
        return self.condition == self.Condition.FRIGHTENED

    def is_eaten(self):
        return self.condition == self.Condition.EATEN

    def is_chasing(self):
        return self.condition == self.Condition.CHASE

    def set_to_chase(self, target: Coordinates):
        self.target = target
        self.condition = self.Condition.CHASE

    def set_to_frightened(self):
        self.condition = self.Condition.FRIGHTENED
        self.target = self.home_corner

    def set_to_eaten(self):
        self.condition = self.Condition.EATEN

    def draw(self, screen):
        if self.condition == self.Condition.CHASE:
            screen.blit(pygame.transform.flip(self.img, True, False),
                        (self.x_pos, self.y_pos))
        elif self.condition == self.Condition.FRIGHTENED:
            screen.blit(pygame.transform.flip(self.frightened_img, True, False),
                        (self.x_pos, self.y_pos))
        else: #eaten
            screen.blit(pygame.transform.flip(self.eaten_img, True, False),
                        (self.x_pos, self.y_pos))

    def move(self):
        pass

    class Condition(enum.Enum):
        CHASE = 0
        EATEN = 1
        FRIGHTENED = 2


