from lambda0agent import LAgent
import pygame
from snake import Snake
from pygame.locals import *
import random
import numpy as np

pygame.init()
width = 1000
height = 1000
screen = pygame.display.set_mode((width, height))


draw_apple = True
apple_eaten = False

NUM_SNAKES = 1
CELL_SIZE = 50

FRAMES_PER_TURN = 600

BACKGROUND_COL = (0, 0, 255)
SNAKE_COL = (0, 255, 0)
APPLE_COL = (255, 0, 0)

states = 256
actions = 4
epsilon = 0.5
gamma = 0.9
alpha = 0.2
lam = 0.2

Q = np.zeros((states, actions))
N = np.zeros((states, actions))

#snake = Snake(width, height)
#agent = Agent(snake, states, actions, epsilon, gamma, alpha, Q)
#agent.s = agent.make_state()
num_episodes = 1
directions = ["UP", "DOWN", "LEFT", "RIGHT"]

for i in range(num_episodes):
    snake = Snake(width, height)
    agent = LAgent(snake, states, actions, epsilon, gamma, alpha, Q, N, lam)
    agent.s = agent.make_state()

    play_game = True
    frames_passed = 0
    dir_updated = False
    score = 0


    while play_game:
        screen.fill(BACKGROUND_COL)

        if not dir_updated:
            if np.random.rand() < agent.epsilon:
               action = random.choice(directions)
               snake.updateDirection(action)
               agent.a = agent.dir_to_num(action)
            else:
               options = agent.Q[agent.s]
               act_num = np.argmax(options)
               agent.a = act_num
               action = agent.dir_to_num(act_num)
               snake.updateDirection(action)
            dir_updated = True


        #sets the apple location
        if draw_apple:
            draw_apple = False
            snake.setNewAppleLocation()
        #draws apple location
        pygame.draw.rect(screen, APPLE_COL, (snake.apple[0], snake.apple[1], CELL_SIZE, CELL_SIZE))

        #checks to see if the snake head is on the apple aka eats the apple
        if snake.getHeadLocation() == snake.apple:
            draw_apple = True
            apple_eaten = True
            score += 1

        #dictates the speed of the game
        if frames_passed > FRAMES_PER_TURN:
            dir_updated = False
            if not snake.isAlive():
                play_game = False
                agent.r = -1000
            frames_passed = 0
            snake.updateBody(apple_eaten)
            agent.s_prime = agent.make_state()
            if apple_eaten:
                agent.r = 100
            else:
                agent.r = -0.1
            apple_eaten = False

        #draws the snake at every time step
        for snek in snake.body:
            #pass
            pygame.draw.rect(screen, SNAKE_COL, (snek[0], snek[1], CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, SNAKE_COL, (snek[0] + 1, snek[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2))

        agent.updateQ()
        for j in range(states):
            print(Q[j])

        pygame.display.update()
        frames_passed += 1

    print(f"You got {score} points!")

##need to add way to save policy and re-use

print(Q)
pygame.quit()