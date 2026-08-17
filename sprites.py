import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 48))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.vel_x = 0
        self.is_grounded = False

    def update(self, platforms):
        self.handle_input()
        self.apply_gravity()
        self.rect.x += self.vel_x
        self.check_collision(platforms, 'horizontal')
        self.rect.y += self.vel_y
        self.check_collision(platforms, 'vertical')

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.is_grounded:
            self.vel_y = JUMP_STRENGTH
            self.is_grounded = False

    def apply_gravity(self):
        self.vel_y += GRAVITY

    def check_collision(self, platforms, direction):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if direction == 'horizontal':
                    if self.vel_x > 0: self.rect.right = platform.rect.left
                    if self.vel_x < 0: self.rect.left = platform.rect.right
                elif direction == 'vertical':
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
                        self.is_grounded = True
                    if self.vel_y < 0:
                        self.rect.top = platform.rect.bottom
                        self.vel_y = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))