import os

# Use dummy video/audio drivers if no display/valid sound device
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import sys

# Screen dimensions
WIDTH, HEIGHT = 800, 600
BG_COLOR = (0, 0, 20)
PLAYER_COLOR = (200, 200, 255)
HUD_COLOR = (255, 255, 255)
PLAYER_SIZE = 40
PLAYER_SPEED = 5

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
        self.oxygen = 100  # percentage

    def handle_input(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED

        # Keep player in bounds
        if self.rect.left < 0:
            self.rect.left = 0
            print("HAL: I can't let you go outside, Dave.")
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            print("HAL: I can't let you go outside, Dave.")
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def update(self):
        # Oxygen decreases slowly
        self.oxygen -= 0.01
        if self.oxygen <= 0:
            print("HAL: Looks like you're out of oxygen, Dave.")
            pygame.quit()
            sys.exit()

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)


def draw_hud(surface, font, player):
    """Render simple HUD elements like oxygen level."""
    oxygen_text = font.render(f"Oxygen: {int(player.oxygen)}%", True, HUD_COLOR)
    surface.blit(oxygen_text, (10, 10))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("I'm Sorry, Dave")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    player = Player()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.update()

        screen.fill(BG_COLOR)
        player.draw(screen)
        draw_hud(screen, font, player)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
