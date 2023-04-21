import pygame
from environment import snakeSize


class Snake(pygame.sprite.Sprite):
    size = snakeSize
    initialVelocity = 5

    def __init__(self):
        super().__init__()
        self.x = 45
        self.y = 55

        self.list = []
        self.length = 1

        self.velocityX = 0
        self.velocityY = 0

    def handleDirection(self, eventKey: int):
        if eventKey == pygame.K_UP:
            self.velocityX = 0
            self.velocityY = -Snake.initialVelocity
        elif eventKey == pygame.K_RIGHT:
            self.velocityX = Snake.initialVelocity
            self.velocityY = 0
        elif eventKey == pygame.K_DOWN:
            self.velocityX = 0
            self.velocityY = Snake.initialVelocity
        elif eventKey == pygame.K_LEFT:
            self.velocityX = -Snake.initialVelocity
            self.velocityY = 0

    def slither(self):
        self.x += self.velocityX
        self.y += self.velocityY

    def increaseLength(self, increment: int = 10):
        self.length += increment
