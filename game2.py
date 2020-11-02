import pygame
from snake import Snake
from pygame.locals import *
import random
from gameState import GameState

pygame.init()
width = 500
height = 500
screen = pygame.display.set_mode((width, height))

apple = [0, 0]
draw_apple = True
apple_eaten = False
one_ate = False
two_ate = False

NUM_SNAKES = 1
CELL_SIZE = 50

FRAMES_PER_TURN = 1000

BACKGROUND_COL = (0, 0, 255)
SNAKE_COL = (0, 255, 0)
APPLE_COL = (255, 0, 0)
OUTER_COL = (255, 255, 255)

score = 0


snake1 = Snake(width, height)
#snake2 = Snake(width, height)
state = GameState([snake1], apple)

play_game = True
frames_passed = 0
dir_updated = False
while play_game:
    screen.fill(BACKGROUND_COL)

    #gets the key events and sets the direction of the snake
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play_game = False

    #sets the apple location
    if draw_apple:
        draw_apple = False
        while True:
            apple[0] = random.randint(0, width / CELL_SIZE - 1) * CELL_SIZE
            apple[1] = random.randint(0, height / CELL_SIZE -1) * CELL_SIZE
            if apple not in snake1.body: break
        state.setApple(apple)

    #draws apple location
    pygame.draw.rect(screen, APPLE_COL, (apple[0], apple[1], CELL_SIZE, CELL_SIZE))

    #checks to see if the snake head is on the apple aka eats the appel
    if snake1.getHeadLocation() == apple:
        draw_apple = True
        apple_eaten = True
        
        score += 1

    #dictates the speed of the game
    if frames_passed > FRAMES_PER_TURN:
        #print(state.players[0].body[0])
        dir_updated = False
        if not snake1.isAlive(): play_game = False
        


        def getMax(playerIndex, gameState, depth):
            if depth <= 0: return gameState.evaluate(playerIndex)
            return max([getMax(playerIndex, gameState.generateSuccessor(playerIndex, action), depth - 1) for action in state.getActions(playerIndex)])

        def getBestAction(playerIndex, gameState):
            bestActions = []
            bestScore = -10001
            #actions = state.getActions(playerIndex)
            #return random.choice(actions)

            for action in state.getActions(playerIndex):
                curr = getMax(playerIndex, gameState.generateSuccessor(playerIndex, action), 0)
                if curr > bestScore:
                    bestScore = curr
                    bestActions = [action]
                elif curr == bestScore:
                    bestActions.append(action)
            if bestScore == -10000:
                print("Time to die...")
            return random.choice(bestActions)

        bestAction = getBestAction(0, state)
        snake1.updateDirection(bestAction)
        frames_passed = 0
        state = state.generateSuccessor(0, snake1.direction)
        snake1.updateBody(apple_eaten)
        #snake2.updateBody(two_ate)
        
        apple_eaten = False

    #draws the snake at every time step
    def drawSnake(snake, color1, color2):
        for snek in snake.body:
            pygame.draw.rect(screen, color1, (snek[0], snek[1], CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, color2, (snek[0] + 1, snek[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2))
    #if not snake1.isAlive(): play_game = False
    drawSnake(snake1, OUTER_COL, SNAKE_COL)
    #drawSnake(snake2, SNAKE_COL, BACKGROUND_COL)

    pygame.display.update()
    frames_passed += 1

print(f"You got {score} points!")
pygame.quit()
