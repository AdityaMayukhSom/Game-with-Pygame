import os, pygame
import sys

# sys.path.append('src')
# sys.path.append('../')
from Food import Food
from Snake import Snake
from Window import Window
from environment import fps, white, red, black
from environment import screenWidth, screenHeight
from environment import eatingRadius, highScorePath


def isFoodEaten(snake: Snake, food: Food):
    return abs(food.x - snake.x) < eatingRadius and abs(food.y - snake.y) < eatingRadius


# Creating game loop
def gameLoop(window: Window):
    snake = Snake()
    food = Food()
    # when this becomes true, we will ask whether he wants to quit the game or play another round
    gameOver = False
    score, highScore = 0, 0

    if not os.path.exists(highScorePath):
        with open(highScorePath, "w") as f:
            f.write("0")
    else:
        with open(highScorePath, "r") as f:
            highScore = int(f.read())

    while (
        True
    ):  # this loop is created so that the game window stays till the user exits it
        if gameOver:
            with open(highScorePath, "w") as f:
                f.write(str(highScore))
            window.showGameOver()
            break

        for (
            event
        ) in (
            pygame.event.get()
        ):  # this consists of all the activities we do with the mouse or keyboard
            if event.type == pygame.QUIT:  # if exit button is pressed
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                snake.handleDirection(event.key)

        snake.slither()

        if isFoodEaten(snake, food):
            score += 10
            window.playSuccessMusic()
            food.changePosition()
            snake.handleFoodEaten()
            if score > highScore:
                highScore = score

        window.fillScreenWithColor(white)
        window.showScore(score, highScore)

        if (
            snake.head in snake.list[:-1]
            or snake.x < 0
            or snake.x > screenWidth
            or snake.y < 0
            or snake.y > screenHeight
        ):
            # if the snake collides with itself, i.e., coordinate of the head matches with any other element in the list
            gameOver = True
            window.playGameOverMusic()

        window.plotFood(food, red)
        window.plotSnake(snake, black)
        window.clock.tick(fps)
        pygame.display.update()
