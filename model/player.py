from typing import Tuple


class Player:
    def __init__(self, sprites: list, position_x: int, position_y: int):
        self.sprites = sprites
        self.position_x = position_x
        self.position_y = position_y
        self.sprite_index = 0
