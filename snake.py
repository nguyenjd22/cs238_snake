import pygame
from pygame.locals import *
import random

SNAKE_COL = (0, 255, 0)
cell_size = 50
directions = ["UP", "DOWN", "LEFT", "RIGHT"]

class Snake:
    def __init__(self, width, height):
            self.body = [[width // 2, height // 2], [width // 2, height // 2 - cell_size], [width // 2, height // 2 - 2 * cell_size]]
            self.head = self.body[0]
            self.length = len(self.body)
            self.direction = "LEFT"
            self.ENV_WIDTH = width
            self.ENV_HEIGHT = height


    def getHeadLocation(self):
        return self.body[0]
    def getLength(self):
        return len(self.body)
    def getDirection(self):
        return self.direction

    def isAlive(self):
        if self.body[0][0] > self.ENV_WIDTH or self.body[0][0] < 0 or self.body[0][1] > self.ENV_HEIGHT or self.body[0][1] < 0:
            return False
        for x in range(1, self.getLength()):
            if self.body[x] == self.body[0] and x != 0:
                return False

        return True
