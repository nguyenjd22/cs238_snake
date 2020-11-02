import random

SNAKE_COL = (0, 255, 0)
CELL_SIZE = 50
directions = ["UP", "DOWN", "LEFT", "RIGHT"]

class Snake:
    def __init__(self, width, height):
            self.body = [[width // 2, height // 2], [width // 2, height // 2 - CELL_SIZE], [width // 2, height // 2 - 2 * CELL_SIZE]]
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
        if self.body[0][0] >= self.ENV_WIDTH or self.body[0][0] < 0 or self.body[0][1] >= self.ENV_HEIGHT or self.body[0][1] < 0:
            return False
        head = self.body[0]
        #for x in range(self.getLength()):
            #if self.body[x] == self.body[0] and x != 0:
                #print(f"Head: {self.body[0]}")
                #return False
        if head in self.body[1:]: return False

        return True

    def updateBody(self, apple_eaten):
        new_head = [self.body[0][0], self.body[0][1]]

        if self.direction == "UP":
            new_head[1] -= CELL_SIZE
        elif self.direction == "DOWN":
            new_head[1] += CELL_SIZE
        elif self.direction == "RIGHT":
            new_head[0] += CELL_SIZE
        elif self.direction == "LEFT":
            new_head[0] -= CELL_SIZE

        self.body.insert(0, new_head)
        if not apple_eaten:
            self.body.pop(self.getLength() - 1)

    def updateDirection(self, dir):
        if dir == "UP" and self.direction != "DOWN":
            self.direction = dir
        elif dir == "DOWN" and self.direction != "UP":
            self.direction = dir
        elif dir == "RIGHT" and self.direction != "LEFT":
            self.direction = dir
        elif dir == "LEFT" and self.direction != "RIGHT":
            self.direction = dir
