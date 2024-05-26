import pygame

from model.board_structure import BoardStructure
from model.coordinates import Coordinates
from model.direction import Direction
from model.eaten_object import EatenObject
from model.entity.entity import Entity
from model.space_params.space_params import SpaceParams
from model.turns import Turns

PLAYER_SPRITE_SIZE = 45
SPRITE_FREQUENCY = 7


class Player(Entity):
    def __init__(self, sprites: list, center_position: Coordinates, turns: Turns, space_params: SpaceParams, velocity=2,
                 lives=3):
        super().__init__(center_position, turns, space_params, velocity)
        self.sprites = sprites
        self.sprite_index = 0
        self.velocity = velocity
        self.direction = Direction.LEFT
        self.power_up = False
        self.lives = lives
        self.sprite_counter = 0

    def eat(self):
        i = (self.coordinates.y // self.space_params.segment_height)
        j = (self.coordinates.x // self.space_params.segment_width)
        if self.board[i][j] == BoardStructure.DOT.value:
            self.board[i][j] = 0
            return EatenObject.DOT
        elif self.board[i][j] == BoardStructure.BIG_DOT.value:
            self.board[i][j] = 0
            self.power_up = True
            return EatenObject.BIG_DOT
        return EatenObject.NOTHING

    def move(self, screen, direction_command: Direction):
        self._check_borders_ahead()
        self.__calculate_sprite_index()
        self._teleport_if_board_limit_reached()

        turned = self.__check_turns_allowed(direction_command)

        if self.direction == Direction.LEFT:
            self.__draw_face_left(screen)
            if self.turns.left:
                self._move_left()
            else:
                self._snap_to_center(self.space_params.segment_width, self.space_params.segment_height)

        if self.direction == Direction.RIGHT:
            self.__draw_face_right(screen)
            if self.turns.right:
                self._move_right()
            else:
                self._snap_to_center(self.space_params.segment_width, self.space_params.segment_height)

        if self.direction == Direction.DOWN:
            self.__draw_face_down(screen)
            if self.turns.down:
                self._move_down()
            else:
                self._snap_to_center(self.space_params.segment_width, self.space_params.segment_height)
        if self.direction == Direction.UP:
            self.__draw_face_up(screen)
            if self.turns.up:
                self._move_up()
            else:
                self._snap_to_center(self.space_params.segment_width, self.space_params.segment_height)
        return turned

    def __calculate_sprite_index(self):
        self.sprite_counter += 1
        if self.sprite_counter % SPRITE_FREQUENCY == 0:
            self.sprite_index += 1
        if self.sprite_counter % ((len(self.sprites) - 1) * SPRITE_FREQUENCY) == 0:
            self.sprite_index = 0

    def __draw_face_left(self, screen):
        screen.blit(pygame.transform.flip(self.sprites[self.sprite_index], True, False),
                    (self.x_pos, self.y_pos))

    def __draw_face_right(self, screen):
        screen.blit(self.sprites[self.sprite_index],
                    (self.x_pos, self.y_pos))

    def __draw_face_down(self, screen):
        screen.blit(pygame.transform.rotate(self.sprites[self.sprite_index], 270),
                    (self.x_pos, self.y_pos))

    def __draw_face_up(self, screen):
        screen.blit(pygame.transform.rotate(self.sprites[self.sprite_index], 90),
                    (self.x_pos, self.y_pos))

    def __check_turns_allowed(self, direction_command):
        if direction_command == Direction.LEFT and self.turns.left:
            if self.direction == Direction.RIGHT:
                self.direction = direction_command
            else:
                if self._is_at_center(self.space_params.segment_width, self.space_params.segment_height):
                    self.direction = direction_command
            return True
        elif direction_command == Direction.RIGHT and self.turns.right:
            if self.direction == Direction.LEFT:
                self.direction = direction_command
            else:
                if self._is_at_center(self.space_params.segment_width, self.space_params.segment_height):
                    self.direction = direction_command
            return True
        elif direction_command == Direction.UP and self.turns.up:
            if self.direction == Direction.DOWN:
                self.direction = direction_command
            else:
                if self._is_at_center(self.space_params.segment_width, self.space_params.segment_height):
                    self.direction = direction_command
            return True
        elif direction_command == Direction.DOWN and self.turns.down:
            if self.direction == Direction.UP:
                self.direction = direction_command
            else:
                if self._is_at_center(self.space_params.segment_width, self.space_params.segment_height):
                    self.direction = direction_command
            return True
        else:
            return False


