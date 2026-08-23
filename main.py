import pygame
import sys
import random
from settings import *
from sprites import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.shake = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
        
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target, dt):
        target_x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        target_y = -target.rect.centery + int(SCREEN_HEIGHT / 2)
        self.camera.x += (target_x - self.camera.x) * 6 * dt
        self.camera.y += (target_y - self.camera.y) * 6 * dt
        
        if self.shake > 0:
            self.camera.x += random.randint(-15, 15) * self.shake
            self.camera.y += random.randint(-15, 15) * self.shake
            self.shake -= dt

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple 2D Platformer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Trebuchet MS", 24, bold=True)
        self.title_font = pygame.font.SysFont("Trebuchet MS", 56, bold=True)
        self.state = "MENU"
        self.score = 0
        self.current_level = 0
        self.level_time = 0.0
        self.vignette = self.create_vignette()
        self.stars = [(random.randint(0, SCREEN_WIDTH*3), random.randint(0, SCREEN_HEIGHT*3), random.random()) for _ in range(150)]
        self.fade_alpha = 255
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    def create_vignette(self):
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for radius in range(SCREEN_WIDTH, SCREEN_WIDTH // 2, -15):
            alpha = min(140, int(140 * (1 - radius / SCREEN_WIDTH)))
            pygame.draw.circle(surf, (0, 0, 10, alpha), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), radius)
        return surf

    def load_level(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.limits = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.springs = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.interactables = pygame.sprite.Group()
        self.ui_elements = pygame.sprite.Group()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.level_time = 0.0
        self.fade_alpha = 255

        map_data = LEVELS[self.current_level]
        for row, tiles in enumerate(map_data):
            for col, tile in enumerate(tiles):
                x, y = col * TILE_SIZE, row * TILE_SIZE
                if tile == "P":
                    self.player = Player(x, y)
                    self.all_sprites.add(self.player)
                elif tile == "X":
                    p = Platform(x, y)
                    self.all_sprites.add(p); self.platforms.add(p)
                elif tile == "B":
                    p = Platform(x, y, breakable=True)
                    self.all_sprites.add(p); self.platforms.add(p)
                elif tile == "M":
                    p = Platform(x, y, moving=True)
                    self.all_sprites.add(p); self.platforms.add(p)
                elif tile == "L":
                    l = LimitBlock(x, y)
                    self.limits.add(l)
                elif tile == "C":
                    c = Coin(x, y)
                    self.all_sprites.add(c); self.coins.add(c)
                elif tile == "E":
                    e = Enemy(x, y, "red")
                    self.all_sprites.add(e); self.enemies.add(e)
                elif tile == "U":
                    e = Enemy(x, y, "purple")
                    self.all_sprites.add(e); self.enemies.add(e)
                elif tile == "S":
                    s = Spring(x, y)
                    self.all_sprites.add(s); self.springs.add(s)
                elif tile == "^":
                    h = StaticEntity(x, y, HAZARD_COLOR, "HAZARD")
                    self.all_sprites.add(h); self.hazards.add(h)
                elif tile == "G":
                    g = StaticEntity(x, y, GOAL_COLOR, "GOAL")
                    self.all_sprites.add(g); self.interactables.add(g)
                elif tile in TUTORIAL_MESSAGES:
                    t = FloatingText(x, y, TUTORIAL_MESSAGES[tile], TEXT_COLOR, is_tutorial=True)
                    self.all_sprites.add(t); self.ui_elements.add(t)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if self.state in ["MENU", "WIN"] and event.key == pygame.K_SPACE:
                    if self.state == "WIN":
                        self.current_level = 0
                        self.score = 0
                    self.load_level()
                    self.state = "PLAYING"
                elif self.state == "PLAYING":
                    if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                        self.player.jump()
                    elif event.key == pygame.K_r:
                        self.load_level()
                        
            if event.type == pygame.KEYUP and self.state == "PLAYING":
                if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                    self.player.jump_cut()

    def update(self, dt):
        if self.state != "PLAYING": return
        
        self.level_time += dt
        if self.fade_alpha > 0:
            self.fade_alpha = max(0, self.fade_alpha - 400 * dt)
            
        self.player.update(dt, self.platforms, self.hazards, self.enemies, self.springs, self)
        for e in self.enemies: e.update(dt, self.player, self.platforms)
        self.coins.update(dt)
        self.springs.update(dt)
        self.particles.update(dt)
        self.interactables.update(dt)
        self.ui_elements.update(dt)
        self.platforms.update(dt, self.platforms, self.limits)
        self.camera.update(self.player, dt)
        
        hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        for hit in hits:
            self.score += 50
            ft = FloatingText(hit.rect.centerx, hit.rect.centery, "+50", COIN_COLOR)
            self.all_sprites.add(ft); self.ui_elements.add(ft)
            for _ in range(15):
                p = Particle(hit.rect.centerx, hit.rect.centery, COIN_COLOR)
                self.all_sprites.add(p); self.particles.add(p)
                
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
            blend = y / SCREEN_HEIGHT
            r = int(BG_TOP[0] * (1 - blend) + BG_BOTTOM[0] * blend)
            g = int(BG_TOP[1] * (1 - blend) + BG_BOTTOM[1] * blend)
            b = int(BG_TOP[2] * (1 - blend) + BG_BOTTOM[2] * blend)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        cam_x, cam_y = self.camera.camera.x, self.camera.camera.y
        for sx, sy, size in self.stars:
            px = (sx + cam_x * size * 0.5) % SCREEN_WIDTH
            py = (sy + cam_y * size * 0.5) % SCREEN_HEIGHT
            c = int(80 + 175 * size)
            pygame.draw.circle(self.screen, (c, c, c), (px, py), 1 + size * 1.5)

    def draw_hud(self):
        # Subtle pulsing animation for HUD elements
        pulse = math.sin(pygame.time.get_ticks() / 300.0) * 2
        title_txt = self.font.render("Simple 2D Platformer", True, (150, 150, 180))
        score_txt = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        level_txt = self.font.render(f"Level: {self.current_level + 1} / {len(LEVELS)}", True, TEXT_COLOR)
        time_txt = self.font.render(f"Time: {self.level_time:.1f}s", True, COIN_COLOR)
        
        self.screen.blit(title_txt, (SCREEN_WIDTH // 2 - title_txt.get_width() // 2, 10 + int(pulse * 0.5)))
        self.screen.blit(score_txt, (20, 20))
        self.screen.blit(level_txt, (SCREEN_WIDTH // 2 - level_txt.get_width() // 2, 40))
        self.screen.blit(time_txt, (SCREEN_WIDTH - time_txt.get_width() - 20, 20))
        
        pygame.draw.rect(self.screen, (30, 30, 40), (20, 60, 150, 15), border_radius=4)
        if self.player.dash_cd <= 0:
            pygame.draw.rect(self.screen, PLAYER_DASH_COLOR, (20, 60, 150, 15), border_radius=4)
            ready_txt = pygame.font.SysFont("Trebuchet MS", 12, bold=True).render("DASH READY", True, (0, 0, 0))
            self.screen.blit(ready_txt, (20 + 75 - ready_txt.get_width()//2, 61))
        else:
            ratio = max(0, 1 - (self.player.dash_cd / 1.0))
            pygame.draw.rect(self.screen, (200, 150, 50), (20, 60, 150 * ratio, 15), border_radius=4)

    def draw(self):
        if self.state == "MENU" or self.state == "WIN":
            self.draw_bg()
            title_str = "Simple 2D Platformer"
            sub_str = "Press SPACE to Start" if self.state == "MENU" else "CAMPAIGN COMPLETE! Press SPACE to replay."
            
            title = self.title_font.render(title_str, True, GOAL_COLOR)
            txt = self.font.render(sub_str, True, TEXT_COLOR)
            
            for i in range(1, 4):
                glow = self.title_font.render(title_str, True, (100, 50, 200))
                glow.set_alpha(100 // i)
                self.screen.blit(glow, (SCREEN_WIDTH//2 - title.get_width()//2 + i*2, SCREEN_HEIGHT//2 - 60 + i*2))
                
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 60))
            self.screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, SCREEN_HEIGHT//2 + 20))
        else:
            self.draw_bg()
            
            for p in self.platforms: draw_shadow(self.screen, self.camera.apply_rect(p.rect), radius=0)
            
            for sprite in self.all_sprites:
                if not isinstance(sprite, FloatingText) and not isinstance(sprite, Platform):
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
                elif isinstance(sprite, Platform):
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
                    
            self.screen.blit(self.vignette, (0,0))
            for ui in self.ui_elements: self.screen.blit(ui.image, self.camera.apply(ui))
            self.draw_hud()
            
            if self.fade_alpha > 0:
                fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fade_surf.fill((15, 20, 30))
                fade_surf.set_alpha(int(self.fade_alpha))
                self.screen.blit(fade_surf, (0, 0))
            
        pygame.display.flip()

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update(dt)
            self.draw()

if __name__ == "__main__":
    g = Game()
    g.run()