import asyncio
import pygame
import random
import os
import sys
pygame.init()
# x = pygame.init() # returns a tuple (a, b), where a = number of initialized packages and b = number of errors. Used for testing purpose.
# print(x)

# Adding background music
pygame.mixer.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0 , 0)

# Creating game window
screen_width = 900
screen_height = 500
game_window = pygame.display.set_mode((screen_width, screen_height)) # makes the game window, 900, 500 are the height and width of the window

# Background Image
bg_img = pygame.image.load("snake.jpg")
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height)).convert_alpha() # convert alpha sets the image so that the game speed is not slowed down

# Name of the game
pygame.display.set_caption("Snake Xenzia") # sets the name of the game which will be visible on the top of game window
pygame.display.update() # update function has to be run to make the changes in the display visible. Otherwise the user cannot see it.

# Game specific variables
clock = pygame.time.Clock() # to control the time within the game
font = pygame.font.SysFont("calibri", 40) # sets the font of the game. None means it takes default font of pygame and 55 is the fontsize

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color) # True is set to show high resolution things on low resolution
    game_window.blit(screen_text, [x, y])
    
def plot_snake(game_window, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(game_window, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    game_window.fill(white)
    game_window.blit(bg_img, (0, 0))
    text_screen("Welcome to Snake Xenzia", red, 200, 150)
    text_screen("Press Spacebar to continue", red, 200, 200)
    while not exit_game:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # pygame.mixer.music.load("success.ogg") # load the music
                    # pygame.mixer.music.play() # play the music
                    asyncio.run(game_loop())
        pygame.display.update()
        clock.tick(60)

# Creating game loop
async def game_loop():
    # Game specific variables
    exit_game = False # this will become true when the player will want to exit the game, and thus the game will be closed
    game_over = False # when this becomes true, we will ask whether he wants to quit the game or play another round
    snake_x = 45
    snake_y = 55
    snake_size = 10

    init_velocity = 5
    velocity_x = 0
    velocity_y = 0

    snake_list = []
    snake_length = 1

    food_x = random.randint(50, screen_width - 50) # plots the food anywhere
    food_y = random.randint(50, screen_height - 50)
    score = 0
    fps = 30 # fps = frame per second
    if not os.path.exists("high_score.txt"):
        with open("high_score.txt", "w") as f:
            f.write("0")
    with open("high_score.txt", "r") as f:
        high_score = f.read()
    while not exit_game: # this loop is created so that the game window stays till the user exits it
        if game_over:
            with open("high_score.txt", "w") as f:
                f.write(str(high_score))
            game_window.fill(white)
            text_screen("Game Over! Press Enter to Continue.", red, 150, 220)
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        exit_game = True
                        await game_loop()
        else:
            for event in pygame.event.get(): # this consists of all the activities we do with the mouse or keyboard
                # print(event) # our actions are printed and these events have to be handled
                if event.type == pygame.QUIT: # if exit button is pressed
                    exit_game = True
                    
                if event.type == pygame.KEYDOWN: # if any keyboard key is pressed
                    if event.key == pygame.K_RIGHT: # if right arrow key is pressed. If the KEYDOWN is not checked, event.key will be inactive
                        velocity_x = init_velocity     
                        velocity_y = 0
                    if event.key == pygame.K_LEFT: 
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP: 
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN: 
                        velocity_y = init_velocity
                        velocity_x = 0
                            
            snake_x += velocity_x
            snake_y += velocity_y
                
            if abs(food_x - snake_x) < 6 and abs(food_y - snake_y) < 6:
                pygame.mixer.music.load("success.ogg") # load the music
                pygame.mixer.music.play() # play the music
                score += 10
                # print("Score: ", score)
                food_x = random.randint(50, screen_width - 50) # changing the food position
                food_y = random.randint(50, screen_height - 50)
                snake_length += 5
                if score > int(high_score):
                    high_score = score
                
            game_window.fill(white) # makes the window white            
            # making head of snake as rectangle(location_to_be_printed, color, [x_position, y_position, size, size])
            text_screen("Score: " + str(score), red, 5, 5) # printing score on screen
            text_screen("High Score: " + str(high_score), red, 5, 40) # printing score on screen
                
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
                
            if len(snake_list) > snake_length:
                snake_list.pop(0)
                
            if head in snake_list[:-1]: # if the snake collides with itself, i.e., coordinate of the head matches with any other element in the list
                game_over = True
                pygame.mixer.music.load("game_over.ogg") 
                pygame.mixer.music.play() 
            
            # print(snake_x, snake_y)    
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load("game_over.ogg") 
                pygame.mixer.music.play() 
                
            pygame.draw.rect(game_window, red, [food_x, food_y, snake_size, snake_size]) # plotting the food
            plot_snake(game_window, black, snake_list, snake_size) # plotting the snake
            
        pygame.display.update()
        await asyncio.sleep(0)
        clock.tick(fps)
        
    # After the user exits the game
    pygame.quit() # exit the pygame module
    sys.exit() # exit python
    
welcome()