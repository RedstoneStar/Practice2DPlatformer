# main.py
import pygame
import sys
import random
import math
import asyncio
from settings import *
from sprites import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
        
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target, dt):
        target_x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        target_y = -target.rect.centery + int(SCREEN_HEIGHT / 2)
        
        self.camera.x = target_x
        self.camera.y = target_y

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple 2D Platformer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Trebuchet MS", 24, bold=True)
        self.title_font = pygame.font.SysFont("Trebuchet MS", 56, bold=True)
        self.small_font = pygame.font.SysFont("Trebuchet MS", 12, bold=True)
        
        self.state = "MENU"
        self.score = 0
        self.current_level = 0
        self.level_time = 0.0
        self.dark_overlay = self.create_dark_overlay()
        self.kill_y = 0 
        
        # spawn stars
        self.stars = []
        for _ in range(150):
            star_x = random.randint(0, SCREEN_WIDTH * 3)
            star_y = random.randint(0, SCREEN_HEIGHT * 3)
            star_size = random.random()
            self.stars.append((star_x, star_y, star_size))
            
        self.fade_alpha = 255
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    def create_dark_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for radius in range(SCREEN_WIDTH, SCREEN_WIDTH // 2, -15):
            alpha_val = int(140 * (1 - radius / SCREEN_WIDTH))
            if alpha_val > 140:
                alpha_val = 140
            pygame.draw.circle(overlay, (0, 0, 10, alpha_val), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), radius)
        return overlay

    def load_level(self):
        # init groups
        self.platforms = pygame.sprite.Group()
        self.limits = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.springs = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.interactables = pygame.sprite.Group()
        self.ui_elements = pygame.sprite.Group()
        self.orbs = pygame.sprite.Group()
        
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.level_time = 0.0
        self.fade_alpha = 255

        map_data = LEVELS[self.current_level]
        self.kill_y = len(map_data) * TILE_SIZE + 400 # fall death threshold
        
        # parse map
        for row, tiles in enumerate(map_data):
            for col, tile in enumerate(tiles):
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                
                if tile == "P":
                    self.player = Player(x, y)
                elif tile == "X":
                    p = Platform(x, y)
                    self.platforms.add(p)
                elif tile == "B":
                    p = Platform(x, y, breakable=True)
                    self.platforms.add(p)
                elif tile == "M":
                    p = Platform(x, y, moving=True)
                    self.platforms.add(p)
                elif tile == "L":
                    l = LimitBlock(x, y)
                    self.limits.add(l)
                elif tile == "C":
                    c = Coin(x, y)
                    self.coins.add(c)
                elif tile == "O":
                    o = JumpOrb(x, y)
                    self.orbs.add(o)
                elif tile == "E":
                    e = Enemy(x, y, "red")
                    self.enemies.add(e)
                elif tile == "U":
                    e = Enemy(x, y, "purple")
                    self.enemies.add(e)
                elif tile == "F":
                    e = Enemy(x, y, "flyer")
                    self.enemies.add(e)
                elif tile == "S":
                    s = Spring(x, y)
                    self.springs.add(s)
                elif tile == "^":
                    h = StaticEntity(x, y, HAZARD_COLOR, "HAZARD")
                    self.hazards.add(h)
                elif tile == "G":
                    g = StaticEntity(x, y, GOAL_COLOR, "GOAL")
                    self.interactables.add(g)
                elif tile in TUTORIAL_MESSAGES:
                    t = PopupText(x, y, TUTORIAL_MESSAGES[tile], TEXT_COLOR, is_tutorial=True)
                    self.ui_elements.add(t)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    if self.state == "PLAYING":
                        self.state = "PAUSED"
                    elif self.state == "PAUSED":
                        self.state = "PLAYING"
                        
                if (self.state == "MENU" or self.state == "WIN") and event.key == pygame.K_SPACE:
                    if self.state == "WIN":
                        self.current_level = 0
                        self.score = 0
                    self.load_level()
                    self.state = "PLAYING"
                    
                elif self.state in ["PLAYING", "PAUSED"] and event.key == pygame.K_r:
                    self.load_level()
                    self.state = "PLAYING"
                    
                elif self.state == "PLAYING":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.player.jump()
                        
            if event.type == pygame.KEYUP and self.state == "PLAYING":
                if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.player.jump_cut()

    def update(self, dt):
        if self.state == "PAUSED":
            return
            
        if self.state != "PLAYING":
            return
        
        self.level_time += dt
        
        if self.fade_alpha > 0:
            self.fade_alpha -= 400 * dt
            if self.fade_alpha < 0:
                self.fade_alpha = 0
                
        # update everything
        self.platforms.update(dt, self.platforms, self.limits)
        self.player.update(dt, self.platforms, self.hazards, self.enemies, self.springs, self)
        
        for e in self.enemies: 
            e.update(dt, self.player, self.platforms)
            
        self.coins.update(dt)
        self.orbs.update(dt)
        self.springs.update(dt)
        self.particles.update(dt)
        self.interactables.update(dt)
        self.ui_elements.update(dt)
        
        self.camera.update(self.player, dt)
        
        # handle collectables
        hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        for hit in hits:
            self.score += 50
            score_popup = PopupText(hit.rect.centerx, hit.rect.centery, "+50", COIN_COLOR)
            self.ui_elements.add(score_popup)
            for _ in range(5):
                p = Particle(hit.rect.centerx, hit.rect.centery, COIN_COLOR)
                self.particles.add(p)
                
        orb_hits = pygame.sprite.spritecollide(self.player, self.orbs, False)
        for o in orb_hits:
            if o.active:
                o.collect()
                self.player.jumps_left = 2
                for _ in range(4):
                    self.particles.add(Particle(o.rect.centerx, o.rect.centery, ORB_COLOR))
                
        interacts = pygame.sprite.spritecollide(self.player, self.interactables, False)
        for i in interacts:
            if i.tag == "GOAL":
                self.current_level += 1
                if self.current_level >= len(LEVELS):
                    self.state = "WIN"
                else:
                    self.load_level()

    def draw_bg(self):
        for y in range(SCREEN_HEIGHT):
            percent = y / SCREEN_HEIGHT
            r = int(BG_TOP[0] * (1 - percent) + BG_BOTTOM[0] * percent)
            g = int(BG_TOP[1] * (1 - percent) + BG_BOTTOM[1] * percent)
            b = int(BG_TOP[2] * (1 - percent) + BG_BOTTOM[2] * percent)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        cam_x = self.camera.camera.x
        cam_y = self.camera.camera.y
        
        for star in self.stars:
            sx = star[0]
            sy = star[1]
            size = star[2]
            
            px = (sx + cam_x * size * 0.5) % SCREEN_WIDTH
            py = (sy + cam_y * size * 0.5) % SCREEN_HEIGHT
            c = int(80 + 175 * size)
            pygame.draw.circle(self.screen, (c, c, c), (px, py), 1 + size * 1.5)

    def draw_hud(self):
        pulse_effect = math.sin(pygame.time.get_ticks() / 300.0) * 2
        title_txt = self.font.render("Simple 2D Platformer", True, (150, 150, 180))
        score_txt = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        level_txt = self.font.render(f"Level: {self.current_level + 1} / {len(LEVELS)}", True, TEXT_COLOR)
        time_txt = self.font.render(f"Time: {round(self.level_time, 1)}s", True, COIN_COLOR)
        
        self.screen.blit(title_txt, (SCREEN_WIDTH // 2 - title_txt.get_width() // 2, 10 + int(pulse_effect * 0.5)))
        self.screen.blit(score_txt, (20, 20))
        self.screen.blit(level_txt, (SCREEN_WIDTH // 2 - level_txt.get_width() // 2, 40))
        self.screen.blit(time_txt, (SCREEN_WIDTH - time_txt.get_width() - 20, 20))
        
        # dash cooldown bar
        pygame.draw.rect(self.screen, (30, 30, 40), (20, 60, 150, 15), border_radius=4)
        if self.player.dash_cd <= 0:
            pygame.draw.rect(self.screen, PLAYER_DASH_COLOR, (20, 60, 150, 15), border_radius=4)
            ready_txt = self.small_font.render("DASH READY", True, (0, 0, 0))
            self.screen.blit(ready_txt, (20 + 75 - ready_txt.get_width() // 2, 61))
        else:
            ratio = max(0, 1 - (self.player.dash_cd / 1.0))
            pygame.draw.rect(self.screen, (200, 150, 50), (20, 60, 150 * ratio, 15), border_radius=4)

    def draw(self):
        if self.state == "MENU" or self.state == "WIN":
            self.draw_bg()
            title_str = "Simple 2D Platformer"
            if self.state == "MENU":
                sub_str = "Press SPACE to Start"
            else:
                sub_str = "CAMPAIGN COMPLETE! Press SPACE to replay."
            
            title = self.title_font.render(title_str, True, GOAL_COLOR)
            txt = self.font.render(sub_str, True, TEXT_COLOR)
            
            for i in range(1, 4):
                glow = self.title_font.render(title_str, True, (100, 50, 150))
                self.screen.blit(glow, (SCREEN_WIDTH // 2 - title.get_width() // 2 + i * 2, SCREEN_HEIGHT // 3 + i * 2))
                
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 3))
            
            pulse = math.sin(pygame.time.get_ticks() / 200.0) * 10
            self.screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, SCREEN_HEIGHT // 2 + 50 + int(pulse)))
        else:
            self.draw_bg()
            
            # culling rect
            view_rect = pygame.Rect(-self.camera.camera.x - 80, -self.camera.camera.y - 80, SCREEN_WIDTH + 160, SCREEN_HEIGHT + 160)
            
            for g in self.interactables:
                if view_rect.colliderect(g.rect): self.screen.blit(g.image, self.camera.apply(g))
            for p in self.platforms:
                if view_rect.colliderect(p.rect): self.screen.blit(p.image, self.camera.apply(p))
            for s in self.springs:
                if view_rect.colliderect(s.rect): self.screen.blit(s.image, self.camera.apply(s))
            for h in self.hazards:
                if view_rect.colliderect(h.rect): self.screen.blit(h.image, self.camera.apply(h))
            for c in self.coins:
                if view_rect.colliderect(c.rect): self.screen.blit(c.image, self.camera.apply(c))
            for o in self.orbs:
                if view_rect.colliderect(o.rect): self.screen.blit(o.image, self.camera.apply(o))
                
            for e in self.enemies:
                if view_rect.colliderect(e.rect):
                    cam_rect = self.camera.apply(e)
                    draw_shadow(self.screen, cam_rect, radius=6)
                    ox = (e.image.get_width() - e.rect.width) // 2
                    oy = (e.image.get_height() - e.rect.height) // 2
                    self.screen.blit(e.image, (cam_rect.x - ox, cam_rect.y - oy))
                    
            for p in self.particles:
                if view_rect.colliderect(p.rect): self.screen.blit(p.image, self.camera.apply(p))
                
            cam_p = self.camera.apply(self.player)
            draw_shadow(self.screen, cam_p, radius=4)
            ox = (self.player.image.get_width() - self.player.rect.width) // 2
            oy = (self.player.image.get_height() - self.player.rect.height) // 2
            self.screen.blit(self.player.image, (cam_p.x - ox, cam_p.y - oy))
            
            for u in self.ui_elements:
                if view_rect.colliderect(u.rect): self.screen.blit(u.image, self.camera.apply(u))
                
            self.screen.blit(self.dark_overlay, (0, 0))
            self.draw_hud()
            
            if self.fade_alpha > 0:
                fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fade_surf.fill((0, 0, 0))
                fade_surf.set_alpha(int(self.fade_alpha))
                self.screen.blit(fade_surf, (0, 0))
                
            # UI overlay
            if self.state == "PAUSED":
                pause_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                pause_overlay.fill((0, 0, 0, 150))
                self.screen.blit(pause_overlay, (0, 0))
                pause_title = self.title_font.render("PAUSED", True, TEXT_COLOR)
                self.screen.blit(pause_title, (SCREEN_WIDTH // 2 - pause_title.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
                pause_sub = self.font.render("Press ESC to Resume or R to Reset", True, TEXT_COLOR)
                self.screen.blit(pause_sub, (SCREEN_WIDTH // 2 - pause_sub.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
                
        pygame.display.flip()

    async def run(self):
        # main game loop
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            if dt > 0.05:
                dt = 0.05 # cap dt lag
                
            # print(f"FPS: {self.clock.get_fps()}")
            
            self.events()
            self.update(dt)
            self.draw()
            await asyncio.sleep(0)

if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())