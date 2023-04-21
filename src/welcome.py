from environment import white, red, black, screen_width, screen_height


def welcome(game_window, text_screen, bg_img):
    game_window.fill(white)
    game_window.blit(bg_img, (0, 0))

    text_screen("Welcome to Snake Xenzia", red, 200, 150)
    text_screen("Press Spacebar to continue", red, 200, 200)
