import random

from environment import foodSize
from environment import screenWidth, screenHeight


class Food:
    size = foodSize

    x = random.randint(50, screenWidth - 50)
    y = random.randint(50, screenHeight - 50)

    def changePosition(self):
        self.x = random.randint(50, screenWidth - 50)
        self.y = random.randint(50, screenHeight - 50)
