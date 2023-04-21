import random
import pygame
from environment import foodSize
from environment import screenWidth, screenHeight


class Food(pygame.sprite.Sprite):
    size = foodSize

    def __init__(self):
        super().__init__()
        self.x = random.randint(50, screenWidth - 50)
        self.y = random.randint(50, screenHeight - 50)

    def changePosition(self):
        self.x = random.randint(50, screenWidth - 50)
        self.y = random.randint(50, screenHeight - 50)
