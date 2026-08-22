import pygame
import math
import random
from settings import *

vec = pygame.math.Vector2

class Trail(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, width, height), border_radius=8)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.alpha = 150

    def update(self, dt):
        self.alpha -= 600 * dt
        if self.alpha <= 0:
            self.kill()
        else:
            self.image.set_alpha(int(self.alpha))

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color):
        super().__init__()
        font = pygame.font.SysFont("Arial", 20, bold=True)
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_y = -80
        self.life = 255
        self.base_image = self.image.copy()

    def update(self, dt):
        self.rect.y += self.vel_y * dt
        self.life -= 250 * dt
        if self.life <= 0:
            self.kill()
        else:
            self.image = self.base_image.copy()
            self.image.set_alpha(int(self.life))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE * 0.7, TILE_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.spawn_point = vec(x, y)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
        self.is_grounded = False
        self.on_wall = 0 
        self.jumps_left = 2
        
        self.coyote_timer = 0
        self.jump_buffer = 0
        self.dash_cd = 0
        self.facing_right = True

    def update(self, dt, platforms, hazards, enemies, game):
        self.acc = vec(0, GRAVITY)
        self.coyote_timer -= dt
        self.jump_buffer -= dt
        self.dash_cd -= dt
        
        self.handle_input(dt, game)
        
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc * dt
        
        if self.on_wall != 0 and self.vel.y > 0:
            self.vel.y = min(self.vel.y, WALL_SLIDE_SPEED)
            if random.random() < 0.3:
                game.particles.add(Particle(self.rect.centerx, self.rect.bottom, (200, 200, 200)))
        else:
            self.vel.y = min(self.vel.y, TERMINAL_VELOCITY)
            
        # X collision
        self.pos.x += self.vel.x * dt + 0.5 * self.acc.x * (dt ** 2)
        self.rect.x = int(self.pos.x)
        self.check_collision(platforms, 'horizontal')

        # Y collision
        self.pos.y += self.vel.y * dt + 0.5 * self.acc.y * (dt ** 2)
        self.rect.y = int(self.pos.y)
        self.check_collision(platforms, 'vertical')
        
        if self.is_grounded:
            self.coyote_timer = 0.2 

        if self.jump_buffer > 0 and (self.coyote_timer > 0 or self.jumps_left > 0):
            self.execute_jump(game)
            
        self.draw_player()
        
        if abs(self.vel.x) > 600:
            game.particles.add(Trail(self.rect.x, self.rect.y, self.rect.width, self.rect.height, PLAYER_DASH_COLOR))

        if self.rect.top > len(LEVEL_1) * TILE_SIZE + 200 or pygame.sprite.spritecollideany(self, hazards) or pygame.sprite.spritecollideany(self, enemies):
            self.die(game)

    def draw_player(self):
        self.image.fill((0,0,0,0))
        color = PLAYER_COLOR if self.jumps_left > 0 else (30, 150, 30)
        # Glow if dash is ready
        if self.dash_cd <= 0:
            pygame.draw.rect(self.image, (100, 255, 100, 100), (-2, -2, self.rect.width+4, self.rect.height+4), border_radius=10)
        pygame.draw.rect(self.image, color, (0, 0, self.rect.width, self.rect.height), border_radius=8)

    def handle_input(self, dt, game):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -ACCELERATION
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = ACCELERATION
            self.facing_right = True
            
        if keys[pygame.K_LSHIFT] and self.dash_cd <= 0:
            self.vel.x = 1400 * (1 if self.facing_right else -1)
            self.vel.y = 0
            self.dash_cd = 1.2
            game.camera.shake = 0.15

    def jump(self):
        self.jump_buffer = 0.15
            
    def execute_jump(self, game):
        self.vel.y = JUMP_STRENGTH
        self.is_grounded = False
        self.coyote_timer = 0
        self.jump_buffer = 0
        self.jumps_left -= 1
        for _ in range(5):
            game.particles.add(Particle(self.rect.centerx, self.rect.bottom, (200, 200, 200)))
            
        if self.on_wall != 0: 
            self.vel.x = -self.on_wall * WALL_JUMP_X
            self.on_wall = 0

    def jump_cut(self):
        if self.vel.y < JUMP_STRENGTH * 0.3:
            self.vel.y = JUMP_STRENGTH * 0.3

    def die(self, game):
        for _ in range(20):
             game.particles.add(Particle(self.rect.centerx, self.rect.centery, PLAYER_COLOR))
        self.pos = vec(self.spawn_point.x, self.spawn_point.y)
        self.vel = vec(0, 0)
        self.rect.topleft = self.pos
        self.dash_cd = 0
        game.camera.shake = 0.4 

    def check_collision(self, platforms, direction):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if direction == 'horizontal':
            self.on_wall = 0
            if hits:
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
                    if getattr(hits[0], 'moving', False):
                        self.pos.x += hits[0].vel_x
                elif self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = int(self.pos.y)
            else:
                if self.vel.y > 0 and self.coyote_timer <= 0:
                    self.is_grounded = False

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, breakable=False, moving=False):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE + 10), pygame.SRCALPHA)
        color = (160, 140, 100) if breakable else PLATFORM_COLOR
        pygame.draw.rect(self.image, (0,0,0, 80), (3, TILE_SIZE//2, TILE_SIZE-6, TILE_SIZE//2 + 8), border_radius=6)
        pygame.draw.rect(self.image, color, (0, 0, TILE_SIZE, TILE_SIZE), border_radius=6)
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.breakable = breakable
        self.moving = moving
        self.vel_x = 3 if moving else 0
        self.start_x = x

    def update(self, dt):
        if self.moving:
            self.rect.x += self.vel_x
            if abs(self.rect.x - self.start_x) > 150:
                self.vel_x *= -1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE*0.8, TILE_SIZE*0.8 + 10), pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y + TILE_SIZE*0.2, TILE_SIZE*0.8, TILE_SIZE*0.8)
        self.base_speed = 80
        self.dir = 1
        self.vel_y = 0
        self.is_aggro = False

    def update(self, dt, player, platforms):
        dist_x = player.rect.centerx - self.rect.centerx
        dist_y = player.rect.centery - self.rect.centery
        
        self.is_aggro = abs(dist_x) < 250 and abs(dist_y) < 150
        
        if self.is_aggro:
            speed = self.base_speed * 2.2
            color = (255, 80, 80)
            target_dir = 1 if dist_x > 0 else -1
            self.dir = target_dir
        else:
            speed = self.base_speed
            color = ENEMY_COLOR
            
        self.vel_y += GRAVITY * dt
        self.rect.y += self.vel_y * dt
        
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            if self.vel_y > 0:
                self.rect.bottom = hits[0].rect.top
                self.vel_y = 0

        self.image.fill((0,0,0,0))
        pygame.draw.rect(self.image, (0,0,0, 60), (2, self.rect.height-2, self.rect.width-4, 8), border_radius=10)
        pygame.draw.rect(self.image, color, (0, 0, self.rect.width, self.rect.height), border_radius=10)
        eye_x = 18 if self.dir == 1 else 6
        pygame.draw.rect(self.image, (255,255,255), (eye_x, 8, 8, 8), border_radius=2)
        if self.is_aggro:
            pygame.draw.rect(self.image, (255,0,0), (eye_x+2, 10, 4, 4))
        
        probe_x = self.rect.right + 5 if self.dir == 1 else self.rect.left - 15
        probe_floor = pygame.Rect(probe_x, self.rect.bottom + 5, 10, 10)
        probe_wall = pygame.Rect(probe_x, self.rect.centery, 10, 10)
        
        floor_hit = any(p.rect.colliderect(probe_floor) for p in platforms)
        wall_hit = any(p.rect.colliderect(probe_wall) for p in platforms)
        
        if not floor_hit or wall_hit:
            if self.is_aggro and self.vel_y == 0:
                self.vel_y = JUMP_STRENGTH * 0.85
            elif not self.is_aggro:
                self.dir *= -1
                
        self.rect.x += speed * self.dir * dt

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE*1.5, TILE_SIZE*1.5), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x + TILE_SIZE//2, y + TILE_SIZE//2))
        self.base_y = self.rect.y
        self.time = random.uniform(0, 10)

    def update(self, dt):
        self.time += dt * 5
        pulse = abs(math.sin(self.time * 2)) * 6
        self.image.fill((0,0,0,0))
        center = TILE_SIZE * 0.75
        pygame.draw.circle(self.image, (255, 215, 0, 60), (center, center), 14 + pulse)
        pygame.draw.circle(self.image, (255, 255, 200, 120), (center, center), 10 + pulse/2)
        pygame.draw.circle(self.image, COIN_COLOR, (center, center), 8)
        self.rect.y = self.base_y + math.sin(self.time) * 10

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.color = color
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = vec(random.uniform(-200, 200), random.uniform(-300, -50))
        self.life = 255

    def update(self, dt):
        self.vel.y += GRAVITY * 0.6 * dt 
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt
        self.life -= 400 * dt
        if self.life <= 0:
            self.kill()
        else:
            self.image.fill((0,0,0,0))
            size = max(2, int((self.life / 255) * 5))
            pygame.draw.circle(self.image, (*self.color[:3], int(self.life)), (5, 5), size)

class StaticEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, color, tag=""):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE + 10), pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.tag = tag
        if tag == "HAZARD":
            pygame.draw.polygon(self.image, (150, 0, 0, 150), [(0, TILE_SIZE+5), (TILE_SIZE//2, TILE_SIZE//2+5), (TILE_SIZE, TILE_SIZE+5)])
            pygame.draw.polygon(self.image, HAZARD_COLOR, [(0, TILE_SIZE), (TILE_SIZE//2, TILE_SIZE//2), (TILE_SIZE, TILE_SIZE)])
        else:
            pygame.draw.rect(self.image, (0,0,0, 80), (3, TILE_SIZE//2, TILE_SIZE-6, TILE_SIZE//2 + 8), border_radius=6)
            pygame.draw.rect(self.image, color, (0,0,TILE_SIZE,TILE_SIZE), border_radius=4)