from model.board_definition import BoardDefinition


class SpaceParams:
    def __init__(self, board_definition: BoardDefinition, segment_width, segment_height, fudge_factor):
        self.board_definition = board_definition
        self.tile_width = segment_width
        self.tile_height = segment_height
        self.fudge_factor = fudge_factor
