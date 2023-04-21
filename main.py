import sys
import asyncio
import pygame

sys.path.append("src")
from environment import fps, screenWidth, screenHeight, gameTitle
from GameLoop import gameLoop
from Window import Window


async def main():
    window = Window(gameTitle, screenWidth, screenHeight)

    # Game greetings
    window.showGreetings()

    while True:
        window.clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                gameLoop(window)
                # if gameloop is running, no need to run the outer loop
                window.clock.tick(0)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
