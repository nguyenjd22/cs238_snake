import pygame
from dumbsnake import DumbSnake
from pygame.locals import *
import random

pygame.init()
width = 500
height = 500
screen = pygame.display.set_mode((width, height))

draw_apple = True
apple_eaten = False

NUM_SNAKES = 1
CELL_SIZE = 50

FRAMES_PER_TURN = 10

BACKGROUND_COL = (0, 0, 255)
SNAKE_COL = (0, 255, 0)
APPLE_COL = (255, 0, 0)

score = 0


snake = DumbSnake(width, height)

play_game = True
frames_passed = 0
dir_updated = False
calibrated = False
onEdge = False
while play_game:
    screen.fill(BACKGROUND_COL)

    snake_head = snake.getHeadLocation()


    if not dir_updated:
        if snake_head[1] / CELL_SIZE == snake.ENV_HEIGHT / CELL_SIZE - 1 or snake_head[0] / CELL_SIZE == 0 or snake_head[0] / CELL_SIZE == (snake.ENV_WIDTH / CELL_SIZE) - 1:
            onEdge = True
        else:
            onEdge = False

        if not calibrated:
            if snake_head[0] == 0 and snake_head[1] == 0:
                snake.updateDirection("RIGHT")
                calibrated = True
            if snake_head[0] == 0 and snake_head[1] != 0:
                snake.updateDirection("UP")

        else:
            if not onEdge:
                if (snake_head[0] / CELL_SIZE) % 2 == 1 and snake_head[1] == 0:
                    snake.updateDirection("DOWN")
                elif (snake_head[0] / CELL_SIZE) % 2 == 1 and snake_head[1] / CELL_SIZE == (snake.ENV_WIDTH / CELL_SIZE) - 2:
                    snake.updateDirection("RIGHT")
                elif (snake_head[1] / CELL_SIZE == 0 )and (snake_head[0] / CELL_SIZE % 2 == 0):
                    snake.updateDirection("RIGHT")
                elif snake_head[1] / CELL_SIZE == (snake.ENV_WIDTH / CELL_SIZE) - 2 and (snake_head[0] / CELL_SIZE) % 2 == 0:
                    snake.updateDirection("UP")
            else:
                if snake_head[0] == 0 and snake_head[1] == 0: #top left
                    snake.updateDirection("RIGHT")
                elif snake_head[0] / CELL_SIZE== snake.ENV_WIDTH / CELL_SIZE - 1 and snake_head[1] == 0: #top right
                    snake.updateDirection("DOWN")
                elif snake_head[0] / CELL_SIZE == snake.ENV_WIDTH / CELL_SIZE - 1 and snake_head[1] / CELL_SIZE == snake.ENV_HEIGHT / CELL_SIZE - 1: #bottom right
                    snake.updateDirection("LEFT")
                elif snake_head[0] == 0 and  snake_head[1] / CELL_SIZE == snake.ENV_HEIGHT / CELL_SIZE - 1: #bottom left
                    snake.updateDirection("UP")


        dir_updated = True

    #sets the apple location
    if apple_eaten:
        snake.setNewAppleLocation()

    #draws apple location
    pygame.draw.rect(screen, APPLE_COL, (snake.apple[0], snake.apple[1], CELL_SIZE, CELL_SIZE))

    #checks to see if the snake head is on the apple aka eats the appel
    if snake.getHeadLocation() == snake.apple:
        draw_apple = True
        apple_eaten = True
        score += 1
        if snake.getLength() == 100:
            play_game = False

    #dictates the speed of the game
    if frames_passed > FRAMES_PER_TURN:
        dir_updated = False
        if not snake.isAlive(): play_game = False

        frames_passed = 0
        snake.updateBody(apple_eaten)
        apple_eaten = False

    #draws the snake at every time step
    index = 0
    for snek in snake.body:
        pygame.draw.rect(screen, (0, 255 - int((255 * index + 1) / len(snake.body)), 0), (snek[0], snek[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, (0, 255 - int((255 * index + 1) / len(snake.body)), 0), (snek[0] + 1, snek[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2))
        index += 1

    pygame.display.update()
    frames_passed += 1

print(f"You got {score} points!")
pygame.quit()
