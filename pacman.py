import sys
from model.board_definition import BoardDefinition
from model.level_config import LevelConfig
from settings import *
from levels.level_content_initializer import LevelContentInitializer
from model.direction import Direction


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.timer = pygame.time.Clock()
        self.game_engine = self.init()
        self.game_start_sfx = pygame.mixer.Sound('media/game_start.wav')

    def init(self):
        board = BOARD.copy()
        board_definition = BoardDefinition(board)
        level_1 = LevelConfig(wall_color='blue', gate_color='white',
                              board_definition=board_definition, power_up_limit=POWER_UP_LIMIT)
        level_init = LevelContentInitializer(level_1, self.screen)
        return level_init.init_game_engine()

    def update(self):
        self.timer.tick(FPS)
        self.game_engine.tick()
        pygame.display.flip()

    def draw(self):
        self.screen.fill([12, 2, 25])

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.game_engine.direction_command = Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    self.game_engine.direction_command = Direction.RIGHT
                if event.key == pygame.K_DOWN:
                    self.game_engine.direction_command = Direction.DOWN
                if event.key == pygame.K_UP:
                    self.game_engine.direction_command = Direction.UP
                if event.key == pygame.K_SPACE and self.game_engine.game_over:
                    pygame.init()
                    self.game_start_sfx.play()
                    self.game_engine = self.init()
            if event.type == GHOST_EATEN_EVENT:
                self.game_engine.play_ghost_runsaway_sound()
            if event.type == PLAYER_EATEN_EVENT:
                self.game_engine.play_player_eaten_sound()

    def run(self):
        self.game_start_sfx.play()
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
