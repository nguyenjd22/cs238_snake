import pygame
from pygame.locals import *
import random

pygame.init()

width = 500
height = 500

screen = pygame.display.set_mode((width, height))

apple = [0, 0]
draw_apple = True
apple_eaten = False

num_snakes = 1
cell_size = 50

frames_per_turn = 600

background = (0, 0, 255)
snake_col = (0, 255, 0)
middle_col = (0, 255, 0)
apple_col = (255, 0, 0)

score = 0

snake = [[width // 2, height // 2], [width // 2, height // 2 - cell_size], [width // 2, height // 2 - 2 * cell_size]]

directions = ["UP", "DOWN", "LEFT", "RIGHT"]
direction = "LEFT"

def check_alive():
    if snake[0][0] > width or snake[0][0] < 0 or snake[0][1] > height or snake[0][1] < 0:
        return False
    for x in range(1, len(snake)):
        if snake[x] == snake[0] and x != 0: 
            return False

    return True

play_game = True
dir_updated = False
frames_passed = 0
while play_game: 
    screen.fill(background)

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
        apple[0] = random.randint(0, width / cell_size - 1) * cell_size
        apple[1] = random.randint(0, height / cell_size -1) * cell_size

    pygame.draw.rect(screen, apple_col, (apple[0], apple[1], cell_size, cell_size))

    if snake[0] == apple:
        draw_apple = True
        apple_eaten = True
        score += 1

    if frames_passed > frames_per_turn:
        dir_updated = False
        if not check_alive(): play_game = False
        frames_passed = 0
        new_head = [snake[0][0], snake[0][1]]
        
        if direction == "UP":
            new_head[1] -= cell_size
        elif direction == "DOWN":
            new_head[1] += cell_size
        elif direction == "RIGHT":
            new_head[0] += cell_size
        elif direction == "LEFT":
            new_head[0] -= cell_size
     
        snake.insert(0, new_head)
        if not apple_eaten: 
            snake.pop(len(snake) - 1)
        else:
            apple_eaten = False

    for snek in snake:
        pygame.draw.rect(screen, snake_col, (snek[0], snek[1], cell_size, cell_size))
        pygame.draw.rect(screen, middle_col, (snek[0] + 1, snek[1] + 1, cell_size - 2, cell_size - 2))

    pygame.display.update()
    frames_passed += 1

print(f"You got {score} points!")
pygame.quit()
