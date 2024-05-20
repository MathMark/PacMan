import pygame
from pygame import Surface

from model.board_structure import BoardStructure
from model.direction import Direction
from model.ghost import Ghost
from model.level_config import LevelConfig
import math

from model.player import Player

PI = math.pi
SPRITE_FREQUENCY = 7
FLICK_FREQUENCY = 20
SCORE_SCREEN_OFFSET = 50

class GameEngine:

    def __init__(self, screen: Surface, level: LevelConfig, player: Player, ghosts: list[Ghost]):
        self.screen = screen
        self.level = level
        self.board_definition = level.board_definition
        self.board = self.board_definition.board
        self.board_width = self.board_definition.width
        self.board_height = self.board_definition.height
        self.segment_height = ((screen.get_height() - SCORE_SCREEN_OFFSET) // self.board_height)
        self.segment_width = (screen.get_width() // self.board_width)
        self.counter = 0
        self.flicker_counter = 0
        self.flick = True
        self.player = player
        self.ghosts = ghosts
        self.fudge_factor = 15
        self.direction_command = Direction.LEFT
        pygame.font.init()
        self.game_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.power_up_counter = 0
        self.score_coordinates = (SCORE_SCREEN_OFFSET, (self.screen.get_height() - SCORE_SCREEN_OFFSET))
        self.powerup_circle_coordinates = (250, ((self.screen.get_height() - SCORE_SCREEN_OFFSET) + 15))


    def __calculate_sprite_index(self):
        self.counter += 1
        if self.counter % SPRITE_FREQUENCY == 0:
            self.player.sprite_index += 1
        if self.counter % ((len(self.player.sprites) - 1) * SPRITE_FREQUENCY) == 0:
            self.player.sprite_index = 0

    def draw_player(self):
        self.__calc_power_up_counter()
        self.__teleport_if_board_limit_reached()
        self.__calculate_sprite_index()
        self.__check_turns_allowed()

        if self.player.direction == Direction.LEFT:
            self.player.draw_face_left(self.screen)
            if not self.__is_collision_left():
                self.player.move_left()

        if self.player.direction == Direction.RIGHT:
            self.player.draw_face_right(self.screen)
            if not self.__is_collision_right():
                self.player.move_right()

        if self.player.direction == Direction.DOWN:
            self.player.draw_face_down(self.screen)
            if not self.__is_collision_down():
                self.player.move_down()
        if self.player.direction == Direction.UP:
            self.player.draw_face_up(self.screen)
            if not self.__is_collision_up():
                self.player.move_up()
        self.__eat()

    def draw_ghosts(self):
        for ghost in self.ghosts:
            ghost.draw(self.screen)


    def __check_turns_allowed(self):
        if self.direction_command == Direction.LEFT:
            i = (self.player.center_y // self.segment_height)
            j = ((self.player.center_x - self.fudge_factor) // self.segment_width)
        elif self.direction_command == Direction.RIGHT:
            i = (self.player.center_y // self.segment_height)
            j = ((self.player.center_x + self.fudge_factor) // self.segment_width)
        elif self.direction_command == Direction.UP:
            i = ((self.player.center_y - self.fudge_factor) // self.segment_height)
            j = (self.player.center_x // self.segment_width)
        else:  # direction == DOWN
            i = ((self.player.center_y + self.fudge_factor) // self.segment_height)
            j = (self.player.center_x // self.segment_width)
        if self.board_definition.check_coordinate_within(i, j):
            if self.board[i][j] < 3:
                self.player.direction = self.direction_command
            else:
                self.direction_command = self.player.direction

    def __calc_power_up_counter(self):
        if self.player.power_up:
            if self.power_up_counter <= 0:
                self.player.power_up = False
                self.power_up_counter = 0
                self.__set_ghosts_normal()
        self.power_up_counter -= 1

    def __eat(self):
        i = (self.player.center_y // self.segment_height)
        j = (self.player.center_x // self.segment_width)
        if self.board[i][j] == BoardStructure.DOT.value:
            self.board[i][j] = 0
            self.level.score += 10
        elif self.board[i][j] == BoardStructure.BIG_DOT.value:
            self.board[i][j] = 0
            self.level.score += 50
            self.player.power_up = True
            self.power_up_counter = self.level.power_up_limit
            self.__set_ghosts_dead()

    def __set_ghosts_dead(self):
        for ghost in self.ghosts:
            ghost.set_to_dead()

    def __set_ghosts_spooked(self):
        for ghost in self.ghosts:
            ghost.set_to_spooked()

    def __set_ghosts_normal(self):
        for ghost in self.ghosts:
            ghost.set_to_normal()

    def __teleport_if_board_limit_reached(self):
        i = (self.player.position_y // self.segment_height)
        j = (self.player.position_x // self.segment_width)
        if j >= self.board_width - 1:
            self.player.teleport(self.segment_width, self.player.position_y)
        if j < 1:
            self.player.teleport((self.board_width - 1) * self.segment_width, self.player.position_y)
        if i >= self.board_height - 1:
            self.player.teleport(self.player.position_x, self.segment_height)
        if i < 1:
            self.player.teleport(self.player.position_x, (self.board_height - 1) * self.segment_height)

    def __is_collision_down(self):
        # a bit below player center coordinate
        coordinate_x = (self.player.center_y + self.fudge_factor) // self.segment_height
        coordinate_y = self.player.center_x // self.segment_width
        return self.board[coordinate_x][coordinate_y] >= 3

    def __is_collision_up(self):
        # a bit upper player center coordinate
        coordinate_x = (self.player.center_y - self.fudge_factor) // self.segment_height
        coordinate_y = self.player.center_x // self.segment_width
        return self.board[coordinate_x][coordinate_y] >= 3

    def __is_collision_left(self):
        coordinate_x = self.player.center_y // self.segment_height
        coordinate_y = (self.player.center_x - self.fudge_factor) // self.segment_width
        return self.board[coordinate_x][coordinate_y] >= 3

    def __is_collision_right(self):
        coordinate_x = self.player.center_y // self.segment_height
        coordinate_y = (self.player.center_x + self.fudge_factor) // self.segment_width
        if self.board_definition.check_coordinate_within(coordinate_x, coordinate_y):
            return self.board[coordinate_x][coordinate_y] >= 3
        return False

    def __calculate_flick(self):
        self.flicker_counter += 1
        if self.flicker_counter % FLICK_FREQUENCY == 0:
            self.flick = not self.flick
        if self.flicker_counter == FLICK_FREQUENCY * 2:
            self.flicker_counter = 0

    def draw_misc(self):
        score_text = self.game_font.render(f'Score: {self.level.score}', True, 'white')
        self.screen.blit(score_text, self.score_coordinates)
        if self.player.power_up:
            pygame.draw.circle(self.screen, 'blue', self.powerup_circle_coordinates, 15)
        for i in range(self.player.lives):
            self.screen.blit(pygame.transform.scale(self.player.sprites[0], (30, 30)),
                             (((self.screen.get_width() // 2) + (self.screen.get_width() // 4)) + i * 40,
                              self.screen.get_height() - SCORE_SCREEN_OFFSET))

    def draw_level(self, level_config: LevelConfig):
        self.__calculate_flick()
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == BoardStructure.DOT.value:
                    center = (
                        j * self.segment_width + (0.5 * self.segment_width),
                        i * self.segment_height + (0.5 * self.segment_height))
                    pygame.draw.circle(self.screen, level_config.gate_color, center, 4)
                if self.board[i][j] == BoardStructure.BIG_DOT.value and not self.flick:
                    center = (
                        j * self.segment_width + (0.5 * self.segment_width),
                        i * self.segment_height + (0.5 * self.segment_height))
                    pygame.draw.circle(self.screen, level_config.gate_color, center, 10)
                if self.board[i][j] == BoardStructure.VERTICAL_WALL.value:
                    pygame.draw.line(self.screen, level_config.wall_color,
                                     (j * self.segment_width + (0.5 * self.segment_width), i * self.segment_height),
                                     (j * self.segment_width + (0.5 * self.segment_width),
                                      i * self.segment_height + self.segment_height), 3)
                if self.board[i][j] == BoardStructure.HORIZONTAL_WALL.value:
                    pygame.draw.line(self.screen, level_config.wall_color,
                                     (j * self.segment_width, i * self.segment_height + (0.5 * self.segment_height)),
                                     (j * self.segment_width + self.segment_width,
                                      i * self.segment_height + (0.5 * self.segment_height)), 3)
                if self.board[i][j] == BoardStructure.TOP_RIGHT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * self.segment_width - (self.segment_width * 0.4)) - 2,
                                     (i * self.segment_height + (0.5 * self.segment_height)), self.segment_width,
                                     self.segment_height],
                                    0, PI / 2, 3)
                if self.board[i][j] == BoardStructure.TOP_LEFT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * self.segment_width + (self.segment_width * 0.5)),
                                     (i * self.segment_height + (0.5 * self.segment_height)),
                                     self.segment_width, self.segment_height], PI / 2, PI,
                                    3)
                if self.board[i][j] == BoardStructure.BOTTOM_LEFT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * self.segment_width + (self.segment_width * 0.5)),
                                     (i * self.segment_height - (0.4 * self.segment_height)),
                                     self.segment_width, self.segment_height], PI,
                                    3 * PI / 2, 3)
                if self.board[i][j] == BoardStructure.BOTTOM_RIGHT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * self.segment_width - (self.segment_width * 0.4)) - 2,
                                     (i * self.segment_height - (0.4 * self.segment_height)), self.segment_width,
                                     self.segment_height],
                                    3 * PI / 2,
                                    2 * PI, 3)
                if self.board[i][j] == BoardStructure.GATE.value:
                    pygame.draw.line(self.screen, level_config.gate_color,
                                     (j * self.segment_width, i * self.segment_height + (0.5 * self.segment_height)),
                                     (j * self.segment_width + self.segment_width,
                                      i * self.segment_height + (0.5 * self.segment_height)), 3)
