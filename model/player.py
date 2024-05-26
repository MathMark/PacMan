from typing import Tuple

import pygame

from model.coordinates import Coordinates
from model.direction import Direction
from model.turns import Turns

PLAYER_SPRITE_SIZE = 45


class Player:
    def __init__(self, sprites: list, center_position: Coordinates, turns: Turns, velocity=2, lives=3):
        self.sprites = sprites
        self.sprite_index = 0
        self.velocity = velocity
        self.coordinates = center_position
        self.position_x = self.coordinates.x - PLAYER_SPRITE_SIZE // 2
        self.position_y = self.coordinates.y - PLAYER_SPRITE_SIZE // 2
        self.direction = Direction.LEFT
        self.power_up = False
        self.lives = lives
        self.turns = turns

    def draw_face_left(self, screen):
        screen.blit(pygame.transform.flip(self.sprites[self.sprite_index], True, False),
                    (self.position_x, self.position_y))

    def draw_face_right(self, screen):
        screen.blit(self.sprites[self.sprite_index],
                    (self.position_x, self.position_y))

    def draw_face_down(self, screen):
        screen.blit(pygame.transform.rotate(self.sprites[self.sprite_index], 270),
                    (self.position_x, self.position_y))

    def draw_face_up(self, screen):
        screen.blit(pygame.transform.rotate(self.sprites[self.sprite_index], 90),
                    (self.position_x, self.position_y))

    def teleport(self, x, y):
        self.position_x = x
        self.position_y = y
        self.coordinates.x = self.position_x + PLAYER_SPRITE_SIZE // 2
        self.coordinates.y = self.position_y + PLAYER_SPRITE_SIZE // 2

    def move_right(self):
        self.position_x += self.velocity
        self.coordinates.x += self.velocity

    def move_left(self):
        self.position_x -= self.velocity
        self.coordinates.x -= self.velocity

    def move_up(self):
        self.position_y -= self.velocity
        self.coordinates.y -= self.velocity

    def move_down(self):
        self.position_y += self.velocity
        self.coordinates.y += self.velocity

    def snap_to_center(self, cell_width, cell_height):
        self.coordinates.x = round(self.coordinates.x // cell_width) * cell_width + cell_width // 2
        self.coordinates.y = round(self.coordinates.y // cell_height) * cell_height + cell_height // 2
        self.position_x = self.coordinates.x - PLAYER_SPRITE_SIZE // 2
        self.position_y = self.coordinates.y - PLAYER_SPRITE_SIZE // 2

    def is_at_center(self, cell_width, cell_height):
        return (self.coordinates.x - cell_width // 2) % cell_width == 0 and \
            (self.coordinates.y - cell_height // 2) % cell_height == 0

