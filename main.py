import pygame
import sys
from settings import *
from sprites import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target, dt):
        # Smooth Camera Lerp instead of rigid locking
        target_x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        target_y = -target.rect.centery + int(SCREEN_HEIGHT / 2)
        
        self.camera.x += (target_x - self.camera.x) * 5 * dt
        self.camera.y += (target_y - self.camera.y) * 5 * dt

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Engine V2: Physics, States & Entities")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.state = "MENU" # Menu, Playing, Win
        self.score = 0

    def load_level(self):
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.interactables = pygame.sprite.Group()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Parse string map
        for row, tiles in enumerate(LEVEL_MAP):
            for col, tile in enumerate(tiles):
                x, y = col * TILE_SIZE, row * TILE_SIZE
                if tile == "P":
                    self.player = Player(x, y)
                    self.all_sprites.add(self.player)
                elif tile == "X":
                    p = Platform(x, y)
                    self.all_sprites.add(p)
                    self.platforms.add(p)
                elif tile == "B":
                    p = Platform(x, y, breakable=True)
                    self.all_sprites.add(p)
                    self.platforms.add(p)
                elif tile == "M":
                    p = Platform(x, y, moving=True)
                    self.all_sprites.add(p)
                    self.platforms.add(p)
                elif tile == "C":
                    c = Coin(x, y)
                    self.all_sprites.add(c)
                    self.coins.add(c)
                elif tile == "E":
                    e = Enemy(x, y)
                    self.all_sprites.add(e)
                    self.enemies.add(e)
                elif tile == "^":
                    h = StaticEntity(x, int(y + TILE_SIZE/2), HAZARD_COLOR)
                    h.image = pygame.Surface((TILE_SIZE, TILE_SIZE//2))
                    h.image.fill(HAZARD_COLOR)
                    h.rect = h.image.get_rect(topleft=(x, int(y + TILE_SIZE/2)))
                    self.all_sprites.add(h)
                    self.hazards.add(h)
                elif tile == "F":
                    f = StaticEntity(x, y, (50, 150, 255), "CHECKPOINT")
                    self.all_sprites.add(f)
                    self.interactables.add(f)
                elif tile == "G":
                    g = StaticEntity(x, y, GOAL_COLOR, "GOAL")
                    self.all_sprites.add(g)
                    self.interactables.add(g)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if self.state == "MENU" and event.key == pygame.K_SPACE:
                    self.score = 0
                    self.load_level()
                    self.state = "PLAYING"
                elif self.state == "WIN" and event.key == pygame.K_SPACE:
                    self.state = "MENU"
                elif self.state == "PLAYING":
                    if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                        self.player.jump()
                        
            if event.type == pygame.KEYUP and self.state == "PLAYING":
                if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                    self.player.jump_cut()

    def update(self, dt):
        if self.state != "PLAYING": return
        
        # Pass dt scalar to physics objects
        self.player.update(dt, self.platforms, self.hazards, self.enemies)
        self.enemies.update(dt)
        self.coins.update(dt)
        self.particles.update(dt)
        self.platforms.update(dt)
        self.camera.update(self.player, dt)
        
        # Interactions
        if pygame.sprite.spritecollide(self.player, self.coins, True):
            self.score += 10
            for _ in range(5):
                p = Particle(self.player.rect.centerx, self.player.rect.centery, COIN_COLOR)
                self.all_sprites.add(p)
                self.particles.add(p)
                
        interacts = pygame.sprite.spritecollide(self.player, self.interactables, False)
        for i in interacts:
            if i.tag == "CHECKPOINT":
                self.player.spawn_point = vec(i.rect.x, i.rect.y)
                i.image.fill((50, 255, 50)) # Turn green
            elif i.tag == "GOAL":
                self.state = "WIN"

    def draw(self):
        self.screen.fill(BG_COLOR)
        
        if self.state == "MENU":
            txt = self.font.render("Press SPACE to Start", True, TEXT_COLOR)
            self.screen.blit(txt, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
        elif self.state == "WIN":
            txt = self.font.render(f"You Win! Score: {self.score} - Press SPACE", True, TEXT_COLOR)
            self.screen.blit(txt, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))
        else:
            # Simple Parallax Effect
            pygame.draw.rect(self.screen, (35, 35, 45), (self.camera.camera.x * 0.5 % SCREEN_WIDTH, 100, 200, 400))
            
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            
            score_text = self.font.render(f"Score: {self.score} | Timer: {pygame.time.get_ticks()//1000}", True, TEXT_COLOR)
            self.screen.blit(score_text, (15, 15))
            
        pygame.display.flip()

    def run(self):
        while True:
            # Calculate Delta Time in seconds
            dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update(dt)
            self.draw()

if __name__ == "__main__":
    g = Game()
    g.run()