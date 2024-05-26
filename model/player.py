import pygame

from global_variables import DISTANCE_FACTOR
from model.board_structure import BoardStructure
from model.coordinates import Coordinates
from model.direction import Direction
from model.eaten_object import EatenObject
from model.space_params.space_params import SpaceParams
from model.turns import Turns

PLAYER_SPRITE_SIZE = 45
SPRITE_FREQUENCY = 7


class Player:
    def __init__(self, sprites: list, center_position: Coordinates, turns: Turns, space_params: SpaceParams, velocity=2,
                 lives=3):
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
        self.space_params = space_params
        self.board = space_params.board_definition.board
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
        self.__check_borders_ahead()
        self.__calculate_sprite_index()
        self.__teleport_if_board_limit_reached()

        turned = self.__check_turns_allowed(direction_command)

        if self.direction == Direction.LEFT:
            self.__draw_face_left(screen)
            if self.turns.left:
                self.__move_left()
            else:
                self.__snap_to_center(self.space_params.segment_width, self.space_params.segment_height)

        if self.direction == Direction.RIGHT:
            self.__draw_face_right(screen)
            if self.turns.right:
                self.__move_right()
            else:
                self.__snap_to_center(self.space_params.segment_width, self.space_params.segment_height)

        if self.direction == Direction.DOWN:
            self.__draw_face_down(screen)
            if self.turns.down:
                self.__move_down()
            else:
                self.__snap_to_center(self.space_params.segment_width, self.space_params.segment_height)
        if self.direction == Direction.UP:
            self.__draw_face_up(screen)
            if self.turns.up:
                self.__move_up()
            else:
                self.__snap_to_center(self.space_params.segment_width, self.space_params.segment_height)
        return turned

    def __calculate_sprite_index(self):
        self.sprite_counter += 1
        if self.sprite_counter % SPRITE_FREQUENCY == 0:
            self.sprite_index += 1
        if self.sprite_counter % ((len(self.sprites) - 1) * SPRITE_FREQUENCY) == 0:
            self.sprite_index = 0

    def __draw_face_left(self, screen):
        screen.blit(pygame.transform.flip(self.sprites[self.sprite_index], True, False),
                    (self.position_x, self.position_y))

    def __draw_face_right(self, screen):
        screen.blit(self.sprites[self.sprite_index],
                    (self.position_x, self.position_y))

    def __draw_face_down(self, screen):
        screen.blit(pygame.transform.rotate(self.sprites[self.sprite_index], 270),
                    (self.position_x, self.position_y))

    def __draw_face_up(self, screen):
        screen.blit(pygame.transform.rotate(self.sprites[self.sprite_index], 90),
                    (self.position_x, self.position_y))

    def __teleport(self, x, y):
        self.position_x = x
        self.position_y = y
        self.coordinates.x = self.position_x + PLAYER_SPRITE_SIZE // 2
        self.coordinates.y = self.position_y + PLAYER_SPRITE_SIZE // 2

    def __move_right(self):
        self.position_x += self.velocity
        self.coordinates.x += self.velocity

    def __move_left(self):
        self.position_x -= self.velocity
        self.coordinates.x -= self.velocity

    def __move_up(self):
        self.position_y -= self.velocity
        self.coordinates.y -= self.velocity

    def __move_down(self):
        self.position_y += self.velocity
        self.coordinates.y += self.velocity

    def __snap_to_center(self, cell_width, cell_height):
        self.coordinates.x = round(self.coordinates.x // cell_width) * cell_width + cell_width // 2
        self.coordinates.y = round(self.coordinates.y // cell_height) * cell_height + cell_height // 2
        self.position_x = self.coordinates.x - PLAYER_SPRITE_SIZE // 2
        self.position_y = self.coordinates.y - PLAYER_SPRITE_SIZE // 2

    def __is_at_center(self, cell_width, cell_height):
        return (self.coordinates.x - cell_width // 2) % cell_width < 2 and \
            (self.coordinates.y - cell_height // 2) % cell_height < 2

    def __teleport_if_board_limit_reached(self):
        i = (self.position_y // self.space_params.segment_height)
        j = (self.position_x // self.space_params.segment_width)
        if j >= self.space_params.board_definition.width - 1:
            self.__teleport(self.space_params.segment_width, self.position_y)
        if j < 1:
            self.__teleport((self.space_params.board_definition.width - 1) * self.space_params.segment_width,
                            self.position_y)
        if i >= self.space_params.board_definition.height - 1:
            self.__teleport(self.position_x, self.space_params.segment_height)
        if i < 1:
            self.__teleport(self.position_x,
                            (self.space_params.board_definition.height - 1) * self.space_params.segment_height)

    def __check_turns_allowed(self, direction_command):
        if direction_command == Direction.LEFT and self.turns.left:
            if self.direction == Direction.RIGHT:
                self.direction = direction_command
            else:
                if self.__is_at_center(self.space_params.segment_width, self.space_params.segment_height):
                    self.direction = direction_command
            return True
        elif direction_command == Direction.RIGHT and self.turns.right:
            if self.direction == Direction.LEFT:
                self.direction = direction_command
            else:
                if self.__is_at_center(self.space_params.segment_width, self.space_params.segment_height):
                    self.direction = direction_command
            return True
        elif direction_command == Direction.UP and self.turns.up:
            if self.direction == Direction.DOWN:
                self.direction = direction_command
            else:
                if self.__is_at_center(self.space_params.segment_width, self.space_params.segment_height):
                    self.direction = direction_command
            return True
        elif direction_command == Direction.DOWN and self.turns.down:
            if self.direction == Direction.UP:
                self.direction = direction_command
            else:
                if self.__is_at_center(self.space_params.segment_width, self.space_params.segment_height):
                    self.direction = direction_command
            return True
        else:
            return False

    def __check_borders_ahead(self):
        i = (self.coordinates.y // self.space_params.segment_height)
        j = ((self.coordinates.x + DISTANCE_FACTOR) // self.space_params.segment_width) - 1
        if self.space_params.board_definition.check_coordinate_within(i, j) and self.board[i][j] < 3:
            self.turns.left = True
        else:
            self.turns.left = False

        i = (self.coordinates.y // self.space_params.segment_height)
        j = ((self.coordinates.x - DISTANCE_FACTOR) // self.space_params.segment_width) + 1
        if self.space_params.board_definition.check_coordinate_within(i, j) and self.board[i][j] < 3:
            self.turns.right = True
        else:
            self.turns.right = False
        i = ((self.coordinates.y + DISTANCE_FACTOR) // self.space_params.segment_height) - 1
        j = (self.coordinates.x // self.space_params.segment_width)
        if self.space_params.board_definition.check_coordinate_within(i, j) and self.board[i][j] < 3:
            self.turns.up = True
        else:
            self.turns.up = False

        i = ((self.coordinates.y - DISTANCE_FACTOR) // self.space_params.segment_height) + 1
        j = (self.coordinates.x // self.space_params.segment_width)
        if self.space_params.board_definition.check_coordinate_within(i, j) and self.board[i][j] < 3:
            self.turns.down = True
        else:
            self.turns.down = False
