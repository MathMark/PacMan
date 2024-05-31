from model.board_definition import BoardDefinition
from model.positions import InitialPositions


class LevelConfig:

    def __init__(self, board_definition: BoardDefinition, wall_color: str, gate_color: str, power_up_limit, initial_positions: InitialPositions):
        self.board_definition = board_definition
        self.wall_color = wall_color
        self.gate_color = gate_color
        self.score = 0
        self.power_up_limit = power_up_limit
        self.initial_positions = initial_positions
