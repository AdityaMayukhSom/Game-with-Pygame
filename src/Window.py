import pygame

from Food import Food
from Snake import Snake
from environment import white, red, black


class Window:
    def __init__(self, title: str, width: int, height: int):
        pygame.init()
        pygame.mixer.init()

        self.title = title
        self.width = width
        self.height = height

        # makes the game window, 900, 500 are the height and width of the window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        # To control the time within the game
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", 20)
        self.font_small = pygame.font.SysFont("Arial", 15)
        self.font_big = pygame.font.SysFont("Arial", 30)
        self.font_small_big = pygame.font.SysFont("Arial", 20)
        self.font_big_big = pygame.font.SysFont("Arial", 40)
        self.font_small_big_big = pygame.font.SysFont("Arial", 20)

    def fillScreenWithColor(self, color):
        self.screen.fill(color)

    def showTextOnScreen(self, text, color, x, y):
        textSurface = self.font.render(text, True, color)
        self.screen.blit(textSurface, [x, y])

    def showGreetings(self):
        greetingsImage = pygame.image.load("assets/snake.jpg")
        # convert alpha sets the image so that the game speed is not slowed down
        greetingsImage = pygame.transform.scale(greetingsImage, (self.width, self.height)).convert_alpha()
        self.screen.blit(greetingsImage, (0, 0))
        self.showTextOnScreen("Welcome to Snake Xenzia", red, 200, 150)
        self.showTextOnScreen("Press Spacebar to continue", red, 200, 200)
        pygame.display.update()

    def showScore(self, score: int, highScore: int):
        self.showTextOnScreen("Score: " + str(score), red, 5, 5)  # printing score on screen
        self.showTextOnScreen("High Score: " + str(highScore), red, 5, 40)

    def showGameOver(self):
        self.screen.fill(white)
        self.showTextOnScreen("Game Over! Press Enter to Continue.", red, 150, 220)  # printing score on screen
        pygame.display.update()

    def plotSnake(self, snake: Snake, color):
        for x, y in snake.list:
            pygame.draw.rect(self.screen, color, [x, y, Snake.size, Snake.size])

    def plotFood(self, food: Food, color):
        pygame.draw.rect(self.screen, color, [food.x, food.y, Food.size, Food.size])

    def playSuccessMusic(self):
        pygame.mixer.music.load("music/success.ogg")  # load the music
        pygame.mixer.music.play()  # play the music

    def playGameOverMusic(self):
        pygame.mixer.music.load("music/game_over.ogg")
        pygame.mixer.music.play()
