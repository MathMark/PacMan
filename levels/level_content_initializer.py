import pygame
from pygame import Surface

from draw.game_engine import SCORE_SCREEN_OFFSET, GameEngine
from model.coordinates import Coordinates
from model.entity.ghost.clyde import Clyde
from model.entity.ghost.ghost import GHOST_SPRITE_SIZE, Ghost
from model.level_config import LevelConfig
from model.entity.player.player import PLAYER_SPRITE_SIZE, Player
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
        initial_position = Coordinates(player_position[0] * self.segment_width + (self.segment_width // 2),
                                       player_position[1] * self.segment_height + (self.segment_height // 2))
        for i in range(1, 5):
            player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'),
                                                        (PLAYER_SPRITE_SIZE, PLAYER_SPRITE_SIZE)))
        space_params = SpaceParams(self.level.board_definition, self.segment_width, self.segment_height, 21)
        return Player(player_images, initial_position, Turns(), space_params)

    def __load_ghosts(self, target: Coordinates):
        blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), GHOST_SPRITE_SIZE)
        pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), GHOST_SPRITE_SIZE)
        inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), GHOST_SPRITE_SIZE)
        clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), GHOST_SPRITE_SIZE)
        frightened_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/frightened.png'),
                                                GHOST_SPRITE_SIZE)
        eaten_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/eaten.png'), GHOST_SPRITE_SIZE)

        turns = Turns()
        space_params = SpaceParams(self.level.board_definition, self.segment_width, self.segment_height, 21)
        blinky_position = self.level.initial_positions.blinky_position
        pinky_position = self.level.initial_positions.pinky_position
        inky_position = self.level.initial_positions.inky_position
        clyde_position = self.level.initial_positions.clyde_position
        blinky = Ghost(center_position=Coordinates(blinky_position[0] * self.segment_width + (self.segment_width // 2),
                                                   blinky_position[1] * self.segment_height + (
                                                               self.segment_height // 2)),
                       img=blinky_img, frightened_img=frightened_img, eaten_img=eaten_img,
                       target=target, turns=turns, space_params=space_params, home_corner=Coordinates(5, 5))
        pinky = Ghost(center_position=Coordinates(pinky_position[0] * self.segment_width + (self.segment_width // 2),
                                                  pinky_position[1] * self.segment_height + (
                                                          self.segment_height // 2)),
                      img=pinky_img, frightened_img=frightened_img, eaten_img=eaten_img,
                      target=target, turns=turns, space_params=space_params, home_corner=Coordinates(5, 5))
        inky = Ghost(center_position=Coordinates(inky_position[0] * self.segment_width + (self.segment_width // 2),
                                                 inky_position[1] * self.segment_height + (
                                                         self.segment_height // 2)),
                     img=inky_img, frightened_img=frightened_img, eaten_img=eaten_img,
                     target=target, turns=turns, space_params=space_params, home_corner=Coordinates(5, 5))
        clyde = Clyde(center_position=Coordinates(clyde_position[0] * self.segment_width + (self.segment_width // 2),
                                                  clyde_position[1] * self.segment_height + (
                                                          self.segment_height // 2)),
                      img=clyde_img, frightened_img=frightened_img, eaten_img=eaten_img,
                      target=target, turns=turns, space_params=space_params, home_corner=Coordinates(5, 5))

        return [blinky, pinky, inky, clyde]

    def init_game_engine(self):
        player = self.__load_player()
        ghosts = self.__load_ghosts(player.coordinates)
        return GameEngine(self.screen, self.level, player, ghosts)
