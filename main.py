import pygame
import sys
from settings import *
from sprites import Player, Platform

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Practice 2D Platformer")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    player = Player(100, 300)
    all_sprites.add(player)

    level_data = [
        (0, 550, 800, 50),
        (200, 420, 200, 20),
        (450, 300, 180, 20),
        (150, 180, 150, 20)
    ]

    for p in level_data:
        plat = Platform(*p)
        all_sprites.add(plat)
        platforms.add(plat)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(platforms)

        screen.fill(BG_COLOR)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

import pygame
import sys
from settings import *
from sprites import Player, Platform

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Auto-Coded Platformer")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    player = Player(100, 300)
    all_sprites.add(player)

    level_data = [
        (0, 550, 800, 50),
        (200, 420, 200, 20),
        (450, 300, 180, 20),
        (150, 180, 150, 20)
    ]

    for p in level_data:
        plat = Platform(*p)
        all_sprites.add(plat)
        platforms.add(plat)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(platforms)

        screen.fill(BG_COLOR)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()





import pygame
import sys
from settings import *
from sprites import Player, Platform

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Auto-Coded Platformer")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    player = Player(100, 300)
    all_sprites.add(player)

    level_data = [
        (0, 550, 800, 50),
        (200, 420, 200, 20),
        (450, 300, 180, 20),
        (150, 180, 150, 20)
    ]

    for p in level_data:
        plat = Platform(*p)
        all_sprites.add(plat)
        platforms.add(plat)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(platforms)

        screen.fill(BG_COLOR)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()



import pygame
import sys
from settings import *
from sprites import Player, Platform

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Auto-Coded Platformer")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    player = Player(100, 300)
    all_sprites.add(player)

    level_data = [
        (0, 550, 800, 50),
        (200, 420, 200, 20),
        (450, 300, 180, 20),
        (150, 180, 150, 20)
    ]

    for p in level_data:
        plat = Platform(*p)
        all_sprites.add(plat)
        platforms.add(plat)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(platforms)

        screen.fill(BG_COLOR)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()




import pygame
import sys
from settings import *
from sprites import Player, Platform

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Auto-Coded Platformer")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    player = Player(100, 300)
    all_sprites.add(player)

    level_data = [
        (0, 550, 800, 50),
        (200, 420, 200, 20),
        (450, 300, 180, 20),
        (150, 180, 150, 20)
    ]

    for p in level_data:
        plat = Platform(*p)
        all_sprites.add(plat)
        platforms.add(plat)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(platforms)

        screen.fill(BG_COLOR)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()