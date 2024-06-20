import numpy as np
from numpy import ndarray


class BoardDefinition:
    def __init__(self, board: ndarray):
        board_size = np.shape(board)
        self.height = board_size[0]
        self.width = board_size[1]
        self.board = board

    def check_coordinate_within(self, i, j):
        return i <= self.height - 1 and j <= self.width - 1

