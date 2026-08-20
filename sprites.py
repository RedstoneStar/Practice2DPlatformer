import pygame
import math
from settings import *

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE * 0.7, TILE_SIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawn_point = vec(x, y)
        
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
        self.is_grounded = False
        self.on_wall = 0 # -1 left, 1 right, 0 none
        self.jumps_left = 2
        
        # Powerup state
        self.speed_multiplier = 1.0

    def update(self, dt, platforms, hazards, enemies):
        self.acc = vec(0, GRAVITY)
        self.handle_input()
        
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc * dt
        
        # Wall sliding terminal velocity
        if self.on_wall != 0 and self.vel.y > 0:
            if self.vel.y > WALL_SLIDE_SPEED:
                self.vel.y = WALL_SLIDE_SPEED
        elif self.vel.y > TERMINAL_VELOCITY:
            self.vel.y = TERMINAL_VELOCITY
            
        # X collision
        self.pos.x += self.vel.x * dt + 0.5 * self.acc.x * (dt ** 2)
        self.rect.x = int(self.pos.x)
        self.check_collision(platforms, 'horizontal')

        # Y collision
        self.pos.y += self.vel.y * dt + 0.5 * self.acc.y * (dt ** 2)
        self.rect.y = int(self.pos.y)
        self.check_collision(platforms, 'vertical')
        
        # Death Checks
        if self.rect.top > len(LEVEL_MAP) * TILE_SIZE + 200 or \
           pygame.sprite.spritecollideany(self, hazards) or \
           pygame.sprite.spritecollideany(self, enemies):
            self.die()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -ACCELERATION * self.speed_multiplier
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = ACCELERATION * self.speed_multiplier
            
    def jump(self):
        if self.is_grounded or self.jumps_left > 0:
            self.vel.y = JUMP_STRENGTH
            self.is_grounded = False
            self.jumps_left -= 1
        elif self.on_wall != 0: # Wall Jump
            self.vel.y = WALL_JUMP_Y
            self.vel.x = -self.on_wall * WALL_JUMP_X
            self.on_wall = 0
            
    def jump_cut(self):
        if self.vel.y < JUMP_STRENGTH * 0.3:
            self.vel.y = JUMP_STRENGTH * 0.3

    def die(self):
        self.pos = vec(self.spawn_point.x, self.spawn_point.y)
        self.vel = vec(0, 0)
        self.rect.topleft = self.pos

    def check_collision(self, platforms, direction):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if direction == 'horizontal':
            self.on_wall = 0
            if hits:
                # Handle destructible platforms
                if getattr(hits[0], 'breakable', False):
                    hits[0].kill()
                    return
                
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                    self.on_wall = 1
                elif self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                    self.on_wall = -1
                self.vel.x = 0
                self.rect.x = int(self.pos.x)
                
        elif direction == 'vertical':
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                    self.is_grounded = True
                    self.jumps_left = 2
                    
                    # Attach to moving platforms
                    if getattr(hits[0], 'moving', False):
                        self.pos.x += hits[0].vel_x
                        
                elif self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = int(self.pos.y)
            else:
                if self.vel.y > 0:
                    self.is_grounded = False

# --- WORLD ENTITIES ---
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, breakable=False, moving=False):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(PLATFORM_COLOR if not breakable else (100, 100, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.breakable = breakable
        self.moving = moving
        self.vel_x = 2 if moving else 0
        self.start_x = x

    def update(self, dt):
        if self.moving:
            self.rect.x += self.vel_x
            if abs(self.rect.x - self.start_x) > 100:
                self.vel_x *= -1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE*0.8, TILE_SIZE*0.8))
        self.image.fill(ENEMY_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y + TILE_SIZE*0.2))
        self.speed = 100
        self.dir = 1
        self.start_x = x

    def update(self, dt):
        self.rect.x += self.speed * self.dir * dt
        if abs(self.rect.x - self.start_x) > 120:
            self.dir *= -1

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE*0.4, TILE_SIZE*0.4))
        self.image.fill(COIN_COLOR)
        self.rect = self.image.get_rect(center=(x + TILE_SIZE//2, y + TILE_SIZE//2))
        self.base_y = self.rect.y
        self.time = 0

    def update(self, dt):
        # Hover animation
        self.time += dt * 5
        self.rect.y = self.base_y + math.sin(self.time) * 5

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.life = 255

    def update(self, dt):
        self.life -= 400 * dt
        if self.life <= 0:
            self.kill()
        else:
            self.image.set_alpha(int(self.life))

class StaticEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, color, tag=""):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.tag = tag