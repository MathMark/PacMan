PLAYER_SPRITE_SIZE = 45


class Player:
    def __init__(self, sprites: list, position_x: int, position_y: int, velocity=2):
        self.sprites = sprites
        self.position_x = position_x
        self.position_y = position_y
        self.sprite_index = 0
        self.velocity = velocity
        self.center_x = PLAYER_SPRITE_SIZE // 2
        self.center_y = PLAYER_SPRITE_SIZE // 2
        # R, L, U, D
        self.turns_allowed = [False, False, False, False]
