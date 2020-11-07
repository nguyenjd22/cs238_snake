import pygame
from snake import Snake
from pygame.locals import *
import random
import numpy as np
from agent import Agent
import pdb 

pygame.init()
pygame.quit()

#### game set - up parameters #####
pygame.init()


WIDTH = 500
HEIGHT = 500
CELL_SIZE = 50

FRAMES_PER_TURN = 5


BACKGROUND_COL = (0, 128, 255)
SNAKE_COL = (0, 255, 128)
APPLE_COL = (255, 0, 64)

#### Q learning Hyper Parameters #####
states, actions = 145, 4

epsilon = 0.0

gamma = 0.5
alpha = 0.7

num_games = 1


screen = pygame.display.set_mode((WIDTH, HEIGHT))



def playGame(snake, agent):
    global screen
    

    score = 0
    play_game = True
    frames_passed = 0
    dir_updated = False

    snake.initApple()
    #print(snake.apple)
    start_state = agent.make_state()
    apple_dist = agent.getAppleDist()
    agent.s = (start_state, apple_dist)
    

    while play_game:

        screen.fill(BACKGROUND_COL)


        if frames_passed > FRAMES_PER_TURN: ##take action, get reward, go to new state
            agent.takeAction()
            agent.snake.updateBody()

            new_state = agent.make_state()
            new_apple_dist = agent.getAppleDist()
            agent.s_prime = (new_state, new_apple_dist)

            alive = agent.snake.isAlive()

            if not alive: ##if the snake died, then 
                agent.r = -10
                agent.s_prime = (144, 0) #death state
                num = agent.s[0]
                #print(agent.Q[num])
                #print(agent.a)
                agent.updateQ()
                play_game = False
            
            else:
                if agent.snake.body[0] == agent.snake.apple: ##snake ate the apple
                    score += 1

                    snake.addSnek()

                    #make a new apple and have the state the agent transitioned into reflect that:
                    agent.snake.setNewAppleLocation()
                    updated_state = agent.make_state()
                    updated_apple_dist = agent.getAppleDist()
                    agent.s_prime = (updated_state, updated_apple_dist)

                    agent.r = 5
                    agent.updateQ()

                    agent.s = agent.s_prime



                else: ##didn't eat the apple, so delete the last body element
                    

                    ##check if the agent got closer to the apple
                    got_closer = False
                    if agent.s[1] > agent.s_prime[1]:
                        got_closer = True
                    
                    if got_closer:
                        agent.r = 1
                    else:
                        agent.r = -1
                    
                    agent.updateQ()
                    agent.s = agent.s_prime

            frames_passed = 0


         ##don't change anything, just draw the snake
        i = 0
        for snek in agent.snake.body:
            pygame.draw.rect(screen, SNAKE_COL, (snek[0], snek[1], CELL_SIZE, CELL_SIZE))
            i += 1
            col = (0, int(255 * i + 1 / len(agent.snake.body)), 0)
            pygame.draw.rect(screen, col, (snek[0] + 1, snek[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2))
        pygame.draw.rect(screen, APPLE_COL, (snake.apple[0], snake.apple[1], CELL_SIZE, CELL_SIZE))

        frames_passed += 1
        pygame.display.update()

    print(f"You got {score} points!")
    return score
    #print(agent.Q)

        


def trainSnake():
    snake = Snake(WIDTH, HEIGHT)
    #Q = np.zeros((states, actions))
    Q = np.loadtxt("q.csv", delimiter=",")
    agent = Agent(snake, states, actions, epsilon, gamma, alpha, Q)

    sum = 0
    best = playGame(snake, agent)
    sum += best

    for i in range(1, num_games):
        new_snake = Snake(WIDTH, HEIGHT)
        agent.snake = new_snake
        if i > 50:
            agent.epsilon = 0.05
        new_score = playGame(new_snake, agent)
        sum += new_score
        
        if new_score > best:
            best = new_score


    print(best)
    print(sum / num_games)

    Qdata = agent.Q
    np.savetxt("q.csv", Qdata, delimiter=",")

    #for i in range(144):
        #print(agent.Q[i])

    pygame.quit()



def main():
    trainSnake()


if __name__ == '__main__':
    main()