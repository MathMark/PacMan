import pygame
from pygame import Surface

from model.board_structure import BoardStructure
from model.direction import Direction
from model.eaten_object import EatenObject
from model.ghost.ghost import Ghost
from model.level_config import LevelConfig
import math

from model.player import Player

PI = math.pi

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
        self.flicker_counter = 0
        self.flick = True
        self.player = player
        self.ghosts = ghosts
        self.distance_factor = 10
        self.direction_command = Direction.LEFT
        pygame.font.init()
        self.game_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.power_up_counter = 0
        self.score_coordinates = (SCORE_SCREEN_OFFSET, (self.screen.get_height() - SCORE_SCREEN_OFFSET))
        self.powerup_circle_coordinates = (250, ((self.screen.get_height() - SCORE_SCREEN_OFFSET) + 15))

        self.pause = False

    def tick(self):
        self.draw_level()
        self.draw_player()
        self.draw_ghosts()
        self.draw_misc()
        self.__o()

    def __o(self):
        for ghost in self.ghosts:
            if (abs(ghost.center_x - self.player.coordinates.x) < self.distance_factor) \
                    and (abs(ghost.center_y - self.player.coordinates.y) < self.distance_factor):
                if ghost.is_frightened():
                    ghost.set_to_eaten()
                elif ghost.is_chasing():
                    self.player.lives = self.player.lives - 1

    def draw_player(self):
        self.__calc_power_up_counter()
        turned = self.player.move(self.screen, self.direction_command)
        if not turned:
            self.direction_command = self.player.direction
        eaten = self.player.eat()
        if eaten == EatenObject.DOT:
            self.level.score += 10
        elif eaten == EatenObject.BIG_DOT:
            self.level.score += 50
            self.power_up_counter = self.level.power_up_limit
            self.__set_ghosts_frightened()

    def draw_ghosts(self):
        for ghost in self.ghosts:
            ghost.draw(self.screen)
            ghost.move()

    def __calc_power_up_counter(self):
        if self.player.power_up:
            if self.power_up_counter <= 0:
                self.player.power_up = False
                self.power_up_counter = 0
                self.__set_ghosts_to_chase()
        self.power_up_counter -= 1

    def __set_ghosts_frightened(self):
        for ghost in self.ghosts:
            ghost.set_to_frightened()

    def __set_ghosts_eaten(self):
        for ghost in self.ghosts:
            ghost.set_to_eaten()

    def __set_ghosts_to_chase(self):
        for ghost in self.ghosts:
            ghost.set_to_chase(self.player.coordinates)

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

    def draw_level(self):
        self.__calculate_flick()
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == BoardStructure.DOT.value:
                    center = (
                        j * self.segment_width + (0.5 * self.segment_width),
                        i * self.segment_height + (0.5 * self.segment_height))
                    pygame.draw.circle(self.screen, self.level.gate_color, center, 4)
                if self.board[i][j] == BoardStructure.BIG_DOT.value and not self.flick:
                    center = (
                        j * self.segment_width + (0.5 * self.segment_width),
                        i * self.segment_height + (0.5 * self.segment_height))
                    pygame.draw.circle(self.screen, self.level.gate_color, center, 10)
                if self.board[i][j] == BoardStructure.VERTICAL_WALL.value:
                    pygame.draw.line(self.screen, self.level.wall_color,
                                     (j * self.segment_width + (0.5 * self.segment_width), i * self.segment_height),
                                     (j * self.segment_width + (0.5 * self.segment_width),
                                      i * self.segment_height + self.segment_height), 3)
                if self.board[i][j] == BoardStructure.HORIZONTAL_WALL.value:
                    pygame.draw.line(self.screen, self.level.wall_color,
                                     (j * self.segment_width, i * self.segment_height + (0.5 * self.segment_height)),
                                     (j * self.segment_width + self.segment_width,
                                      i * self.segment_height + (0.5 * self.segment_height)), 3)
                if self.board[i][j] == BoardStructure.TOP_RIGHT_CORNER.value:
                    pygame.draw.arc(self.screen, self.level.wall_color,
                                    [(j * self.segment_width - (self.segment_width * 0.4)) - 2,
                                     (i * self.segment_height + (0.5 * self.segment_height)), self.segment_width,
                                     self.segment_height],
                                    0, PI / 2, 3)
                if self.board[i][j] == BoardStructure.TOP_LEFT_CORNER.value:
                    pygame.draw.arc(self.screen, self.level.wall_color,
                                    [(j * self.segment_width + (self.segment_width * 0.5)),
                                     (i * self.segment_height + (0.5 * self.segment_height)),
                                     self.segment_width, self.segment_height], PI / 2, PI,
                                    3)
                if self.board[i][j] == BoardStructure.BOTTOM_LEFT_CORNER.value:
                    pygame.draw.arc(self.screen, self.level.wall_color,
                                    [(j * self.segment_width + (self.segment_width * 0.5)),
                                     (i * self.segment_height - (0.4 * self.segment_height)),
                                     self.segment_width, self.segment_height], PI,
                                    3 * PI / 2, 3)
                if self.board[i][j] == BoardStructure.BOTTOM_RIGHT_CORNER.value:
                    pygame.draw.arc(self.screen, self.level.wall_color,
                                    [(j * self.segment_width - (self.segment_width * 0.4)) - 2,
                                     (i * self.segment_height - (0.4 * self.segment_height)), self.segment_width,
                                     self.segment_height],
                                    3 * PI / 2,
                                    2 * PI, 3)
                if self.board[i][j] == BoardStructure.GATE.value:
                    pygame.draw.line(self.screen, self.level.gate_color,
                                     (j * self.segment_width, i * self.segment_height + (0.5 * self.segment_height)),
                                     (j * self.segment_width + self.segment_width,
                                      i * self.segment_height + (0.5 * self.segment_height)), 3)

    # Draw additional grid to easily control object movements
    def debug(self):
        for i in range(self.board_definition.width):
            pygame.draw.line(self.screen, 'green',
                             (i * self.segment_width, 0),
                             (i * self.segment_width, self.board_definition.height * self.segment_height), 2)
        for j in range(self.board_definition.height):
            pygame.draw.line(self.screen, 'green',
                             (0, j * self.segment_height),
                             (self.board_definition.width * self.segment_width, j * self.segment_height), 2)
