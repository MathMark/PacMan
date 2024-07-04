import pygame
from pygame import Surface
from model.board_structure import BoardStructure
from model.direction import Direction
from model.eaten_object import EatenObject
from model.entity.ghost.blinky import Blinky
from model.entity.ghost.clyde import Clyde
from model.entity.ghost.ghost import Ghost
from model.entity.ghost.inky import Inky
from model.entity.ghost.pinky import Pinky
from model.level_config import LevelConfig
import math

from model.entity.player.player import Player
from settings import *

PI = math.pi

FLICK_FREQUENCY = 20
SCORE_SCREEN_OFFSET = 50

GHOST_EATEN_EVENT = pygame.USEREVENT + 1

class GameEngine:

    def __init__(self, screen: Surface, level: LevelConfig, player: Player, ghosts: list[Ghost]):
        self.screen = screen
        self.level = level
        self.board_definition = level.board_definition
        self.board = self.board_definition.board
        self.board_width = self.board_definition.width
        self.board_height = self.board_definition.height
        self.tile_height = ((screen.get_height() - SCORE_SCREEN_OFFSET) // self.board_height)
        self.tile_width = (screen.get_width() // self.board_width)
        self.flicker_counter = 0
        self.flick = True
        self.player = player
        self.ghosts = ghosts
        self.direction_command = Direction.LEFT
        self.game_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.score_coordinates = (SCORE_SCREEN_OFFSET, (self.screen.get_height() - SCORE_SCREEN_OFFSET))
        self.powerup_circle_coordinates = (250, ((self.screen.get_height() - SCORE_SCREEN_OFFSET) + 15))
        self.pause = False
        self.start_counter = 0
        self.game_over = False

    def show_game_over(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 40)
        title = font.render('Game Over', True, 'red')
        restart_button = font.render('Hit Space to restart', True, (255, 255, 255))
        self.screen.blit(title, (
            self.screen.get_width() / 2 - title.get_width() / 2, self.screen.get_height() / 2 - title.get_height() / 3))
        self.screen.blit(restart_button, (self.screen.get_width() / 2 - restart_button.get_width() / 2,
                                          self.screen.get_height() / 1.9 + restart_button.get_height()))

        self.screen.blit(self.ghosts[0].assets.right[0],
                         (self.screen.get_width() / 2, self.screen.get_height() / 2 + self.screen.get_height() / 6))
        self.screen.blit(self.ghosts[1].assets.right[0],
                         (self.screen.get_width() / 2 - self.screen.get_width() / 8,
                          self.screen.get_height() / 2 + self.screen.get_height() / 6))
        self.screen.blit(self.ghosts[2].assets.right[0],
                         (self.screen.get_width() / 2 - self.screen.get_width() / 16,
                          self.screen.get_height() / 2 + self.screen.get_height() / 6))
        self.screen.blit(self.ghosts[3].assets.right[0],
                         (self.screen.get_width() / 2 + self.screen.get_width() / 16,
                          self.screen.get_height() / 2 + self.screen.get_height() / 6))

    def tick(self):
        if self.player.lives == -1:
            self.game_over = True
            self.show_game_over()
        else:
            self.render_level()
            self.draw_misc()
            self.render_ghosts()
            if self.player.is_ready():
                self.reset_ghosts()
                self.render_ready_text()
                self.render_player()
                self.start_counter += 1
                if self.start_counter == START_TRIGGER:
                    self.player.set_to_chase()
                    self.start_counter = 0
            elif self.player.is_chasing():
                self.render_player()
                self.move_player()
                self.move_ghosts()
                self.check_ghosts_and_player_collision()
            elif self.player.is_eaten():
                self.player.play_death_animation(self.screen)
            if DEBUG:
                self.debug()

    def check_ghosts_and_player_collision(self):
        for ghost in self.ghosts:
            if (abs(ghost.location_x - self.player.location_x) < DISTANCE_FACTOR) \
                    and (abs(ghost.location_y - self.player.location_y) < DISTANCE_FACTOR):
                if ghost.is_frightened():
                    self.level.score += 50 * self.player.score_multiplier
                    self.player.score_multiplier += 1
                    ghost.set_to_eaten()
                elif ghost.is_chasing() or ghost.is_scatter():
                    pygame.time.wait(500)
                    pygame.time.set_timer(PLAYER_EATEN_EVENT, 1, True)
                    self.player.set_to_eaten()

    def play_ghost_runsaway_sound(self):
        self.player.sfx.retreating.play()

    def play_player_eaten_sound(self):
        self.player.sfx.pacman_death.play()

    def render_player(self):
        self.player.render(self.screen)

    def move_player(self):
        turned = self.player.move(self.screen, self.direction_command)
        if not turned:
            self.direction_command = self.player.direction
        eaten = self.player.eat()
        if eaten == EatenObject.DOT:
            self.level.score += 10
        elif eaten == EatenObject.BIG_DOT:
            self.level.score += 50
            self.player.powerup_counter = self.level.power_up_limit
            self.__set_ghosts_state('frightened')
        if not self.player.powerup:
            self.__set_ghosts_state('chase')

    def render_ghosts(self):
        for ghost in self.ghosts:
            ghost.render(self.screen)

    def move_ghosts(self):
        for ghost in self.ghosts:
            ghost.follow_target()

    def reset_ghosts(self):
        for ghost in self.ghosts:
            ghost.reset_position()

    def __set_ghosts_state(self, state: str):
        for ghost in self.ghosts:
            if state == 'frightened':
                ghost.set_to_frightened()
            elif state == 'eaten':
                ghost.set_to_eaten()
            elif state == 'scatter':
                ghost.set_to_scatter()
            elif state == 'chase':
                ghost.set_to_chase()

    def __calculate_flick(self):
        self.flicker_counter += 1
        if self.flicker_counter % FLICK_FREQUENCY == 0:
            self.flick = not self.flick
        if self.flicker_counter == FLICK_FREQUENCY * 2:
            self.flicker_counter = 0

    def draw_misc(self):
        score_text = self.game_font.render(f'Score: {self.level.score}', True, 'white')
        self.screen.blit(score_text, self.score_coordinates)

        if self.player.powerup:
            pygame.draw.circle(self.screen, 'blue', self.powerup_circle_coordinates, 15)
        for i in range(self.player.lives):
            self.screen.blit(pygame.transform.scale(self.player.sprites[1], (30, 30)),
                             (((self.screen.get_width() // 2) + (self.screen.get_width() // 4)) + i * 40,
                              self.screen.get_height() - SCORE_SCREEN_OFFSET))

    def render_ready_text(self):
        ready_text = self.game_font.render(f'READY!', True, 'yellow')
        self.screen.blit(ready_text, (self.screen.get_width() // 2 - 50, self.screen.get_height() // 2))

    def render_level(self):
        self.__calculate_flick()
        for i, row in enumerate(self.board):
            for j, cell in enumerate(self.board[i]):
                x, y = j * self.tile_width, i * self.tile_height
                center = (x + self.tile_width / 2, y + self.tile_height / 2)
                if cell == BoardStructure.DOT.value:
                    pygame.draw.circle(self.screen, self.level.gate_color, center, 4)
                elif cell == BoardStructure.BIG_DOT.value and not self.flick:
                    pygame.draw.circle(self.screen, self.level.gate_color, center, 10)
                elif cell == BoardStructure.VERTICAL_WALL.value:
                    pygame.draw.line(self.screen, self.level.wall_color, (x + self.tile_width / 2, y),
                                     (x + self.tile_width / 2, y + self.tile_height), 3)
                elif cell == BoardStructure.HORIZONTAL_WALL.value:
                    pygame.draw.line(self.screen, self.level.wall_color, (x, y + self.tile_height / 2),
                                     (x + self.tile_width, y + self.tile_height / 2), 3)
                elif cell == BoardStructure.TOP_RIGHT_CORNER.value:
                    pygame.draw.arc(self.screen, self.level.wall_color,
                                    [(j * self.tile_width - (self.tile_width * 0.4)) - 2,
                                     (i * self.tile_height + (0.5 * self.tile_height)), self.tile_width,
                                     self.tile_height],
                                    0, PI / 2, 3)
                elif cell == BoardStructure.TOP_LEFT_CORNER.value:
                    pygame.draw.arc(self.screen, self.level.wall_color,
                                    [(j * self.tile_width + (self.tile_width * 0.5)),
                                     (i * self.tile_height + (0.5 * self.tile_height)),
                                     self.tile_width, self.tile_height], PI / 2, PI,
                                    3)
                elif cell == BoardStructure.BOTTOM_LEFT_CORNER.value:
                    pygame.draw.arc(self.screen, self.level.wall_color,
                                    [(j * self.tile_width + (self.tile_width * 0.5)),
                                     (i * self.tile_height - (0.4 * self.tile_height)),
                                     self.tile_width, self.tile_height], PI,
                                    3 * PI / 2, 3)
                elif cell == BoardStructure.BOTTOM_RIGHT_CORNER.value:
                    pygame.draw.arc(self.screen, self.level.wall_color,
                                    [(j * self.tile_width - (self.tile_width * 0.4)) - 2,
                                     (i * self.tile_height - (0.4 * self.tile_height)), self.tile_width,
                                     self.tile_height],
                                    3 * PI / 2,
                                    2 * PI, 3)
                elif cell == BoardStructure.GATE.value:
                    pygame.draw.line(self.screen, self.level.gate_color,
                                     (j * self.tile_width, i * self.tile_height + (0.5 * self.tile_height)),
                                     (j * self.tile_width + self.tile_width,
                                      i * self.tile_height + (0.5 * self.tile_height)), 3)

    def debug(self):
        self.debug_grid()
        self.debug_ghost_targets()

    def debug_ghost_targets(self):
        for ghost in self.ghosts:
            if isinstance(ghost, Blinky):
                pygame.draw.circle(self.screen, 'red', ghost.target(), 8)
            elif isinstance(ghost, Pinky):
                pygame.draw.circle(self.screen, 'pink', ghost.target(), 8)
            elif isinstance(ghost, Inky):
                pygame.draw.circle(self.screen, 'blue', ghost.target(), 8)
            elif isinstance(ghost, Clyde):
                pygame.draw.circle(self.screen, 'yellow', ghost.target(), 8)

    def debug_grid(self):
        # Draw additional grid to easily control object movements
        for i in range(self.board_definition.width):
            pygame.draw.line(self.screen, 'green',
                             (i * self.tile_width, 0),
                             (i * self.tile_width, self.board_definition.height * self.tile_height), 1)
        for j in range(self.board_definition.height):
            pygame.draw.line(self.screen, 'green',
                             (0, j * self.tile_height),
                             (self.board_definition.width * self.tile_width, j * self.tile_height), 1)
