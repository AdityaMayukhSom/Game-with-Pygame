import sys
import asyncio
import pygame

sys.path.append("scripts")
from environment import white, red, black, screen_width, screen_height
from welcome import welcome
from game_loop import game_loop

pygame.init()
# x = pygame.init() # returns a tuple (a, b), where a = number of initialized packages and b = number of errors. Used for testing purpose.
# print(x)
# Adding background music
pygame.mixer.init()
# makes the game window, 900, 500 are the height and width of the window
game_window = pygame.display.set_mode((screen_width, screen_height))
# Background Image
bg_img = pygame.image.load("snake.jpg")
# convert alpha sets the image so that the game speed is not slowed down
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height)).convert_alpha()
# Name of the game
pygame.display.set_caption("Snake Xenzia")  # sets the name of the game which will be visible on the top of game window
# pygame.display.update()  # update function has to be run to make the changes in the display visible. Otherwise the user cannot see it.
# Game specific variables
# To control the time within the game
clock = pygame.time.Clock()
# sets the font of the game. None means it takes default font of pygame and 55 is the fontsize
font = pygame.font.SysFont("calibri", 32)

exit_game = [False]


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)  # True is set to show high resolution things on low resolution
    game_window.blit(screen_text, [x, y])


def plot_snake(game_window, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(game_window, color, [x, y, snake_size, snake_size])


if __name__ == "__main__":
    welcome(game_window, text_screen, bg_img)
    while not exit_game[0]:
        pygame.display.update()
        clock.tick(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game[0] = True
                break
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                asyncio.run(game_loop(game_window, clock, exit_game, text_screen, plot_snake))
                # pygame.mixer.music.load("success.ogg") # load the music
                # pygame.mixer.music.play() # play the music

    # After the user exits the game
    pygame.quit()  # exit the pygame module
    sys.exit()  # exit python
