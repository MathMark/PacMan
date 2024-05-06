import numpy as np
import pygame
from model.board_structure import BoardStructure
from model.level_config import LevelConfig
import math

PI = math.pi


class DrawManager:

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

    def draw_level(self, level_config: LevelConfig):
        board = level_config.board
        board_size = np.shape(board)
        board_height = board_size[0]
        board_width = board_size[1]

        height_ratio = ((self.height - 50) // board_height)
        width_ratio = (self.width // board_width)

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == BoardStructure.DOT.value:
                    center = (j * width_ratio + (0.5 * width_ratio), i * height_ratio + (0.5 * height_ratio))
                    pygame.draw.circle(self.screen, level_config.gate_color, center, 4)
                if board[i][j] == BoardStructure.BIG_DOT.value:
                    center = (j * width_ratio + (0.5 * width_ratio), i * height_ratio + (0.5 * height_ratio))
                    pygame.draw.circle(self.screen, level_config.gate_color, center, 10)
                if board[i][j] == BoardStructure.VERTICAL_WALL.value:
                    pygame.draw.line(self.screen, level_config.wall_color,
                                     (j * width_ratio + (0.5 * width_ratio), i * height_ratio),
                                     (j * width_ratio + (0.5 * width_ratio), i * height_ratio + height_ratio), 3)
                if board[i][j] == BoardStructure.HORIZONTAL_WALL.value:
                    pygame.draw.line(self.screen, level_config.wall_color,
                                     (j * width_ratio, i * height_ratio + (0.5 * height_ratio)),
                                     (j * width_ratio + width_ratio, i * height_ratio + (0.5 * height_ratio)), 3)
                if board[i][j] == BoardStructure.TOP_RIGHT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * width_ratio - (width_ratio * 0.4)) - 2,
                                     (i * height_ratio + (0.5 * height_ratio)), width_ratio, height_ratio],
                                    0, PI / 2, 3)
                if board[i][j] == BoardStructure.TOP_LEFT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * width_ratio + (width_ratio * 0.5)), (i * height_ratio + (0.5 * height_ratio)),
                                     width_ratio, height_ratio], PI / 2, PI,
                                    3)
                if board[i][j] == BoardStructure.BOTTOM_LEFT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * width_ratio + (width_ratio * 0.5)), (i * height_ratio - (0.4 * height_ratio)),
                                     width_ratio, height_ratio], PI,
                                    3 * PI / 2, 3)
                if board[i][j] == BoardStructure.BOTTOM_RIGHT_CORNER.value:
                    pygame.draw.arc(self.screen, level_config.wall_color,
                                    [(j * width_ratio - (width_ratio * 0.4)) - 2,
                                     (i * height_ratio - (0.4 * height_ratio)), width_ratio, height_ratio],
                                    3 * PI / 2,
                                    2 * PI, 3)
                if board[i][j] == BoardStructure.GATE.value:
                    pygame.draw.line(self.screen, level_config.gate_color,
                                     (j * width_ratio, i * height_ratio + (0.5 * height_ratio)),
                                     (j * width_ratio + width_ratio, i * height_ratio + (0.5 * height_ratio)), 3)
