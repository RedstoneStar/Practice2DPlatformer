import pygame
import sys
from settings import *
from sprites import Player, Platform, Coin

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # Returns a new rect shifted by the camera's current offset
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # Center the camera on the target (player)
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)
        self.camera = pygame.Rect(x, y, self.width, self.height)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Enhanced 2D Platformer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.running = True

    def new(self):
        # Reset the game state and score
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        self.player = Player(100, 300)
        self.all_sprites.add(self.player)

        # Expanded Level Data (x, y, width, height)
        level_data = [
            (0, 550, 1500, 50),
            (200, 450, 200, 20),
            (450, 350, 180, 20),
            (700, 250, 150, 20),
            (950, 400, 200, 20),
            (1300, 300, 150, 20)
        ]
        
        # Coin placement (x, y)
        coin_data = [
            (250, 410), (350, 410), (500, 310), 
            (750, 210), (1050, 360), (1350, 260)
        ]

        # Spawn entities
        for p in level_data:
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.platforms.add(plat)
            
        for c in coin_data:
            coin = Coin(*c)
            self.all_sprites.add(coin)
            self.coins.add(coin)
            
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Event-driven jumping prevents multiple rapid triggers
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    self.player.jump()
            # Detect jump release for variable jump height
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    self.player.jump_cut()

    def update(self):
        self.player.update(self.platforms)
        self.camera.update(self.player)
        
        # Check for Coin Collection
        hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        for hit in hits:
            self.score += 10
            
        # Death Mechanic / Void Respawn
        if self.player.rect.top > SCREEN_HEIGHT + 200:
            self.new() # Restart level if they fall too far

    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Draw all sprites shifted by the camera offset
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            
        # Render UI
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (15, 15))
        
        pygame.display.flip()

if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
    pygame.quit()
    sys.exit()