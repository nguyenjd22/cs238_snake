
import pygame
from snake import Snake
from pygame.locals import *
import random
import numpy as np

CELL_SIZE = 50

class Agent():
    def __init__(self, snake, states, actions, epsilon, gamma, alpha, Q):
        self.snake = snake
        self.grid_dims = snake.ENV_HEIGHT / CELL_SIZE
        self.epsilon = epsilon
        self.Q = Q
        self.s = 0
        self.r = 0
        self.a = 0
        self.s_prime = 0
        self.gamma = gamma
        self.alpha = alpha
        self.num_states = states
        self.num_actions = actions
        self.old_dist = float("inf")

    def make_state(self):
        old = self.snake.getState()
        dir_num = self.dir_to_num(old[2])
        quad_num = self.apple_quad(old[1], old[0][0])
        obs = self.get_obstacles(old[0][0])
        state_list = [dir_num] + [quad_num] + obs
        state_tup = tuple(state_list)
        num = np.ravel_multi_index(state_tup, (4, 4, 2, 2, 2, 2))
        return num

    def get_obstacles(self, head):
        obs = [0, 0, 0, 0] #list of if obstacles are present up, right, left, down
        if head[1] == 0:
            obs[0] = 1
        if head[0] == self.snake.ENV_WIDTH:
            obs[1] = 1
        if head[1] == self.snake.ENV_HEIGHT - CELL_SIZE:
            obs[2] = 1
        if head[0] == CELL_SIZE:
            obs[3] = 1
        new_obs = self.check_body(head, obs)
        return new_obs

    def check_body(self, head, obs):
        for i in range(1, len(self.snake.body)):
            snek = self.snake.body[i]
            if head[1] == snek[1] + CELL_SIZE:
                obs[0] = 1
            if head[0] == snek[0] + CELL_SIZE:
                obs[1] = 1
            if head[1] == snek[1] - CELL_SIZE:
                obs[2] = 1
            if head[0] == snek[0] - CELL_SIZE:
                obs[3] = 1
        return obs


    def apple_quad(self, apple, head):
         if apple[0] < head[0] and apple[1] < head[1]:
             #top right
             return 0
         if apple[0] >= head[0] and apple[1] < head[1]:
             #top left
             return 1
         if apple[0] >= head[0] and apple[1] >= head[1]:
             #bottom left
             return 2
         else:
             #bottom right
             return 3

    def dir_to_num(self, dir):
        if dir == "UP":
            return 0
        if dir == "RIGHT":
            return 1
        if dir == "DOWN":
            return 2
        if dir == "LEFT":
                return 3

    def num_to_dir(self, num):
        if num == 0:
            return "UP"
        if num == 1:
            return "RIGHT"
        if num == 2:
            return "DOWN"
        if num == 3:
            return "LEFT"

    def updateQ(self):
        gamma, Q, alpha = self.gamma, self.Q, self.alpha
        s_prime_row = self.Q[self.s_prime]
        max_new_Q = s_prime_row.max()
        self.Q[self.s, self.a]  += alpha * (self.r + gamma * max_new_Q - Q[self.s, self.a])

    def getAppleDist(self):
        x, y = self.snake.getHeadLocation()
        apple = self.snake.getState()[1]
        new_dist = abs(x - apple[0]) + abs(y - apple[1])
        return new_dist

    def updateAppleDist(self, dist):
        self.old_dist = dist
    
    def gotCloser(self):
        new_dist = self.getAppleDist()
        if new_dist > self.old_dist:
            self.old_dist = new_dist
            return False
        else:
            self.old_dist = new_dist
            return True
