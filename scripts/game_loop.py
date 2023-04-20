import random
import os
import pygame
import asyncio

from environment import white, red, black, screen_width, screen_height


# Creating game loop
async def game_loop(game_window, clock, exit_game, text_screen, plot_snake):
    # Game specific variables
    # when this becomes true, we will ask whether he wants to quit the game or play another round
    game_over = False
    snake_x, snake_y = 45, 55

    # initial size of snake is 10px
    snake_size = 10
    init_velocity, velocity_x, velocity_y = 5, 0, 0

    snake_list = []
    snake_length = 1

    # plots the food anywhere
    food_x, food_y = random.randint(50, screen_width - 50), random.randint(50, screen_height - 50)

    # fps = frame per second
    score, fps = 0, 30

    if not os.path.exists("high_score.txt"):
        with open("high_score.txt", "w") as f:
            f.write("0")

    with open("high_score.txt", "r") as f:
        high_score = f.read()

    while not exit_game[0]:  # this loop is created so that the game window stays till the user exits it
        if game_over:
            with open("high_score.txt", "w") as f:
                f.write(str(high_score))

            game_window.fill(white)
            text_screen("Game Over! Press Enter to Continue.", red, 150, 220)
            break

        for event in pygame.event.get():  # this consists of all the activities we do with the mouse or keyboard
            # print(event) # our actions are printed and these events have to be handled
            if event.type == pygame.QUIT:  # if exit button is pressed
                exit_game[0] = True
                break
            elif event.type == pygame.KEYDOWN:
                # if any keyboard key is pressed
                # If the KEYDOWN is not checked, event.key will be inactive
                if event.key == pygame.K_RIGHT:
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

        if exit_game[0]:
            break

        snake_x += velocity_x
        snake_y += velocity_y

        if abs(food_x - snake_x) < 6 and abs(food_y - snake_y) < 6:
            pygame.mixer.music.load("music/success.ogg")  # load the music
            pygame.mixer.music.play()  # play the music
            score += 10
            # print("Score: ", score)
            food_x = random.randint(50, screen_width - 50)  # changing the food position
            food_y = random.randint(50, screen_height - 50)
            snake_length += 5
            if score > int(high_score):
                high_score = score

        game_window.fill(white)  # makes the window white

        # making head of snake as rectangle(location_to_be_printed, color, [x_position, y_position, size, size])
        text_screen("Score: " + str(score), red, 5, 5)  # printing score on screen
        text_screen("High Score: " + str(high_score), red, 5, 40)  # printing score on screen

        head = []
        head.append(snake_x)
        head.append(snake_y)
        snake_list.append(head)

        if len(snake_list) > snake_length:
            snake_list.pop(0)

        if head in snake_list[:-1] or snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
            # if the snake collides with itself, i.e., coordinate of the head matches with any other element in the list
            game_over = True
            pygame.mixer.music.load("music/game_over.ogg")
            pygame.mixer.music.play()

        pygame.draw.rect(game_window, red, [food_x, food_y, snake_size, snake_size])  # plotting the food

        # plotting the snake
        plot_snake(game_window, black, snake_list, snake_size)

        pygame.display.update()
        clock.tick(fps)
        await asyncio.sleep(0)
