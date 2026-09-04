import pygame
import math
import random
from settings import *

def draw_shadow(surface, rect, radius=0):
    shadow = pygame.Surface((rect.width, rect.height + 10), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0, 0, 0, 80), shadow.get_rect(), border_radius=radius)
    surface.blit(shadow, (rect.x, rect.y + 6))

class LimitBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

class Trail(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.alpha = 180

    def update(self, delta_time):
        self.alpha -= 800 * delta_time
        if self.alpha <= 0:
            self.kill()
        else:
            self.image.set_alpha(int(self.alpha))

class PopupText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color, is_tutorial=False):
        super().__init__()
        
        if is_tutorial:
            size = 20
        else:
            size = 22
            
        font = pygame.font.SysFont("Trebuchet MS", size, bold=True)
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.is_tutorial = is_tutorial
        
        if is_tutorial:
            self.vel_y = 0
        else:
            self.vel_y = -100
            
        self.life = 255
        self.base_image = self.image.copy()

    def update(self, delta_time):
        if not self.is_tutorial:
            self.rect.y += self.vel_y * delta_time
            self.life -= 300 * delta_time
            if self.life <= 0:
                self.kill()
            else:
                self.image = self.base_image.copy()
                self.image.set_alpha(int(self.life))
        else:
            self.rect.y += math.sin(pygame.time.get_ticks() / 200.0) * 0.5

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = int(TILE_SIZE * 0.7)
        self.height = TILE_SIZE
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.spawn_point = pygame.math.Vector2(x, y)
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        
        self.is_grounded = False
        self.standing_on = None 
        self.on_wall = 0 
        self.jumps_left = 2
        
        self.coyote_timer = 0
        self.jump_buffer = 0
        self.dash_cd = 0
        self.facing_right = True
        
        self.scale_x = 1.0
        self.scale_y = 1.0

    def update(self, delta_time, platforms, hazards, enemies, springs, game):
        self.acc = pygame.math.Vector2(0, GRAVITY)
        
        self.coyote_timer -= delta_time
        self.jump_buffer -= delta_time
        self.dash_cd -= delta_time
        
        self.scale_x += (1.0 - self.scale_x) * 12 * delta_time
        self.scale_y += (1.0 - self.scale_y) * 12 * delta_time
        
        self.handle_input(delta_time, game)
        
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc * delta_time
        
        if self.on_wall != 0 and self.vel.y > 0:
            self.vel.y = min(self.vel.y, WALL_SLIDE_SPEED)
            if random.random() < 0.05:
                p = Particle(self.rect.centerx, self.rect.bottom, (200, 200, 200))
                game.particles.add(p)
        else:
            self.vel.y = min(self.vel.y, TERMINAL_VELOCITY)
            
        if self.is_grounded and self.standing_on != None:
            self.pos.x += self.standing_on.dx
            self.rect.x = int(self.pos.x)
            
        self.pos.x += self.vel.x * delta_time + 0.5 * self.acc.x * (delta_time ** 2)
        self.rect.x = int(self.pos.x)
        self.check_collision(platforms, 'horizontal', game, delta_time)

        self.pos.y += self.vel.y * delta_time + 0.5 * self.acc.y * (delta_time ** 2)
        self.rect.y = int(self.pos.y)
        self.check_collision(platforms, 'vertical', game, delta_time)
        
        if self.is_grounded:
            self.coyote_timer = 0.15 

        if self.jump_buffer > 0 and (self.coyote_timer > 0 or self.jumps_left > 0 or self.on_wall != 0):
            self.execute_jump(game)
            
        self.check_combat(enemies, game)
        self.check_springs(springs, game)
        
        self.draw_player()
        
        if abs(self.vel.x) > 800:
            trail = Trail(self.rect.x, self.rect.y, self.rect.width, self.rect.height, PLAYER_DASH_COLOR)
            game.particles.add(trail)

        if self.rect.top > len(LEVEL_1) * TILE_SIZE + 400 or pygame.sprite.spritecollideany(self, hazards):
            self.die(game)

    def draw_player(self):
        self.image = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
        
        if self.jumps_left > 0:
            color = PLAYER_COLOR
        else:
            color = (30, 140, 100)
            
        if self.dash_cd > 0 and self.dash_cd > 0.7:
            color = (255, 255, 255)
            
        dw = self.width * self.scale_x
        dh = self.height * self.scale_y
        
        dy = (self.height + 10 - dh) / 2 + (self.height - dh)
        
        if self.is_grounded and abs(self.vel.x) < 5:
            breath = math.sin(pygame.time.get_ticks() / 150.0) * 2.5
            dh -= breath
            dy += breath

        dx = (self.width + 10 - dw) / 2
        
        if self.facing_right:
            back_x = dx - 4 
        else:
            back_x = dx + dw
            
        pygame.draw.rect(self.image, (max(0, color[0]-40), max(0, color[1]-40), max(0, color[2]-40)), (back_x, dy + 8, 4, dh - 16))
        pygame.draw.rect(self.image, color, (dx, dy, dw, dh), border_radius=4)
        
        if self.facing_right:
            eye_x = dx + dw - 14
        else:
            eye_x = dx + 4
            
        pygame.draw.rect(self.image, (20, 20, 30), (eye_x, dy + 6, 10, 10), border_radius=2)
        
        if self.facing_right:
            pupil_offset = 4
        else:
            pupil_offset = 2
            
        pygame.draw.rect(self.image, (0, 255, 255), (eye_x + pupil_offset, dy + 8, 4, 4))

    def handle_input(self, delta_time, game):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -ACCELERATION
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = ACCELERATION
            self.facing_right = True
            
        if keys[pygame.K_LSHIFT] and self.dash_cd <= 0:
            if self.facing_right:
                self.vel.x = DASH_SPEED
            else:
                self.vel.x = -DASH_SPEED
            self.vel.y = 0
            self.dash_cd = 1.0
            
            self.scale_x = 1.7
            self.scale_y = 0.35
            game.camera.shake = 0.2

    def jump(self):
        self.jump_buffer = 0.15
            
    def execute_jump(self, game):
        self.vel.y = JUMP_STRENGTH
        self.is_grounded = False
        self.standing_on = None
        self.coyote_timer = 0
        self.jump_buffer = 0
        
        self.scale_x = 0.55
        self.scale_y = 1.45
        
        for i in range(2):
            p = Particle(self.rect.centerx, self.rect.bottom, (200, 200, 200))
            game.particles.add(p)
            
        if self.on_wall != 0: 
            self.vel.x = -self.on_wall * WALL_JUMP_X
            self.on_wall = 0
            self.jumps_left = 1 
        else:
            self.jumps_left -= 1

    def jump_cut(self):
        if self.vel.y < JUMP_STRENGTH * 0.3:
            self.vel.y = JUMP_STRENGTH * 0.3

    def die(self, game):
        for i in range(10):
             p = Particle(self.rect.centerx, self.rect.centery, PLAYER_COLOR)
             game.particles.add(p)
             
        self.pos = pygame.math.Vector2(self.spawn_point.x, self.spawn_point.y)
        self.vel = pygame.math.Vector2(0, 0)
        self.rect.topleft = self.pos
        self.dash_cd = 0
        game.camera.shake = 0.5 

    def shatter_block(self, block, game):
        block.kill()
        game.camera.shake = 0.3
        for i in range(3):
            p = Particle(block.rect.centerx, block.rect.centery, block.color)
            game.particles.add(p)

    def check_collision(self, platforms, direction, game, delta_time):
        if direction == 'horizontal':
            hits = pygame.sprite.spritecollide(self, platforms, False)
            self.on_wall = 0
            hit_block = None
            
            for block in hits:
                if block.breakable and abs(self.vel.x) > 800:
                    self.shatter_block(block, game)
                else:
                    hit_block = block
                    break
                    
            if hit_block:
                if self.vel.x > 0:
                    self.pos.x = hit_block.rect.left - self.rect.width
                    self.on_wall = 1
                elif self.vel.x < 0:
                    self.pos.x = hit_block.rect.right
                    self.on_wall = -1
                    
                self.vel.x = 0
                self.rect.x = int(self.pos.x)
                
        elif direction == 'vertical':
            hit_block = None
            self.standing_on = None 
            
            if self.vel.y >= 0:
                self.rect.y += 2
                
            hits = pygame.sprite.spritecollide(self, platforms, False)
            
            if self.vel.y >= 0:
                self.rect.y -= 2
            
            for block in hits:
                if block.breakable and self.vel.y < 0:
                    self.shatter_block(block, game)
                    self.vel.y = 0 
                    return
                else:
                    hit_block = block
                    break
                    
            if hit_block:
                if self.vel.y > 0:
                    self.pos.y = hit_block.rect.top - self.rect.height
                    
                    if not self.is_grounded:
                        self.scale_x = 1.45
                        self.scale_y = 0.55
                        if self.vel.y > 600:
                            game.camera.shake = 0.15
                            
                    self.is_grounded = True
                    self.jumps_left = 2
                    self.standing_on = hit_block
                        
                elif self.vel.y < 0:
                    self.pos.y = hit_block.rect.bottom
                    
                self.vel.y = 0
                self.rect.y = int(self.pos.y)
                
            else:
                if self.vel.y > 0 and self.coyote_timer <= 0:
                    self.is_grounded = False

    def check_combat(self, enemies, game):
        hits = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in hits:
            if self.vel.y > 0 and self.rect.bottom < enemy.rect.centery + 15:
                self.vel.y = JUMP_STRENGTH * 0.85
                self.jumps_left = 1
                enemy.take_damage(game)
            else:
                self.die(game)
                
    def check_springs(self, springs, game):
        hits = pygame.sprite.spritecollide(self, springs, False)
        for spring in hits:
            if self.vel.y > 0:
                self.vel.y = SPRING_STRENGTH
                self.jumps_left = 2
                self.scale_x = 0.35
                self.scale_y = 1.85
                game.camera.shake = 0.3
                spring.trigger()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, breakable=False, moving=False):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.breakable = breakable
        self.moving = moving
        
        if breakable:
            self.color = (180, 100, 60)
        elif moving:
            self.color = (200, 180, 50)
        else:
            self.color = PLATFORM_COLOR
        
        pygame.draw.rect(self.image, self.color, (0, 0, TILE_SIZE, TILE_SIZE))
        
        if breakable:
            pygame.draw.line(self.image, (80, 40, 20), (10, 0), (20, 20), 3)
            pygame.draw.line(self.image, (80, 40, 20), (20, 20), (10, 40), 3)
            pygame.draw.line(self.image, (80, 40, 20), (20, 20), (35, 15), 3)
            pygame.draw.rect(self.image, (80, 40, 20), (0, 0, TILE_SIZE, TILE_SIZE), 2)
        elif moving:
            for i in range(-TILE_SIZE, TILE_SIZE, 10):
                pygame.draw.line(self.image, (40, 40, 40), (i, 0), (i+TILE_SIZE, TILE_SIZE), 4)
            pygame.draw.rect(self.image, (255, 255, 255), (0, 0, TILE_SIZE, 4))
            pygame.draw.rect(self.image, (40, 40, 40), (0, 0, TILE_SIZE, TILE_SIZE), 2)
        else:
            r = min(255, self.color[0]+40)
            g = min(255, self.color[1]+40)
            b = min(255, self.color[2]+40)
            pygame.draw.rect(self.image, (r, g, b), (0, 0, TILE_SIZE, 4))
            
            dr = max(0, self.color[0]-40)
            dg = max(0, self.color[1]-40)
            db = max(0, self.color[2]-40)
            pygame.draw.rect(self.image, (dr, dg, db), (0, TILE_SIZE-6, TILE_SIZE, 6))
            pygame.draw.rect(self.image, (30, 40, 50), (0, 0, TILE_SIZE, TILE_SIZE), 2)

        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.pos = pygame.math.Vector2(x, y) 
        
        if moving:
            self.vel_x = 140 
        else:
            self.vel_x = 0
            
        self.dx = 0

    def update(self, delta_time, platforms=None, limits=None):
        self.dx = 0
        
        if self.moving:
            old_x = self.rect.x
            self.pos.x += self.vel_x * delta_time
            self.rect.x = int(self.pos.x)
            
            reverse = False
            
            if limits and pygame.sprite.spritecollideany(self, limits):
                reverse = True
            
            if platforms and not reverse:
                for p in platforms:
                    if p != self and self.rect.colliderect(p.rect):
                        reverse = True
                        break
                        
            if reverse:
                self.vel_x *= -1
                self.pos.x += self.vel_x * delta_time 
                self.rect.x = int(self.pos.x)
                
            self.dx = self.rect.x - old_x

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, etype="red"):
        super().__init__()
        self.etype = etype
        
        if etype == "purple":
            self.hp = 2 
            self.color = ENEMY_PURPLE 
            self.base_speed = 100
        else:
            self.hp = 1
            self.color = ENEMY_RED
            self.base_speed = 70
        
        self.image = pygame.Surface((TILE_SIZE*0.8, TILE_SIZE*0.8), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y + TILE_SIZE*0.2))
        
        self.dir = 1
        self.vel_y = 0
        self.time = random.uniform(0, 10)
        self.edge_jump_cooldown = 0

    def take_damage(self, game):
        self.hp -= 1
        for i in range(4):
             p = Particle(self.rect.centerx, self.rect.top, self.color)
             game.particles.add(p)
             
        if self.hp <= 0:
            self.kill()
            game.camera.shake = 0.2
        else:
            self.color = (255, 120, 255) 
            self.base_speed += 40

    def update(self, delta_time, player, platforms):
        self.edge_jump_cooldown -= delta_time
        self.vel_y += GRAVITY * delta_time
        self.rect.y += self.vel_y * delta_time
        
        hits = pygame.sprite.spritecollide(self, platforms, False)
        is_grounded = False
        
        if hits:
            if self.vel_y > 0:
                self.rect.bottom = hits[0].rect.top
                self.vel_y = 0
                is_grounded = True
            elif self.vel_y < 0:
                self.rect.top = hits[0].rect.bottom
                self.vel_y = 0
                
        if self.dir == 1:
            probe_x = self.rect.right + 6
        else:
            probe_x = self.rect.left - 6
            
        probe_rect = pygame.Rect(probe_x, self.rect.bottom + 4, 2, 2)
        wall_rect = pygame.Rect(probe_x, self.rect.centery, 2, 2)
        
        floor_hit = False
        for p in platforms:
            if p.rect.colliderect(probe_rect):
                floor_hit = True
                break
                
        wall_hit = False
        for p in platforms:
            if p.rect.colliderect(wall_rect):
                wall_hit = True
                break
        
        if wall_hit:
            self.dir *= -1
        elif is_grounded and not floor_hit and self.edge_jump_cooldown <= 0:
            if self.etype == "purple":
                self.vel_y = JUMP_STRENGTH * 0.75
                self.edge_jump_cooldown = 0.6
                self.dir *= -1
            else:
                self.dir *= -1

        if self.etype == "purple" and not is_grounded:
            current_speed = 0 
        else:
            current_speed = self.base_speed
            
        self.rect.x += current_speed * self.dir * delta_time
        
        self.draw_enemy()

    def draw_enemy(self):
        self.time += 0.2
        self.image.fill((0,0,0,0))
        
        squish_x = 1.0 + math.sin(self.time) * 0.08
        squish_y = 1.0 - math.sin(self.time) * 0.08
        
        w = int(self.rect.width * squish_x)
        h = int(self.rect.height * squish_y)
        body_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        
        if self.etype == "red":
            pygame.draw.rect(body_surf, self.color, (0, 0, w, h), border_radius=6)
        else:
            bob = abs(math.sin(self.time)) * 4
            pygame.draw.rect(body_surf, self.color, (0, int(bob), w, h - int(bob)), border_radius=6)
            
        if self.dir == 1:
            eye_x = w - 12
            pupil_offset = 3
        else:
            eye_x = 4
            pupil_offset = 1
            
        pygame.draw.rect(body_surf, (255, 255, 255), (eye_x, 6, 7, 7))
        pygame.draw.rect(body_surf, (0, 0, 0), (eye_x + pupil_offset, 8, 3, 3))
        
        self.image.blit(body_surf, ((self.rect.width - w)//2, self.rect.height - h))

class Spring(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.trigger_time = 0
        
    def trigger(self):
        self.trigger_time = 0.25
        
    def update(self, delta_time):
        self.trigger_time -= delta_time
        self.image.fill((0, 0, 0, 0))
        
        if self.trigger_time > 0:
            h = TILE_SIZE // 2 
        else:
            h = TILE_SIZE // 4
            
        y_off = TILE_SIZE - h
        
        pygame.draw.rect(self.image, (80, 90, 100), (2, y_off, TILE_SIZE-4, h), border_radius=3)
        pygame.draw.rect(self.image, SPRING_COLOR, (4, y_off, TILE_SIZE-8, 6), border_radius=2)
        pygame.draw.line(self.image, (255, 255, 255), (6, y_off+2), (TILE_SIZE-10, y_off+2), 2)

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.base_y = y
        self.time = random.uniform(0, 10)

    def update(self, delta_time):
        self.time += delta_time * 6
        pulse = abs(math.sin(self.time * 2.5)) * 5
        self.image.fill((0, 0, 0, 0))
        
        cx = TILE_SIZE // 2
        cy = TILE_SIZE // 2
        
        pygame.draw.circle(self.image, (255, 215, 0, 100), (cx, cy), int(12 + pulse))
        pygame.draw.rect(self.image, COIN_COLOR, (cx-9, cy-9, 18, 18), border_radius=9)
        pygame.draw.rect(self.image, (255, 255, 200), (cx-5, cy-5, 10, 10), border_radius=5)
        
        self.rect.y = self.base_y + math.sin(self.time) * 6

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        self.color = color
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = pygame.math.Vector2(random.uniform(-300, 300), random.uniform(-450, -50))
        self.life = 255
        self.rot = random.randint(0, 360)

    def update(self, delta_time):
        self.vel.y += GRAVITY * 0.8 * delta_time 
        self.rect.x += self.vel.x * delta_time
        self.rect.y += self.vel.y * delta_time
        
        self.life -= 400 * delta_time
        self.rot += 12
        
        if self.life <= 0:
            self.kill()
        else:
            self.image.fill((0, 0, 0, 0))
            surf = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.rect(surf, (self.color[0], self.color[1], self.color[2], int(self.life)), (0, 0, 10, 10))
            surf = pygame.transform.rotate(surf, self.rot)
            self.image.blit(surf, (0, 0))

class StaticEntity(pygame.sprite.Sprite):
    def __init__(self, x, y, color, tag=""):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.tag = tag
        self.time = 0
        
        if tag == "HAZARD":
            for i in range(3):
                px = i * (TILE_SIZE // 3)
                pygame.draw.polygon(self.image, (150, 150, 150), [(px, TILE_SIZE), (px + TILE_SIZE // 6, TILE_SIZE // 2), (px + TILE_SIZE // 3, TILE_SIZE)])
                pygame.draw.polygon(self.image, HAZARD_COLOR, [(px+2, TILE_SIZE), (px + TILE_SIZE // 6, TILE_SIZE // 2 + 4), (px + TILE_SIZE // 3 - 2, TILE_SIZE)])
                pygame.draw.line(self.image, (255, 255, 255), (px + TILE_SIZE // 6, TILE_SIZE // 2 + 4), (px + TILE_SIZE // 3 - 2, TILE_SIZE), 2)
        elif tag == "GOAL":
            self.color = color

    def update(self, delta_time):
        if self.tag == "GOAL":
            self.time += delta_time * 3.5
            self.image.fill((0, 0, 0, 0))
            
            cx = TILE_SIZE // 2
            cy = TILE_SIZE // 2
            pulse = abs(math.sin(self.time)) * 5
            
            pygame.draw.circle(self.image, self.color, (cx, cy), int(16 + pulse))
            pygame.draw.circle(self.image, (255, 255, 255), (cx, cy), int(10 + pulse))
            pygame.draw.circle(self.image, self.color, (cx, cy), 6)