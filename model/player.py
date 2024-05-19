from model.direction import Direction

PLAYER_SPRITE_SIZE = 45


class Player:
    def __init__(self, sprites: list, position_x: int, position_y: int, velocity=2):
        self.sprites = sprites
        self.position_x = position_x
        self.position_y = position_y
        self.sprite_index = 0
        self.velocity = velocity
        self.center_x = self.position_x + PLAYER_SPRITE_SIZE // 2
        self.center_y = self.position_y + PLAYER_SPRITE_SIZE // 2
        # R, L, U, D
        self.turns_allowed = [False, False, False, False]
        self.direction = Direction.LEFT

    def teleport(self, x, y):
        self.position_x = x
        self.position_y = y
        self.center_x = self.position_x + PLAYER_SPRITE_SIZE // 2
        self.center_y = self.position_y + PLAYER_SPRITE_SIZE // 2

    def move_right(self):
        self.position_x += self.velocity
        self.center_x += self.velocity

    def move_left(self):
        self.position_x -= self.velocity
        self.center_x -= self.velocity

    def move_up(self):
        self.position_y -= self.velocity
        self.center_y -= self.velocity

    def move_down(self):
        self.position_y += self.velocity
        self.center_y += self.velocity
