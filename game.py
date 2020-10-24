import pygame
from snake import Snake
from pygame.locals import *
import random

pygame.init()

width = 500
height = 500

screen = pygame.display.set_mode((width, height))

apple = [0, 0]
draw_apple = True
apple_eaten = False

NUM_SNAKES = 1
CELL_SIZE = 50

FRAMES_PER_TURN = 700

BACKGROUND_COL = (0, 0, 255)
SNAKE_COL = (0, 255, 0)
APPLE_COL = (255, 0, 0)

score = 0

snake = Snake(width, height)

directions = ["UP", "DOWN", "LEFT", "RIGHT"]
direction = "LEFT"

play_game = True
dir_updated = False
frames_passed = 0
while play_game:
    screen.fill(BACKGROUND_COL)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play_game = False
        if event.type == pygame.KEYDOWN and not dir_updated:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"
            if event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            dir_updated = True

    if draw_apple:
        draw_apple = False
        apple[0] = random.randint(0, width / CELL_SIZE - 1) * CELL_SIZE
        apple[1] = random.randint(0, height / CELL_SIZE -1) * CELL_SIZE

    pygame.draw.rect(screen, APPLE_COL, (apple[0], apple[1], CELL_SIZE, CELL_SIZE))

    if snake.getHeadLocation() == apple:
        draw_apple = True
        apple_eaten = True
        score += 1

    if frames_passed > FRAMES_PER_TURN:
        dir_updated = False
        if not snake.isAlive(): play_game = False
        frames_passed = 0
        new_head = [snake.body[0][0], snake.body[0][1]]

        if direction == "UP":
            new_head[1] -= CELL_SIZE
            snake.direction = "UP"
        elif direction == "DOWN":
            new_head[1] += CELL_SIZE
            snake.direction = "DOWN"
        elif direction == "RIGHT":
            new_head[0] += CELL_SIZE
            snake.direction = "RIGHT"
        elif direction == "LEFT":
            new_head[0] -= CELL_SIZE
            snake.direction = "LEFT"

        snake.body.insert(0, new_head)
        if not apple_eaten:
            snake.body.pop(snake.getLength() - 1)
        else:
            apple_eaten = False

    for snek in snake.body:
        pygame.draw.rect(screen, SNAKE_COL, (snek[0], snek[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, SNAKE_COL, (snek[0] + 1, snek[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2))

    pygame.display.update()
    frames_passed += 1

print(f"You got {score} points!")
pygame.quit()
