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

    def update(self, target, dt):
        target_x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        target_y = -target.rect.centery + int(SCREEN_HEIGHT / 2)
        self.camera.x += (target_x - self.camera.x) * 8 * dt
        self.camera.y += (target_y - self.camera.y) * 8 * dt
        
        if self.shake > 0:
            self.camera.x += random.randint(-12, 12) * self.shake
            self.camera.y += random.randint(-12, 12) * self.shake
            self.shake -= dt

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simple 2D Platformer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.state = "MENU"
        self.score = 0
        self.current_level = 0
        self.vignette = self.create_vignette()

    def create_vignette(self):
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        # Soft outer ring instead of heavy alpha multiplier
        for radius in range(SCREEN_WIDTH, SCREEN_WIDTH // 2, -10):
            alpha = min(80, int(80 * (1 - radius / SCREEN_WIDTH)))
            pygame.draw.circle(surf, (0, 0, 0, alpha), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), radius)
        return surf

    def load_level(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.interactables = pygame.sprite.Group()
        self.ui_elements = pygame.sprite.Group()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

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
                elif tile == "C":
                    c = Coin(x, y)
                    self.all_sprites.add(c); self.coins.add(c)
                elif tile == "E":
                    e = Enemy(x, y)
                    self.all_sprites.add(e); self.enemies.add(e)
                elif tile == "^":
                    h = StaticEntity(x, y, HAZARD_COLOR, "HAZARD")
                    self.all_sprites.add(h); self.hazards.add(h)
                elif tile == "G":
                    g = StaticEntity(x, y, GOAL_COLOR, "GOAL")
                    self.all_sprites.add(g); self.interactables.add(g)

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
                elif self.state == "PLAYING" and event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                    self.player.jump()
                        
            if event.type == pygame.KEYUP and self.state == "PLAYING":
                if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                    self.player.jump_cut()

    def update(self, dt):
        if self.state != "PLAYING": return
        
        self.player.update(dt, self.platforms, self.hazards, self.enemies, self)
        for e in self.enemies: e.update(dt, self.player, self.platforms)
        self.coins.update(dt)
        self.particles.update(dt)
        self.ui_elements.update(dt)
        self.platforms.update(dt)
        self.camera.update(self.player, dt)
        
        hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        for hit in hits:
            self.score += 10
            # Pop-up text
            ft = FloatingText(hit.rect.centerx, hit.rect.centery, "+10", COIN_COLOR)
            self.all_sprites.add(ft); self.ui_elements.add(ft)
            for _ in range(12):
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

        offset = self.camera.camera.x
        pygame.draw.polygon(self.screen, (30, 30, 45), [(offset * 0.2 % SCREEN_WIDTH - 200, SCREEN_HEIGHT), (offset * 0.2 % SCREEN_WIDTH + 200, 200), (offset * 0.2 % SCREEN_WIDTH + 600, SCREEN_HEIGHT)])
        pygame.draw.polygon(self.screen, (20, 20, 30), [(offset * 0.4 % SCREEN_WIDTH - 100, SCREEN_HEIGHT), (offset * 0.4 % SCREEN_WIDTH + 150, 350), (offset * 0.4 % SCREEN_WIDTH + 400, SCREEN_HEIGHT)])

    def draw_hud(self):
        score_text = self.font.render(f"Score: {self.score}  |  Level: {self.current_level + 1}", True, TEXT_COLOR)
        self.screen.blit(score_text, (20, 20))
        
        # Dash Cooldown UI
        pygame.draw.rect(self.screen, (50, 50, 50), (20, 60, 150, 15), border_radius=4)
        if self.player.dash_cd <= 0:
            pygame.draw.rect(self.screen, PLAYER_DASH_COLOR, (20, 60, 150, 15), border_radius=4)
        else:
            ratio = max(0, 1 - (self.player.dash_cd / 1.2))
            pygame.draw.rect(self.screen, (200, 200, 50), (20, 60, 150 * ratio, 15), border_radius=4)

    def draw(self):
        if self.state == "MENU" or self.state == "WIN":
            self.screen.fill((20, 20, 30))
            title = self.title_font.render("PLATFORMER 3.0" if self.state=="MENU" else "YOU BEAT THE GAME!", True, GOAL_COLOR)
            txt = self.font.render("Press SPACE to Start", True, TEXT_COLOR)
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(txt, (SCREEN_WIDTH//2 - txt.get_width()//2, SCREEN_HEIGHT//2 + 20))
        else:
            self.draw_bg()
            
            # Sort sprites so particles render behind or in front nicely
            for sprite in self.all_sprites:
                if not isinstance(sprite, FloatingText):
                    self.screen.blit(sprite.image, self.camera.apply(sprite))
                    
            # Apply moody lighting
            self.screen.blit(self.vignette, (0,0))
            
            # Render UI and Floating Text above lighting
            for ui in self.ui_elements:
                self.screen.blit(ui.image, self.camera.apply(ui))
            self.draw_hud()
            
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