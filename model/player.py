from typing import Tuple

import pygame

from model.coordinates import Coordinates
from model.direction import Direction

PLAYER_SPRITE_SIZE = 45


class Player:
    def __init__(self, sprites: list, center_position: Coordinates, velocity=2, lives=3):
        self.sprites = sprites
        self.sprite_index = 0
        self.velocity = velocity
        self.coordinates = center_position
        self.position_x = self.coordinates.x - PLAYER_SPRITE_SIZE // 2
        self.position_y = self.coordinates.y - PLAYER_SPRITE_SIZE // 2
        self.direction = Direction.LEFT
        self.power_up = False
        self.lives = lives

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
