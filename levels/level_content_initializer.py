from typing import Tuple

import pygame
from pygame import Surface

from draw.game_engine import SCORE_SCREEN_OFFSET, GameEngine
from model.direction import Direction
from model.ghost.blinky import Blinky
from model.ghost.clyde import Clyde
from model.ghost.ghost import GHOST_SPRITE_SIZE, Ghost
from model.level_config import LevelConfig
from model.player import PLAYER_SPRITE_SIZE, Player
from model.space_params.space_params import SpaceParams
from model.turns import Turns


class LevelContentInitializer:

    def __init__(self, level: LevelConfig, screen: Surface):
        self.level = level
        self.screen = screen
        self.segment_height = ((self.screen.get_height() - SCORE_SCREEN_OFFSET) // level.board_definition.height)
        self.segment_width = (self.screen.get_width() // level.board_definition.width)
        self.player = self.__load_player()

    def __load_player(self):
        player_images = []
        player_position = self.level.initial_positions.player_postion
        initial_position = (player_position[0] * self.segment_width, player_position[1] * self.segment_height)
        for i in range(1, 5):
            player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'),
                                                        (PLAYER_SPRITE_SIZE, PLAYER_SPRITE_SIZE)))
        return Player(player_images, initial_position)

    def __load_ghosts(self, target: Player):
        blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), GHOST_SPRITE_SIZE)
        pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), GHOST_SPRITE_SIZE)
        inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), GHOST_SPRITE_SIZE)
        clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), GHOST_SPRITE_SIZE)
        spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), GHOST_SPRITE_SIZE)
        dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), GHOST_SPRITE_SIZE)

        turns = Turns()
        space_params = SpaceParams(self.level.board_definition, self.segment_width, self.segment_height, 21)
        blinky_position = self.level.initial_positions.blinky_position
        pinky_position = self.level.initial_positions.pinky_position
        inky_position = self.level.initial_positions.inky_position
        clyde_position = self.level.initial_positions.clyde_position
        blinky = Ghost((blinky_position[0] * self.segment_width, blinky_position[1] * self.segment_height), blinky_img,
                       spooked_img, dead_img, Direction.RIGHT, target, turns, space_params)
        pinky = Ghost((pinky_position[0] * self.segment_width, pinky_position[1] * self.segment_height), pinky_img,
                       spooked_img, dead_img, Direction.UP, target, turns, space_params)
        inky = Ghost((inky_position[0] * self.segment_width, inky_position[1] * self.segment_height), inky_img,
                       spooked_img, dead_img, Direction.UP, target, turns, space_params)
        clyde = Clyde((clyde_position[0] * self.segment_width, clyde_position[1] * self.segment_height), clyde_img,
                       spooked_img, dead_img, Direction.UP, target, turns, space_params)

        return [blinky, pinky, inky, clyde]

    def init_game_engine(self):
        player = self.__load_player()
        ghosts = self.__load_ghosts(player)
        return GameEngine(self.screen, self.level, player, ghosts)
