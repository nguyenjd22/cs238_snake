import snake
import random
import copy

CELL_SIZE = 50
directions = ["UP", "DOWN", "LEFT", "RIGHT"]

class GameState:

    def __init__(self, snakes, apple):
        self.players = snakes
        self.apple = apple
        self.actions = directions
        self.width = snakes[0].ENV_WIDTH
        self.height = snakes[0].ENV_HEIGHT
        self.cell_size = CELL_SIZE
        self.score = 0



    def getAlive(self):
        return len([snake for snake in self.snakes if snake.isAlive()])


    
    def gameOver(self):
        return self.getAlive() == 0
    
    def setApple(self, apple):
        self.apple = apple

    def generateSuccessor(self, playerIndex, action):
        #state = GameState(self.players, self.apple)
        state = copy.deepcopy(self)
        player = state.players[playerIndex]

        apple_eaten = state.apple == player.head
        player.direction = action
        player.updateBody(apple_eaten)
        #if not player.isAlive(): print("Oh, the humanity!")
        if apple_eaten: 
            state.apple[0] = random.randint(0, state.width / CELL_SIZE - 1) * CELL_SIZE
            state.apple[1] = random.randint(0, state.height / CELL_SIZE - 1) * CELL_SIZE
            state.score += 1

        state.players[playerIndex] = player
        return state

    def getActions(self, playerIndex):
        player = self.players[playerIndex]
        head = player.body[0]
        neck = player.body[1]
        badDirection = None
        if head[0] > neck[0]:
            badDirection = "LEFT"
        elif head[0] < neck[0]:
            badDirection = "RIGHT"
        elif head[1] > neck[1]:
            badDirection = "UP"
        else:
            badDirection = "DOWN"
        return [action for action in self.actions if action != badDirection]



    def evaluate(self, playerIndex):
        player = self.players[playerIndex]
        score = self.score * 0
        if not player.isAlive(): return -10000
        #if player.body[0] in player.body[1:]: return -10000
        
        if self.apple == player.body[0]:
            score += 10
        else: 
            score += 10 / mDistance(self.apple, player.body[0])
        #print(score)
        return score


def mDistance(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])
