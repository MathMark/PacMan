from enum import Enum


class BoardStructure(Enum):
    EMPTY = 0
    DOT = 1
    BIG_DOT = 2
    VERTICAL_WALL = 3
    HORIZONTAL_WALL = 4
    TOP_RIGHT_CORNER = 5
    TOP_LEFT_CORNER = 6
    BOTTOM_LEFT_CORNER = 7
    BOTTOM_RIGHT_CORNER = 8
    GATE = 9
