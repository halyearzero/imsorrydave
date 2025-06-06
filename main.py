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
MESSAGE_DURATION = 180  # frames

class MessageManager:
    """Utility to display short text on screen and log it to the console."""
    def __init__(self):
        self.text = ""
        self.timer = 0

    def show(self, text):
        self.text = text
        self.timer = MESSAGE_DURATION
        print(text)

    def update(self):
        if self.timer > 0:
            self.timer -= 1

    def draw(self, surface, font):
        if self.timer > 0:
            msg_surface = font.render(self.text, True, HUD_COLOR)
            surface.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2,
                                       HEIGHT - 30))

class Player:
    def __init__(self, messenger):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, PLAYER_SIZE, PLAYER_SIZE)
        self.oxygen = 100  # percentage
        self.msg = messenger
        self.low_warned = False
        self.crit_warned = False

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
            self.msg.show("HAL: I can't let you go outside, Dave.")
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.msg.show("HAL: I can't let you go outside, Dave.")
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def update(self):
        # Oxygen decreases slowly
        self.oxygen -= 0.01
        if not self.low_warned and self.oxygen <= 50:
            self.msg.show("HAL: Your oxygen is running low, Dave.")
            self.low_warned = True
        if not self.crit_warned and self.oxygen <= 25:
            self.msg.show("HAL: You can't survive much longer, Dave.")
            self.crit_warned = True
        if self.oxygen <= 0:
            self.msg.show("HAL: Looks like you're out of oxygen, Dave.")
            pygame.quit()
            sys.exit()

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)


class LogEntry:
    """Simple collectible log that reveals backstory when found."""
    def __init__(self, rect, text):
        self.rect = rect
        self.text = text
        self.collected = False

    def draw(self, surface):
        if not self.collected:
            pygame.draw.rect(surface, (100, 100, 100), self.rect)


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

    messenger = MessageManager()
    player = Player(messenger)

    logs = [
        LogEntry(pygame.Rect(150, 150, 30, 30),
                 "Log 1: The captain feared HAL was hiding something."),
        LogEntry(pygame.Rect(600, 400, 30, 30),
                 "Log 2: Engineering report. Multiple crew missing."),
        LogEntry(pygame.Rect(350, 100, 30, 30),
                 "Log 3: Emergency protocol initiated without consent."),
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.update()

        for log in logs:
            if not log.collected and player.rect.colliderect(log.rect):
                log.collected = True
                messenger.show(log.text)

        messenger.update()

        screen.fill(BG_COLOR)
        for log in logs:
            log.draw(screen)
        player.draw(screen)
        messenger.draw(screen, font)
        draw_hud(screen, font, player)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
