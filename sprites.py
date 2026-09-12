# sprites.py
import pygame
import math
import random
from settings import *

def draw_shadow(surface, rect, radius=0):
    # simple drop shadow
    shadow = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0, 0, 0, 80), shadow.get_rect(), border_radius=radius)
    surface.blit(shadow, (rect.x + 4, rect.y + 4))

class LimitBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # invisible barrier
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

class Trail(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.alpha = 180

    def update(self, dt):
        self.alpha -= 800 * dt
        if self.alpha <= 0:
            self.kill()
        else:
            self.image.set_alpha(int(self.alpha))

class PopupText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color, is_tutorial=False):
        super().__init__()
        
        size = 20 if is_tutorial else 22
            
        font = pygame.font.SysFont("Trebuchet MS", size, bold=True)
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.is_tutorial = is_tutorial
        
        self.vel_y = 0 if is_tutorial else -100
        self.life = 255
        self.base_image = self.image.copy()

    def update(self, dt):
        if not self.is_tutorial:
            self.rect.y += self.vel_y * dt
            self.life -= 300 * dt
            if self.life <= 0:
                self.kill()
            else:
                self.image = self.base_image.copy()
                self.image.set_alpha(int(self.life))
        else:
            self.rect.y += math.sin(pygame.time.get_ticks() / 200.0) * 0.5 # bob up and down

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = int(TILE_SIZE * 0.7)
        self.height = TILE_SIZE
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
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
        self.dash_timer = 0 
        self.dash_dir = 1
        
        self.facing_right = True
        self.scale_x = 1.0
        self.scale_y = 1.0
        
        # self.debug = False

    def update(self, dt, platforms, hazards, enemies, springs, game):
        self.acc = pygame.math.Vector2(0, GRAVITY)
        
        self.coyote_timer -= dt
        self.jump_buffer -= dt
        self.dash_cd -= dt
        
        # handle dash state
        if self.dash_timer > 0:
            self.dash_timer -= dt
            self.acc.y = GRAVITY * 0.12 # slight float
            self.vel.x = DASH_SPEED * self.dash_dir * (self.dash_timer / 0.25)
            if self.dash_timer <= 0:
                self.vel.x = (DASH_SPEED * 0.4) * self.dash_dir

        self.scale_x += (1.0 - self.scale_x) * 12 * dt
        self.scale_y += (1.0 - self.scale_y) * 12 * dt
        
        self.handle_input(dt, game)
        
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc * dt
        
        if self.on_wall != 0 and self.vel.y > 0:
            self.vel.y = min(self.vel.y, WALL_SLIDE_SPEED)
            if random.random() < 0.05:
                p = Particle(self.rect.centerx, self.rect.bottom, (200, 200, 200))
                game.particles.add(p)
        else:
            self.vel.y = min(self.vel.y, TERMINAL_VELOCITY)
            
        old_x = self.pos.x
        if self.is_grounded and self.standing_on != None:
            self.pos.x += self.standing_on.dx
            
        self.pos.x += self.vel.x * dt + 0.5 * self.acc.x * (dt ** 2)
        self.rect.x = int(self.pos.x)
        self.check_collision(platforms, 'horizontal', game, dt, self.pos.x - old_x)

        old_y = self.pos.y
        self.pos.y += self.vel.y * dt + 0.5 * self.acc.y * (dt ** 2)
        self.rect.y = int(self.pos.y)
        self.check_collision(platforms, 'vertical', game, dt, self.pos.y - old_y)
        
        if self.is_grounded:
            self.coyote_timer = 0.15 

        if self.jump_buffer > 0 and (self.coyote_timer > 0 or self.jumps_left > 0 or self.on_wall != 0):
            self.execute_jump(game)
            
        self.check_combat(enemies, game)
        self.check_springs(springs, game)
        
        self.draw_player()
        
        if self.dash_timer > 0 or abs(self.vel.x) > 800:
            trail = Trail(self.rect.x, self.rect.y, self.rect.width, self.rect.height, PLAYER_DASH_COLOR)
            game.particles.add(trail)

        if self.rect.top > game.kill_y or pygame.sprite.spritecollideany(self, hazards):
            self.die(game)

    def draw_player(self):
        sw = self.width + 60
        sh = self.height + 60
        self.image = pygame.Surface((sw, sh), pygame.SRCALPHA)
        
        if self.jumps_left > 0:
            color = PLAYER_COLOR
        else:
            color = (30, 140, 100) # out of jumps
            
        if self.dash_timer > 0:
            color = (255, 255, 255)
            
        dw = self.width * self.scale_x
        dh = self.height * self.scale_y
        
        dy = (sh - self.height) / 2 + self.height - dh
        
        if self.is_grounded and abs(self.vel.x) < 5:
            breath = math.sin(pygame.time.get_ticks() / 150.0) * 2.5
            dh -= breath
            dy += breath

        dx = (sw - dw) / 2
        
        back_x = dx - 4 if self.facing_right else dx + dw
            
        pygame.draw.rect(self.image, (max(0, color[0]-40), max(0, color[1]-40), max(0, color[2]-40)), (back_x, dy + 8, 4, dh - 16))
        pygame.draw.rect(self.image, color, (dx, dy, dw, dh), border_radius=4)
        
        eye_x = dx + dw - 14 if self.facing_right else dx + 4
            
        pygame.draw.rect(self.image, (20, 20, 30), (eye_x, dy + 6, 10, 10), border_radius=2)
        
        pupil_offset = 4 if self.facing_right else 2
        pygame.draw.rect(self.image, (0, 255, 255), (eye_x + pupil_offset, dy + 8, 4, 4))
        
        # if self.debug:
        #     pygame.draw.rect(self.image, (255,0,0), self.rect, 1)

    def handle_input(self, dt, game):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -ACCELERATION
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = ACCELERATION
            self.facing_right = True
            
        if keys[pygame.K_LSHIFT] and self.dash_cd <= 0:
            self.dash_timer = 0.25
            self.dash_cd = 1.0
            self.dash_dir = 1 if self.facing_right else -1
            self.scale_x = 1.7
            self.scale_y = 0.35
            self.vel.y = 0 # dash reset

    def jump(self):
        self.jump_buffer = 0.15 # buffer window
            
    def execute_jump(self, game):
        self.vel.y = JUMP_STRENGTH
        self.is_grounded = False
        self.standing_on = None
        self.coyote_timer = 0
        self.jump_buffer = 0
        
        self.scale_x = 0.55
        self.scale_y = 1.45
        
        if self.jumps_left == 1 and self.on_wall == 0:
            for i in range(8):
                p = Particle(self.rect.centerx, self.rect.centery + 10, (255, 255, 255))
                ang = i * (math.pi / 4)
                p.vel.x = math.cos(ang) * 150
                p.vel.y = math.sin(ang) * 150
                p.life = 180
                game.particles.add(p)
        else:
            for _ in range(2):
                p = Particle(self.rect.centerx, self.rect.bottom, (200, 200, 200))
                game.particles.add(p)
            
        if self.on_wall != 0: 
            self.vel.x = -self.on_wall * WALL_JUMP_X
            self.on_wall = 0
            self.jumps_left = 1 
        else:
            self.jumps_left -= 1

    def jump_cut(self):
        # variable jump height
        if self.vel.y < JUMP_STRENGTH * 0.3:
            self.vel.y = JUMP_STRENGTH * 0.3

    def die(self, game):
        for _ in range(10):
             p = Particle(self.rect.centerx, self.rect.centery, PLAYER_COLOR)
             game.particles.add(p)
             
        self.pos = pygame.math.Vector2(self.spawn_point.x, self.spawn_point.y)
        self.vel = pygame.math.Vector2(0, 0)
        self.rect.topleft = self.pos
        self.dash_cd = 0
        self.dash_timer = 0

    def shatter_block(self, block, game):
        block.kill()
        for _ in range(3):
            p = Particle(block.rect.centerx, block.rect.centery, block.color)
            game.particles.add(p)

    def check_collision(self, platforms, direction, game, dt, actual_d=0):
        if direction == 'horizontal':
            hits = pygame.sprite.spritecollide(self, platforms, False)
            self.on_wall = 0
            hit_block = None
            is_dashing = self.dash_timer > 0 or abs(self.vel.x) > 800
            
            for block in hits:
                if block.breakable and is_dashing:
                    self.shatter_block(block, game)
                elif hit_block is None and block.alive():
                    hit_block = block
                    
            if hit_block:
                # print(hit_block)
                if actual_d > 0:
                    self.pos.x = hit_block.rect.left - self.rect.width
                    self.on_wall = 1
                elif actual_d < 0:
                    self.pos.x = hit_block.rect.right
                    self.on_wall = -1
                else:
                    if self.rect.centerx < hit_block.rect.centerx:
                        self.pos.x = hit_block.rect.left - self.rect.width
                        self.on_wall = 1
                    else:
                        self.pos.x = hit_block.rect.right
                        self.on_wall = -1
                        
                self.vel.x = 0
                self.rect.x = int(self.pos.x)
                
        elif direction == 'vertical':
            hit_block = None
            self.standing_on = None 
            
            if self.vel.y >= 0:
                self.rect.y += 2 # ground probe
                
            hits = pygame.sprite.spritecollide(self, platforms, False)
            
            if self.vel.y >= 0:
                self.rect.y -= 2
            
            for block in hits:
                if block.breakable and self.vel.y < 0:
                    self.shatter_block(block, game)
                    if self.vel.y < 0: self.vel.y = 0 
                elif hit_block is None and block.alive():
                    hit_block = block
                    
            if hit_block:
                if actual_d > 0 or self.vel.y > 0:
                    self.pos.y = hit_block.rect.top - self.rect.height
                    
                    if not self.is_grounded:
                        self.scale_x = 1.45
                        self.scale_y = 0.55
                            
                    self.is_grounded = True
                    self.jumps_left = 2
                    self.standing_on = hit_block
                        
                elif actual_d < 0 or self.vel.y < 0:
                    self.pos.y = hit_block.rect.bottom
                    
                self.vel.y = 0
                self.rect.y = int(self.pos.y)
                
            else:
                if self.vel.y > 0 and self.coyote_timer <= 0:
                    self.is_grounded = False

    def check_combat(self, enemies, game):
        hits = pygame.sprite.spritecollide(self, enemies, False)
        for enemy in hits:
            # hop on head
            if self.vel.y > 0 and self.rect.bottom < enemy.rect.centery + 15:
                self.vel.y = JUMP_STRENGTH * 0.85
                self.jumps_left = 1
                enemy.take_damage(game)
            else:
                self.die(game)
                
    def check_springs(self, springs, game):
        hits = pygame.sprite.spritecollide(self, springs, False)
        for spring in hits:
            self.vel.y = SPRING_STRENGTH
            self.jumps_left = 2
            self.scale_x = 0.35
            self.scale_y = 1.85
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
        
        self.vel_x = 140 if moving else 0
        self.dx = 0

    def update(self, dt, platforms=None, limits=None):
        self.dx = 0
        
        if self.moving:
            old_x = self.pos.x
            self.pos.x += self.vel_x * dt
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
                self.pos.x = old_x
                self.vel_x *= -1
                self.pos.x += self.vel_x * dt 
                self.rect.x = int(self.pos.x)
                
            self.dx = self.pos.x - old_x

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, etype="red"):
        super().__init__()
        self.etype = etype
        self.spawn_y = y + TILE_SIZE * 0.2
        
        if etype == "purple":
            self.hp = 2 
            self.color = ENEMY_PURPLE 
            self.base_speed = 100
        elif etype == "flyer":
            self.hp = 1
            self.color = ENEMY_FLYER
            self.base_speed = 90
            self.spawn_y = y 
        else:
            self.hp = 1
            self.color = ENEMY_RED
            self.base_speed = 70
        
        self.base_color = self.color
        self.width = int(TILE_SIZE * 0.8)
        self.height = int(TILE_SIZE * 0.8)
        self.image = pygame.Surface((self.width + 80, self.height + 80), pygame.SRCALPHA)
        self.rect = pygame.Rect(x, self.spawn_y, self.width, self.height)
        
        self.dir = 1
        self.vel_y = 0
        self.time = random.uniform(0, 10)
        self.edge_jump_cooldown = 0

    def take_damage(self, game):
        self.hp -= 1
        for _ in range(4):
             p = Particle(self.rect.centerx, self.rect.top, self.color)
             game.particles.add(p)
             
        if self.hp <= 0:
            self.kill()
        else:
            self.base_color = (255, 120, 255) 
            self.color = self.base_color
            self.base_speed += 40 # enrage

    def update(self, dt, player, platforms):
        self.time += dt * 12 # smooth animation timer
        self.edge_jump_cooldown -= dt
        
        if self.etype != "flyer":
            self.vel_y += GRAVITY * dt
            self.rect.y += self.vel_y * dt
            
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
                    
            probe_x = self.rect.right + 6 if self.dir == 1 else self.rect.left - 6
                
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
                    self.edge_jump_cooldown = 0.6 # prevent jump spam
                    self.dir *= -1
                else:
                    self.dir *= -1 # turn at ledge

            current_speed = 0 if self.etype == "purple" and not is_grounded else self.base_speed
                
            self.rect.x += current_speed * self.dir * dt
            
        else:
            if not hasattr(self, "ai_mode"):
                self.ai_mode = "patrol"
                self.charge_time = 0
                self.swoop_vel = pygame.math.Vector2(0, 0)
                self.vel_y = 0
                self.float_t = 0
                
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            on_screen = (abs(dx) < SCREEN_WIDTH/2 + 50 and abs(dy) < SCREEN_HEIGHT/2 + 50)
            
            if self.ai_mode == "patrol":
                self.float_t += dt * 1.5
                target = self.spawn_y + math.sin(self.float_t) * 15
                
                mov_y = target - self.rect.y
                self.rect.y += mov_y * 4 * dt
                for p in platforms:
                    if self.rect.colliderect(p.rect):
                        if mov_y > 0: self.rect.bottom = p.rect.top
                        else: self.rect.top = p.rect.bottom
                        break
                        
                self.rect.x += self.base_speed * self.dir * dt
                hit_w = False
                for p in platforms:
                    if self.rect.colliderect(p.rect):
                        if self.dir == 1: self.rect.right = p.rect.left
                        else: self.rect.left = p.rect.right
                        hit_w = True
                        break
                if hit_w: self.dir *= -1
                
                # tiny chance to attack
                if on_screen and dist >= TILE_SIZE * 3 and random.random() < 0.01:
                    self.ai_mode = "charging"
                    self.charge_time = 1.0
                    
            elif self.ai_mode == "charging":
                self.charge_time -= dt
                
                ratio = max(0.0, 1.0 - self.charge_time) 
                base = getattr(self, 'base_color', ENEMY_FLYER)
                r = int(base[0] + (255 - base[0]) * ratio)
                g = int(base[1] + (50 - base[1]) * ratio)
                b = int(base[2] + (50 - base[2]) * ratio)
                self.color = (r, g, b)
                    
                if self.charge_time <= 0:
                    self.ai_mode = "swooping"
                    self.color = getattr(self, 'base_color', ENEMY_FLYER)
                    ang = math.atan2(dy, dx)
                    self.swoop_vel.x = math.cos(ang) * 450
                    self.swoop_vel.y = math.sin(ang) * 450
                    
            elif self.ai_mode == "swooping":
                self.rect.x += self.swoop_vel.x * dt
                hit = False
                for p in platforms:
                    if self.rect.colliderect(p.rect):
                        hit = True
                        if self.swoop_vel.x > 0: self.rect.right = p.rect.left
                        else: self.rect.left = p.rect.right
                        break
                        
                self.rect.y += self.swoop_vel.y * dt
                for p in platforms:
                    if self.rect.colliderect(p.rect):
                        hit = True
                        if self.swoop_vel.y > 0: self.rect.bottom = p.rect.top
                        else: self.rect.top = p.rect.bottom
                        break
                        
                if hit or not on_screen or dist > 1200:
                    self.ai_mode = "returning"
                    
            elif self.ai_mode == "returning":
                mov_y = self.spawn_y - self.rect.y
                self.rect.y += mov_y * 2 * dt
                for p in platforms:
                    if self.rect.colliderect(p.rect):
                        if mov_y > 0: self.rect.bottom = p.rect.top
                        else: self.rect.top = p.rect.bottom
                        break
                        
                self.rect.x += self.base_speed * self.dir * dt
                hit_w = False
                for p in platforms:
                    if self.rect.colliderect(p.rect):
                        if self.dir == 1: self.rect.right = p.rect.left
                        else: self.rect.left = p.rect.right
                        hit_w = True
                        break
                if hit_w: self.dir *= -1
                
                if abs(mov_y) < 5:
                    self.ai_mode = "patrol"
            
        self.draw_enemy()

    def draw_enemy(self):
        self.image.fill((0,0,0,0))
        
        sx = 1.0 + math.sin(self.time) * 0.08
        sy = 1.0 - math.sin(self.time) * 0.08
        
        w = int(self.rect.width * sx)
        h = int(self.rect.height * sy)
        body_surf = pygame.Surface((w + 20, h + 20), pygame.SRCALPHA)
        
        bx, by = 10, 10
        
        if self.etype == "red":
            pygame.draw.rect(body_surf, self.color, (bx, by, w, h), border_radius=6)
        elif self.etype == "flyer":
            pygame.draw.rect(body_surf, self.color, (bx, by, w, h), border_radius=10)
            spd = 3.0 if getattr(self, "ai_mode", "") in ["charging", "swooping"] else 1.0
            wing_offset = abs(math.sin(self.time * spd)) * 12
            pygame.draw.rect(body_surf, (220, 220, 220), (bx + w//2 - 6, by - wing_offset, 12, 6), border_radius=3)
        else:
            bob = abs(math.sin(self.time)) * 4
            pygame.draw.rect(body_surf, self.color, (bx, by + int(bob), w, h - int(bob)), border_radius=6)
            
        if self.dir == 1:
            eye_x = bx + w - 12
            pupil_offset = 3
        else:
            eye_x = bx + 4
            pupil_offset = 1
            
        pygame.draw.rect(body_surf, (255, 255, 255), (eye_x, by + 6, 7, 7))
        pygame.draw.rect(body_surf, (0, 0, 0), (eye_x + pupil_offset, by + 8, 3, 3))
        
        shake_x = random.randint(-2, 2) if getattr(self, "ai_mode", "") == "charging" else 0
        shake_y = random.randint(-2, 2) if getattr(self, "ai_mode", "") == "charging" else 0
        
        blit_x = (self.image.get_width() - (w + 20)) // 2 + shake_x
        blit_y = (self.image.get_height() - (h + 20)) // 2 + shake_y
        
        if self.etype == "flyer" and hasattr(self, "ai_mode") and self.ai_mode == "swooping":
            ang = -math.degrees(math.atan2(self.swoop_vel.y, self.swoop_vel.x))
            rot = pygame.transform.rotate(body_surf, ang)
            if self.swoop_vel.x < 0:
                rot = pygame.transform.flip(rot, False, True)
            r_rect = rot.get_rect(center=(self.image.get_width()//2 + shake_x, self.image.get_height()//2 + shake_y))
            self.image.blit(rot, r_rect.topleft)
        else:
            self.image.blit(body_surf, (blit_x, blit_y))

class Spring(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.trigger_time = 0
        
    def trigger(self):
        self.trigger_time = 0.25
        
    def update(self, dt):
        self.trigger_time -= dt
        self.image.fill((0, 0, 0, 0))
        
        h = TILE_SIZE // 2 if self.trigger_time > 0 else TILE_SIZE // 4
        y_off = TILE_SIZE - h
        
        pygame.draw.rect(self.image, (80, 90, 100), (2, y_off, TILE_SIZE-4, h), border_radius=3)
        pygame.draw.rect(self.image, SPRING_COLOR, (4, y_off, TILE_SIZE-8, 6), border_radius=2)
        pygame.draw.line(self.image, (255, 255, 255), (6, y_off+2), (TILE_SIZE-10, y_off+2), 2)

class JumpOrb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.base_y = y
        self.time = random.uniform(0, 10)
        self.active = True
        self.inactive_timer = 0
        
    def collect(self):
        self.active = False
        self.inactive_timer = 3.0
        
    def update(self, dt):
        if not self.active:
            self.inactive_timer -= dt
            if self.inactive_timer <= 0:
                self.active = True
                
        self.time += dt * 4
        self.image.fill((0, 0, 0, 0))
        
        if self.active:
            cx = TILE_SIZE // 2
            cy = TILE_SIZE // 2
            pulse = abs(math.sin(self.time)) * 4
            
            pygame.draw.circle(self.image, (100, 255, 255, 100), (cx, cy), int(12 + pulse))
            pygame.draw.circle(self.image, ORB_COLOR, (cx, cy), 8)
            pygame.draw.circle(self.image, (255, 255, 255), (cx-2, cy-2), 3)
            
        self.rect.y = self.base_y + math.sin(self.time) * 4

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.base_y = y
        self.time = random.uniform(0, 10)

    def update(self, dt):
        self.time += dt * 6
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

    def update(self, dt):
        self.vel.y += GRAVITY * 0.8 * dt 
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt
        
        self.life -= 400 * dt
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

    def update(self, dt):
        if self.tag == "GOAL":
            self.time += dt * 3.5
            self.image.fill((0, 0, 0, 0))
            
            cx = TILE_SIZE // 2
            cy = TILE_SIZE // 2
            pulse = abs(math.sin(self.time)) * 5
            
            pygame.draw.circle(self.image, self.color, (cx, cy), int(16 + pulse))
            pygame.draw.circle(self.image, (255, 255, 255), (cx, cy), int(10 + pulse))
            pygame.draw.circle(self.image, self.color, (cx, cy), 6)