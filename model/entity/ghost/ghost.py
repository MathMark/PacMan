import enum
from queue import Queue
from typing import Tuple

import numpy as np
import pygame
from model.direction import Direction
from model.entity.entity import Entity
from model.entity.player.player import Player
from model.space_params.space_params import SpaceParams
from model.turns import Turns
from settings import SPRITE_SIZE

GHOST_SPRITE_SIZE = (45, 45)
RUN_POSITION_CHANGE_FREQUENCY = 2


class Ghost(Entity):
    def __init__(self, center_position: Tuple, img, frightened_img, eaten_img, player: Player,
                 turns: Turns, space_params: SpaceParams, home_corner: Tuple,
                 velocity=2):
        super().__init__(center_position, turns, space_params, velocity)
        self.img = img
        self.eaten_img = eaten_img
        self.frightened_img = frightened_img
        self.direction = Direction.UP
        self.player = player
        self.condition = self.Condition.CHASE
        self.home_corner = home_corner
        self.ghost_run_path = Queue()
        self.c = 0

    def is_frightened(self):
        return self.condition == self.Condition.FRIGHTENED

    def is_eaten(self):
        return self.condition == self.Condition.EATEN

    def is_chasing(self):
        return self.condition == self.Condition.CHASE

    def set_to_chase(self):
        self.velocity = 2
        self.current_target = self.target
        self.condition = self.Condition.CHASE

    def set_to_frightened(self):
        self.velocity = 1
        self.condition = self.Condition.FRIGHTENED
        self.current_target = self.home_corner

    def set_to_eaten(self):
        self.condition = self.Condition.EATEN
        path = self.find_path((14, 14))
        for node in path:
            self.ghost_run_path.put(node)

    def draw(self, screen):
        if self.condition == self.Condition.CHASE:
            screen.blit(pygame.transform.flip(self.img, True, False),
                        (self.top_left_x, self.top_left_y))
        elif self.condition == self.Condition.FRIGHTENED:
            screen.blit(pygame.transform.flip(self.frightened_img, True, False),
                        (self.top_left_x, self.top_left_y))
        else:  # eaten
            screen.blit(pygame.transform.flip(self.eaten_img, True, False),
                        (self.top_left_x, self.top_left_y))

    def follow_target(self, screen):
        pass

    def target(self) -> Tuple:
        pass

    def runaway(self):
        if self.ghost_run_path.empty():
            self.direction = Direction.UP
            self.turns = Turns()
            self.set_to_chase()
            self.top_left_x = self.location_x - SPRITE_SIZE // 2
            self.top_left_y = self.location_y - SPRITE_SIZE // 2
        else:
            if self.c % RUN_POSITION_CHANGE_FREQUENCY == 0:
                next_node = self.ghost_run_path.get()
                self.location_x = next_node[0] * self.space_params.tile_width + (self.space_params.tile_width // 2)
                self.location_y = next_node[1] * self.space_params.tile_height + (self.space_params.tile_height // 2)
            if self.c == RUN_POSITION_CHANGE_FREQUENCY:
                self.c = 0
            else:
                self.c += 1

    def find_path(self, target_point: Tuple):
        # BFS algorithm to find the shortest path
        board = self.space_params.board_definition.board
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        x = (self.location_x // self.space_params.tile_width)
        y = (self.location_y // self.space_params.tile_height)
        start = (x, y)
        end = (target_point[0], target_point[1])
        visited = np.zeros_like(board, dtype=bool)
        visited[start] = True
        queue = Queue()
        queue.put((start, []))
        while not queue.empty():
            (node, path) = queue.get()
            for dx, dy in directions:
                next_node = (node[0] + dx, node[1] + dy)
                if (next_node == end):
                    return path + [next_node]
                if ((next_node[0] >= 0 and next_node[1] >= 0) and
                        (next_node[1] < len(board) and next_node[0] < len(board[0])) and
                        (board[next_node[1]][next_node[0]] < 3 or board[next_node[1]][next_node[0]] == 9)
                        and not visited[next_node[1]][next_node[0]]):
                    visited[next_node[1]][next_node[0]] = True
                    queue.put((next_node, path + [next_node]))
        return []

    def _move(self, direction_command: Direction):
        self._teleport_if_board_limit_reached()
        self._align_movement_to_cell_center(direction_command)

        if self.direction == Direction.LEFT:
            if self.turns.left:
                self._move_left()
            else:
                self._snap_to_center(self.space_params.tile_width, self.space_params.tile_height)

        if self.direction == Direction.RIGHT:
            if self.turns.right:
                self._move_right()
            else:
                self._snap_to_center(self.space_params.tile_width, self.space_params.tile_height)

        if self.direction == Direction.DOWN:
            if self.turns.down:
                self._move_down()
            else:
                self._snap_to_center(self.space_params.tile_width, self.space_params.tile_height)
        if self.direction == Direction.UP:
            if self.turns.up:
                self._move_up()
            else:
                self._snap_to_center(self.space_params.tile_width, self.space_params.tile_height)

    class Condition(enum.Enum):
        CHASE = 0
        EATEN = 1
        FRIGHTENED = 2
