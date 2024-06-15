from typing import List
import numpy as np
from pygame import Surface, draw, SRCALPHA
from src.utils.colors import *
from src.flappy_bird_game.constants import *
from src.flappy_bird_game.Pipe import Pipe, PIPE_WIDTH
from src.model.activation_functions import sigmoid
from src.model.NeuralNet import NeuralNet


class Bird:
    def __init__(self,
                 screen: Surface, gravity: float, y: int = None, x: int = BIRD_X_POS, color=WHITE,
                 brain: NeuralNet | None = None) -> None:
        self.screen = screen
        self.color = color
        self.gravity = gravity
        self.x = x
        self.y = screen.get_height() // 2
        self.bird_velocity = 0

        # each pipe passed it's a score
        self.score = 1
        # for now, fitness is just the mean: self.score / birds-score-sum
        self.fitness = 0

        """" for now on NeuralNet, lets get only the 1st and 2nd pipes as input:
          input-1: self y position
          input-2: closest pipe x pos
          input-3: closest bottom pipe y (or bottom y of gap)
          input-4: closest upper pipe y (or top y of gap)
          input-5: closest2 pipe x pos
          input-6: closest2 bottom pipe y (or bottom y of gap)
          input-7: closest2 upper pipe y (or top y of gap)
        """
        if brain is None:
            self.brain = NeuralNet(
                7, 24, 1,
                activation=sigmoid,
            )
        else:
            self.brain = brain

    def jump(self):
        self.bird_velocity = JUMP_STRENGTH
        if self.y < 0 or self.y > self.screen.get_height():
            self.bird_velocity += self.gravity
            self.y += self.bird_velocity

    def think(self, ordered_pipes: List[Pipe]):
        closest_pipe = ordered_pipes[0]
        second_closer = ordered_pipes[1]
        # don't forget: normalize values on inputs
        inputs = np.array([
            self.y / self.screen.get_height(),
            closest_pipe.x_position / self.screen.get_width(),
            closest_pipe.up_pipe_height / self.screen.get_height(),
            (closest_pipe.up_pipe_height + closest_pipe.gap) / self.screen.get_height(),
            second_closer.x_position / self.screen.get_width(),
            second_closer.up_pipe_height / self.screen.get_height(),
            (second_closer.up_pipe_height + second_closer.gap) / self.screen.get_height(),
        ])

        action = self.brain.feed_forward(inputs)
        if action > .5:
            self.jump()

    def does_it_collide(self, pipes: List[Pipe]) -> bool:
        bird_x = self.x + BIRD_RADIUS
        bird_y_up = self.y + BIRD_RADIUS
        bird_y_down = self.y - BIRD_RADIUS

        for pipe in pipes:
            if pipe.x_position < bird_x < pipe.x_position + PIPE_WIDTH:
                if not (bird_y_up < pipe.up_pipe_height or bird_y_down > pipe.up_pipe_height + pipe.gap):
                    self.score += 1
                    return False
                else:
                    return True

    def fly(self) -> None:
        # cant go bellow the ground
        if self.y < self.screen.get_height():
            self.bird_velocity += self.gravity
            self.y += self.bird_velocity

        # all of this code for transparency... sigh
        circle_surface = Surface((BIRD_RADIUS * 2, BIRD_RADIUS * 2), SRCALPHA)
        transparent_color = self.color + (128,)
        draw.circle(circle_surface, transparent_color, (BIRD_RADIUS, BIRD_RADIUS), BIRD_RADIUS)
        self.screen.blit(circle_surface, (self.x - BIRD_RADIUS, self.y - BIRD_RADIUS))
