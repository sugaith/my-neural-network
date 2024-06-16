from typing import List
import numpy as np
from src.flappy_bird_game.Bird import Bird
from pygame import Surface

MUTATION_RATE = np.float32(.45)
BEST_ONES_DEAD_POOL = 0
BEST_ONES_PICK_COUNT = 3


# for generation counting
class Generation:
    def __init__(self):
        self.count = 0

    def get_next_mutation_rate(self) -> np.float32:
        """" formula to narrow the Mutation rate at each generation
        mut_rate will trend to 0 on GEN.count ~ 36 (no much change in children), and then up again"""
        return abs(MUTATION_RATE - self.count / 36)


GEN = Generation()


# to calculate fittness, lets get the simple mean: bird.score / birds-score-sum
def calc_fitness(population: List[Bird]):
    score_sum = 0
    for bird in population:
        score_sum += bird.score

    for bird in population:
        bird.fitness = bird.score / score_sum


def spawn_bird_generation(screen: Surface, gravity, count: int, previous_gen: None | List[Bird] = None) -> List[Bird]:
    if previous_gen is None:
        return [Bird(screen=screen, gravity=gravity) for _ in range(count)]

    calc_fitness(previous_gen)
    # sort best scores desc
    previous_gen.sort(key=lambda dead_bird: dead_bird.fitness, reverse=True)

    # pick best ones
    best_ones = previous_gen[:BEST_ONES_PICK_COUNT]
    # give extra points to the best
    for i, bird in enumerate(reversed(best_ones)):
        bird.score += i

    GEN.count += 1
    print('GENERATION: ', GEN.count)
    print('previous_gen_count')
    print(len(previous_gen))

    # cut dead pool of birds
    previous_gen[:] = previous_gen[:BEST_ONES_DEAD_POOL]

    # create new generation of birds
    next_gen = [*best_ones]
    children_count = (count - len(best_ones)) // len(best_ones)
    for best_one in best_ones:
        print('Generation with mutation of: ' + str(GEN.get_next_mutation_rate()))
        next_gen += [
            Bird(screen=screen, gravity=gravity,
                 brain=best_one.brain.clone_and_mutate(GEN.get_next_mutation_rate())
                 ) for _ in range(children_count)
        ]

    return next_gen
