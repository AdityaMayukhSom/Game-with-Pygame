# Colors
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)

# Creating game window
screenWidth: int = 900
screenHeight: int = 500

fps: int = 60
gameTitle = "Snake Xenzia"

size = 10
foodSize = size
snakeSize = size
snakeInitialVelocity = 2
snakeVelocityIncrement = 0.01

eatingRadius: int = 5
incrementScore: int = 10

highScorePath = "temp/highScore.txt"
successMusicPath = "assets/music/success.ogg"
gameOverMusicPath = "assets/music/game_over.ogg"
greetingImagePath = "assets/image/snake.jpg"
