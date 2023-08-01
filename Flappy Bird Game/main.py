import random
import sys
import pygame
from pygame.locals import *

# Global game variables
fps = 32  # number of images changing per second. Fo fps >= 32, images change is not visible, it seems as if game is going on
screen_width = 289
screen_height = 511
screen = pygame.display.set_mode((screen_width, screen_height))
ground_y = screen_height * 0.8
game_images = {}
game_sounds = {}
player = "assets/images/bird.jpg"
background = "assets/images/background.png"
pipe_img = "assets/images/pipe.jpg"


def welcome_screen():
    player_x = screen_width // 5
    player_y = (screen_height - game_images["player"].get_height()) // 2
    message_x = (screen_width - game_images["message"].get_height()) // 2
    message_y = int(screen_height * 0.4)
    ground_x = 0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run = False
                return
            else:
                screen.blit(game_images["background"], (0, 0))
                screen.blit(game_images["player"], (player_x, player_y))
                screen.blit(game_images["message"], (message_x, message_y))
                screen.blit(game_images["ground"], (ground_x, ground_y))
                pygame.display.update()
                fps_clock.tick(fps)

def main_game():
    score = 0
    player_x = screen_width // 5
    player_y = screen_width // 5
    ground_x = 0
    new_pipe1 = get_random_pipe()
    new_pipe2 = get_random_pipe()
    upper_pipes = [
        {"x": screen_width + 200, "y": new_pipe1[0]["y"]},
        {"x": screen_width + 200 + screen_width / 2, "y": new_pipe1[1]["y"]}
    ]
    lower_pipes = [
        {"x": screen_width + 200, "y": new_pipe2[0]["y"]},
        {"x": screen_width + 200 + screen_width / 2, "y": new_pipe2[1]["y"]}
    ]
    pipe_velocity_x = -4
    player_velocity_y = -9  # velocity with which bird is falling
    player_max_velocity_y = 10 # max velocity of bird even after pressing up arrow key many times so that bird does not fly away
    player_min_velocity_y = -8
    player_acceleration_y = 1
    player_flap_acceleration_velocity = -8  # velocity of bird while flapping
    player_flapped = False  # It is true when the bird is flapping
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                if player_y > 0:
                    player_velocity_y = player_flap_acceleration_velocity
                    player_flapped = True
                    game_sounds["swoosh"].play()
        # will return true if the player is crashed
        crash_test = is_collide(player_x, player_y, upper_pipes, lower_pipes)
        if crash_test:
            return
        # checking for score
        player_mid_pos = player_x + game_images["player"].get_width() // 2
        for pipe in upper_pipes:
            pipe_mid_pos = pipe["x"] + game_images["pipe"][0].get_width() // 2
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
                score += 1
                print(f"Your score is {score}")
                game_sounds["point"].play()
        if player_velocity_y < player_max_velocity_y and not player_flapped:
            player_velocity_y += player_acceleration_y
        if player_flapped:
            player_flapped = False
        player_height = game_images["player"].get_height()
        player_y = player_y + min(player_velocity_y, ground_y - player_y - player_height)

        # move pipes to the left
        for upperpipe, lowerpipe in zip(upper_pipes, lower_pipes):
            upperpipe["x"] += pipe_velocity_x
            lowerpipe["x"] += pipe_velocity_x
        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upper_pipes[0]["x"] < 5:
            newpipe = get_random_pipe()
            upper_pipes.append(newpipe[0])
            lower_pipes.append(newpipe[1])
        # if the pipe is out of the screen, remove it
        if upper_pipes[0]["x"] < -game_images["pipe"][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)
            
        # images blit
        screen.blit(game_images["background"], (0, 0))
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            screen.blit(game_images["pipe"][0], (upper_pipe["x"], upper_pipe["y"]))
            screen.blit(game_images["pipe"][1], (lower_pipe["x"], lower_pipe["y"]))

        screen.blit(game_images["ground"], (ground_x, ground_y))
        screen.blit(game_images["player"], (player_x, player_y))
        my_digits = [int(x) for x in list(str(score))]
        width = 0
        for digit in my_digits:
            actual_width = game_images["numbers"][digit].get_width()
            actual_height = game_images["numbers"][digit].get_height()
            game_images["numbers"][digit] = pygame.transform.scale(game_images["numbers"][digit], (actual_width // 10, actual_height // 20)) 
            width += game_images["numbers"][digit].get_width()
        x_offset = (screen_width - width) / 2

        for digit in my_digits:
            screen.blit(game_images["numbers"][digit], (x_offset, screen_height * 0.012))
            x_offset += game_images["numbers"][digit].get_width()
        pygame.display.update()
        fps_clock.tick(fps)

def is_collide(player_x, player_y, upper_pipes, lower_pipes):
    if player_y > ground_y - 25 or player_y < 0:
        game_sounds["hit"].play()
        return True
    for pipe in upper_pipes:
        pipe_height = game_images["pipe"][0].get_height()
        if player_y < pipe_height + pipe["y"] and abs(player_x - game_images["pipe"][0].get_width()) < 0.5:
            game_sounds["hit"].play()
            return True
    for pipe in lower_pipes:
        if  abs(player_x - game_images["pipe"][0].get_width()) < 0.5:
            game_sounds["hit"].play()
            return True
    return False

def get_random_pipe():
    pipe_height = game_images["pipe"][0].get_height()
    minimum_gap = screen_height // 3
    pipe_x = screen_width + 10
    pipe_y_lower = minimum_gap + random.randrange(
        0, int(screen_height - game_images["ground"].get_height() - 1.2 * minimum_gap))
    pipe_y_upper = minimum_gap - pipe_y_lower + pipe_height
    pipe = [
        {"x": pipe_x, "y": -pipe_y_upper},  # upper pipe
        {"x": pipe_x, "y": pipe_y_lower}  # lower pipe
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()
    fps_clock = pygame.time.Clock()  # controls fps of the game
    pygame.display.set_caption("Flappy Bird Game")
    game_images["numbers"] = [
        pygame.image.load("assets/images/0.png").convert_alpha(),
        pygame.image.load("assets/images/1.png").convert_alpha(),
        pygame.image.load("assets/images/2.png").convert_alpha(),
        pygame.image.load("assets/images/3.png").convert_alpha(),
        pygame.image.load("assets/images/4.png").convert_alpha(),
        pygame.image.load("assets/images/5.png").convert_alpha(),
        pygame.image.load("assets/images/6.png").convert_alpha(),
        pygame.image.load("assets/images/7.png").convert_alpha(),
        pygame.image.load("assets/images/8.png").convert_alpha(),
        pygame.image.load("assets/images/9.png").convert_alpha()
    ]

    # Game images
    game_images["message"] = pygame.image.load("assets/images/message.png").convert_alpha()
    game_images["ground"] = pygame.image.load("assets/images/ground.png").convert_alpha()
    game_images["pipe"] = (pygame.transform.rotate(pygame.image.load(pipe_img).convert_alpha(), 180),
                           pygame.image.load(pipe_img).convert_alpha())

    # Game sounds
    game_sounds["die"] = pygame.mixer.Sound("assets/audio/die.wav")
    game_sounds["hit"] = pygame.mixer.Sound("assets/audio/hit.wav")
    game_sounds["point"] = pygame.mixer.Sound("assets/audio/point.wav")
    game_sounds["swoosh"] = pygame.mixer.Sound("assets/audio/swoosh.wav")
    
    game_images["background"] = pygame.image.load(background).convert()
    game_images["player"] = pygame.image.load(player).convert_alpha()

    while True:
        welcome_screen()
        main_game()