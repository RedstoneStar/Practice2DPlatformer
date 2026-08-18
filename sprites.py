import pygame
from settings import *

# Vector2 allows for precise sub-pixel movement
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 48))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Vector positioning for fluid physics
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
        # State trackers
        self.is_grounded = False
        self.coyote_frames = 0
        self.jumps_left = 2

    def update(self, platforms):
        self.acc = vec(0, GRAVITY)
        self.handle_input()
        
        # Apply friction to the x-axis acceleration
        self.acc.x += self.vel.x * FRICTION
        
        # Update velocities via equations of motion
        self.vel += self.acc
        
        # Terminal velocity clamp
        if self.vel.y > TERMINAL_VELOCITY:
            self.vel.y = TERMINAL_VELOCITY
            
        # Update X position and check horizontal collisions
        self.pos.x += self.vel.x + 0.5 * self.acc.x
        self.rect.x = int(self.pos.x)
        self.check_collision(platforms, 'horizontal')

        # Update Y position and check vertical collisions
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.y = int(self.pos.y)
        self.check_collision(platforms, 'vertical')
        
        # Manage Coyote Time and Double Jumps
        if not self.is_grounded:
            self.coyote_frames -= 1
        else:
            self.coyote_frames = COYOTE_TIME_FRAMES
            self.jumps_left = 2 

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -ACCELERATION
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = ACCELERATION
            
    def jump(self):
        # Trigger jump if grounded, within coyote time, or if double jumps remain
        if self.is_grounded or self.coyote_frames > 0 or self.jumps_left > 0:
            self.vel.y = JUMP_STRENGTH
            self.is_grounded = False
            self.jumps_left -= 1
            self.coyote_frames = 0
            
    def jump_cut(self):
        # Variable jump height: releasing jump key cuts upward momentum
        if self.vel.y < -3:
            self.vel.y = -3

    def check_collision(self, platforms, direction):
        if direction == 'horizontal':
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                elif self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = int(self.pos.x)

        elif direction == 'vertical':
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                    self.vel.y = 0
                    self.is_grounded = True
                elif self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                    self.vel.y = 0
                self.rect.y = int(self.pos.y)
            else:
                # Disconnect from ground if falling
                if self.vel.y > 0:
                    self.is_grounded = False

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill(COIN_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))