from pathlib import Path

import pygame
from pygame import Surface

from draw.game_engine import SCORE_SCREEN_OFFSET, GameEngine
from model.asset import Asset
from model.entity.ghost.blinky import Blinky
from model.entity.ghost.clyde import Clyde
from model.entity.ghost.inky import Inky
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
        blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), SPRITE_SIZE)
        pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), SPRITE_SIZE)
        inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), SPRITE_SIZE)
        clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), SPRITE_SIZE)
        frightened_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/frightened.png'),
                                                SPRITE_SIZE)
        eaten_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/eaten.png'), SPRITE_SIZE)

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
        blinky_assets, pinky_assets, inky_assets, clyde_assets = self.render_ghosts_assets()

        blinky = Blinky(center_position=blinky_location,
                        assets=blinky_assets, frightened_img=frightened_img, eaten_img=eaten_img,
                        player=player, turns=turns, space_params=space_params, home_corner=BLINKY_CORNER,
                        ghost_house_location=GHOST_HOUSE_LOCATION, ghost_house_exit=GHOST_HOUSE_EXIT)
        pinky = Pinky(center_position=pinky_location,
                      assets=pinky_assets, frightened_img=frightened_img, eaten_img=eaten_img,
                      player=player, turns=turns, space_params=space_params, home_corner=PINKY_CORNER,
                      ghost_house_location=GHOST_HOUSE_LOCATION, ghost_house_exit=GHOST_HOUSE_EXIT)
        inky = Inky(center_position=inky_location,
                    assets=inky_assets, frightened_img=frightened_img, eaten_img=eaten_img,
                    player=player, turns=turns, space_params=space_params, home_corner=INKY_CORNER,
                    blinky=blinky,
                    ghost_house_location=GHOST_HOUSE_LOCATION, ghost_house_exit=GHOST_HOUSE_EXIT)
        clyde = Clyde(center_position=clyde_location,
                      assets=clyde_assets, frightened_img=frightened_img, eaten_img=eaten_img,
                      player=player, turns=turns, space_params=space_params, home_corner=CLYDE_CORNER,
                      ghost_house_location=GHOST_HOUSE_LOCATION, ghost_house_exit=GHOST_HOUSE_EXIT)

        return [blinky, pinky, inky, clyde]

    def init_game_engine(self):
        player = self.__load_player()
        ghosts = self.__load_ghosts(player)
        return GameEngine(self.screen, self.level, player, ghosts)

    def render_ghosts_assets(self):
        blinky_folder = Path('assets/ghost_images/blinky')
        pinky_folder = Path('assets/ghost_images/pinky')
        inky_folder = Path('assets/ghost_images/inky')
        clyde_folder = Path('assets/ghost_images/clyde')

        blinky_assets = Asset(
            left=[pygame.transform.scale(pygame.image.load(blinky_folder.joinpath('left1.png')), SPRITE_SIZE),
                  pygame.transform.scale(pygame.image.load(blinky_folder.joinpath('left2.png')), SPRITE_SIZE)],
            right=[pygame.transform.scale(pygame.image.load(blinky_folder.joinpath('right1.png')), SPRITE_SIZE),
                   pygame.transform.scale(pygame.image.load(blinky_folder.joinpath('right2.png')), SPRITE_SIZE)],
            up=[pygame.transform.scale(pygame.image.load(blinky_folder.joinpath('up1.png')), SPRITE_SIZE),
                pygame.transform.scale(pygame.image.load(blinky_folder.joinpath('up2.png')), SPRITE_SIZE)],
            down=[pygame.transform.scale(pygame.image.load(blinky_folder.joinpath('down1.png')), SPRITE_SIZE),
                  pygame.transform.scale(pygame.image.load(blinky_folder.joinpath('down2.png')), SPRITE_SIZE)])

        pinky_assets = Asset(
            left=[pygame.transform.scale(pygame.image.load(pinky_folder.joinpath('left1.png')), SPRITE_SIZE),
                  pygame.transform.scale(pygame.image.load(pinky_folder.joinpath('left2.png')), SPRITE_SIZE)],
            right=[pygame.transform.scale(pygame.image.load(pinky_folder.joinpath('right1.png')), SPRITE_SIZE),
                   pygame.transform.scale(pygame.image.load(pinky_folder.joinpath('right2.png')), SPRITE_SIZE)],
            up=[pygame.transform.scale(pygame.image.load(pinky_folder.joinpath('up1.png')), SPRITE_SIZE),
                pygame.transform.scale(pygame.image.load(pinky_folder.joinpath('up2.png')), SPRITE_SIZE)],
            down=[pygame.transform.scale(pygame.image.load(pinky_folder.joinpath('down1.png')), SPRITE_SIZE),
                  pygame.transform.scale(pygame.image.load(pinky_folder.joinpath('down2.png')), SPRITE_SIZE)])
        inky_assets = Asset(
            left=[pygame.transform.scale(pygame.image.load(inky_folder.joinpath('left1.png')), SPRITE_SIZE),
                  pygame.transform.scale(pygame.image.load(inky_folder.joinpath('left2.png')), SPRITE_SIZE)],
            right=[pygame.transform.scale(pygame.image.load(inky_folder.joinpath('right1.png')), SPRITE_SIZE),
                   pygame.transform.scale(pygame.image.load(inky_folder.joinpath('right2.png')), SPRITE_SIZE)],
            up=[pygame.transform.scale(pygame.image.load(inky_folder.joinpath('up1.png')), SPRITE_SIZE),
                pygame.transform.scale(pygame.image.load(inky_folder.joinpath('up2.png')), SPRITE_SIZE)],
            down=[pygame.transform.scale(pygame.image.load(inky_folder.joinpath('down1.png')), SPRITE_SIZE),
                  pygame.transform.scale(pygame.image.load(inky_folder.joinpath('down2.png')), SPRITE_SIZE)])
        clyde_assets = Asset(
            left=[pygame.transform.scale(pygame.image.load(clyde_folder.joinpath('left1.png')), SPRITE_SIZE),
                  pygame.transform.scale(pygame.image.load(clyde_folder.joinpath('left2.png')), SPRITE_SIZE)],
            right=[pygame.transform.scale(pygame.image.load(clyde_folder.joinpath('right1.png')), SPRITE_SIZE),
                   pygame.transform.scale(pygame.image.load(clyde_folder.joinpath('right2.png')), SPRITE_SIZE)],
            up=[pygame.transform.scale(pygame.image.load(clyde_folder.joinpath('up1.png')), SPRITE_SIZE),
                pygame.transform.scale(pygame.image.load(clyde_folder.joinpath('up2.png')), SPRITE_SIZE)],
            down=[pygame.transform.scale(pygame.image.load(clyde_folder.joinpath('down1.png')), SPRITE_SIZE),
                  pygame.transform.scale(pygame.image.load(clyde_folder.joinpath('down2.png')), SPRITE_SIZE)])

        return blinky_assets, pinky_assets, inky_assets, clyde_assets

