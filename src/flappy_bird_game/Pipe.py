from typing import List
import random
from pygame import Surface, draw
from src.utils.colors import *
from src.flappy_bird_game.constants import *


class Pipe:
    def __init__(self, screen: Surface, ini_x_position: int | None) -> None:
        self.screen = screen
        self.up_pipe_height = 0
        self.down_pipe_height = 0
        self.gap = 0
        self.x_position = ini_x_position if ini_x_position is not None else screen.get_width()
        self.reset_pipe_structure()

    def reset_pipe_structure(self):
        self.gap = random.randint(MIN_PIPE_GAP, MAX_PIPE_GAP)
        self.down_pipe_height = random.randint(0, self.screen.get_height() - self.gap)
        self.up_pipe_height = self.screen.get_height() - self.gap - self.down_pipe_height

    def draw(self) -> None:
        # up pipe
        draw.rect(self.screen, CYAN, (self.x_position, 0, PIPE_WIDTH, self.up_pipe_height))
        # gap
        draw.rect(self.screen, BLACK, (self.x_position, self.up_pipe_height, PIPE_WIDTH, self.gap))
        # down pipe
        down_pipe_ini = self.gap + self.up_pipe_height
        draw.rect(self.screen, CYAN, (self.x_position, down_pipe_ini, PIPE_WIDTH, self.down_pipe_height))


def get_closest_pipes(pipes: List[Pipe]) -> List[Pipe]:
    ordered_pipes = sorted(pipes, key=lambda _pipe: _pipe.x_position)
    for i in range(len(ordered_pipes)):
        if ordered_pipes[i].x_position < BIRD_X_POS:
            ordered_pipes.pop(i)
            break
    return ordered_pipes




