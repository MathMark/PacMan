import pygame
from pygame import Surface

from draw.game_engine import SCORE_SCREEN_OFFSET, GameEngine
from model.entity.ghost.blinky import Blinky
from model.entity.ghost.clyde import Clyde
from model.entity.ghost.ghost import GHOST_SPRITE_SIZE, Ghost
from model.entity.ghost.pinky import Pinky
from model.level_config import LevelConfig
from model.entity.player.player import PLAYER_SPRITE_SIZE, Player
from model.space_params.space_params import SpaceParams
from model.turns import Turns
from settings import *


class LevelContentInitializer:

    def __init__(self, level: LevelConfig, screen: Surface):
        self.level = level
        self.screen = screen
        self.tile_height = ((self.screen.get_height() - SCORE_SCREEN_OFFSET) // level.board_definition.height)
        self.tile_width = (self.screen.get_width() // level.board_definition.width)
        self.player = self.__load_player()

    def __load_player(self):
        player_images = []

        initial_position = (PLAYER_X * self.tile_width + (self.tile_width // 2),
                            PLAYER_Y * self.tile_height + (self.tile_height // 2))
        for i in range(1, 5):
            player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'),
                                                        (PLAYER_SPRITE_SIZE, PLAYER_SPRITE_SIZE)))
        space_params = SpaceParams(self.level.board_definition, self.tile_width, self.tile_height, 21)
        return Player(player_images, initial_position, Turns(), space_params)

    def __load_ghosts(self, player: Player):
        blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), GHOST_SPRITE_SIZE)
        pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), GHOST_SPRITE_SIZE)
        inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), GHOST_SPRITE_SIZE)
        clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), GHOST_SPRITE_SIZE)
        frightened_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/frightened.png'), GHOST_SPRITE_SIZE)
        eaten_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/eaten.png'), GHOST_SPRITE_SIZE)

        blinky_location = (BLINKY_X * self.tile_width + self.tile_width // 2,
                           BLINKY_Y * self.tile_height + self.tile_height // 2)
        pinky_location = (PINKY_X * self.tile_width + self.tile_width // 2,
                          PINKY_Y * self.tile_height + self.tile_height // 2)
        inky_location = (INKY_X * self.tile_width + self.tile_width // 2,
                         INKY_Y * self.tile_height + self.tile_height // 2)
        clyde_location = (CLYDE_X * self.tile_width + self.tile_width // 2,
                          CLYDE_Y * self.tile_height + self.tile_height // 2)

        turns = Turns()
        space_params = SpaceParams(self.level.board_definition, self.tile_width, self.tile_height, 21)

        blinky = Blinky(center_position=blinky_location,
                        img=blinky_img, frightened_img=frightened_img, eaten_img=eaten_img,
                        player=player, turns=turns, space_params=space_params, home_corner=BLINKY_CORNER,
                        ghost_house_location=GHOST_HOUSE_LOCATION)
        pinky = Pinky(center_position=pinky_location,
                      img=pinky_img, frightened_img=frightened_img, eaten_img=eaten_img,
                      player=player, turns=turns, space_params=space_params, home_corner=PINKY_CORNER,
                      ghost_house_location=GHOST_HOUSE_LOCATION)
        inky = Ghost(center_position=inky_location,
                     img=inky_img, frightened_img=frightened_img, eaten_img=eaten_img,
                     player=player, turns=turns, space_params=space_params, home_corner=(5, 5),
                     ghost_house_location=GHOST_HOUSE_LOCATION)
        clyde = Clyde(center_position=clyde_location,
                      img=clyde_img, frightened_img=frightened_img, eaten_img=eaten_img,
                      player=player, turns=turns, space_params=space_params, home_corner=(0, 0),
                      ghost_house_location=GHOST_HOUSE_LOCATION)

        return [blinky, pinky]

    def init_game_engine(self):
        player = self.__load_player()
        ghosts = self.__load_ghosts(player)
        return GameEngine(self.screen, self.level, player, ghosts)
