import pygame
from typing import List
from src.utils.colors import *
from src.flappy_bird_game.constants import *
from src.flappy_bird_game.Bird import Bird
from src.flappy_bird_game.Pipe import Pipe, get_closest_pipes
from src.flappy_bird_game.neuro_evolution_algorithm import spawn_bird_generation, GEN

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Game variables
gravity = 0.24
pipe_velocity = -3

pipes = []
my_bird = Bird(x=BIRD_X_POS//2,y=HEIGHT, screen=screen, gravity=gravity, color=GREEN)
ai_birds = spawn_bird_generation(screen, gravity, AI_BIRDS_COUNT)
dead_ai_birds: List[Bird] = []

# Main game loop
running = True
clock = pygame.time.Clock()


# Font for AI birds count
font = pygame.font.SysFont(size=36,name=None)

# Create initial pipes
for i in range(4):
    ini_pos = screen.get_width() + i * 300
    pipes.append(Pipe(screen, ini_pos))

while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            my_bird.jump()

    for ai_bird in ai_birds:
        ai_bird.think(get_closest_pipes(pipes))

    # Update pipes
    for pipe in pipes:
        if pipe.x_position + pipe_velocity > -PIPE_WIDTH:
            pipe.x_position += pipe_velocity
        else:
            pipe.x_position = screen.get_width()
            pipe.reset_pipe_structure()

    # Check for collisions
    # running = not my_bird.does_it_collide(pipes)
    for ai_bird_i in range(len(ai_birds) - 1, -1, -1):
        ai_bird = ai_birds[ai_bird_i]
        if ai_bird.does_it_collide(pipes):
            dead_ai_birds.append(ai_birds.pop(ai_bird_i))

    # call next generation if everybody died
    if len(ai_birds) == 0:
        ai_birds = spawn_bird_generation(screen, gravity, AI_BIRDS_COUNT, dead_ai_birds)
        # move pipe a little more
        for pipe in pipes:
            if pipe.x_position + pipe_velocity > -PIPE_WIDTH:
                pipe.x_position += BIRD_RADIUS*3 - 60

    # DRAW PIPES
    for pipe in pipes:
        pipe.draw()

    # FLY THE BIRDS
    for ai_bird in ai_birds:
        ai_bird.fly()
    my_bird.fly()

    # render texts
    score_text = font.render("ai_birds: " + str(len(ai_birds)), True, WHITE)
    screen.blit(score_text, (9, 9))
    generation_count_text = font.render("generation: " + str(GEN.count), True, WHITE)
    screen.blit(generation_count_text, (9, 33))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
