import os

# Use dummy video/audio drivers if no display/valid sound device
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
import sys
import random
from adaptive_ai import AdaptiveAI

# Screen dimensions
WIDTH, HEIGHT = 800, 600
BG_COLOR = (0, 0, 20)
PLAYER_COLOR = (200, 200, 255)
HUD_COLOR = (255, 255, 255)
PLAYER_SIZE = 40
PLAYER_SPEED = 5
ZERO_G_ACCEL = 0.5
ZERO_G_FRICTION = 0.98
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
        self.vx = 0
        self.vy = 0
        self.zero_g = True

    def handle_input(self, keys):
        if self.zero_g:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.vx -= ZERO_G_ACCEL
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.vx += ZERO_G_ACCEL
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.vy -= ZERO_G_ACCEL
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.vy += ZERO_G_ACCEL
        else:
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
        if self.zero_g:
            self.rect.x += self.vx
            self.rect.y += self.vy
            self.vx *= ZERO_G_FRICTION
            self.vy *= ZERO_G_FRICTION

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

    def toggle_zero_g(self):
        self.zero_g = not self.zero_g
        self.vx = 0
        self.vy = 0
        if self.zero_g:
            self.msg.show("Zero-G engaged.")
        else:
            self.msg.show("Magnetic boots activated.")

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


class OxygenCanister:
    """Restores a portion of the player's oxygen when collected."""
    def __init__(self, rect, amount=20):
        self.rect = rect
        self.amount = amount
        self.collected = False
        self.active = True

    def draw(self, surface):
        if not self.collected and self.active:
            pygame.draw.rect(surface, (0, 150, 150), self.rect)


class HackingPuzzle:
    """Simple sequence puzzle that increases in length each time."""
    def __init__(self, level, messenger):
        self.sequence = [
            random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            for _ in range(level + 2)
        ]
        self.index = 0
        self.active = True
        messenger.show("HACK: " + " ".join(self.sequence))
        self.messenger = messenger

    def handle_key(self, key):
        mapping = {
            pygame.K_UP: "UP",
            pygame.K_DOWN: "DOWN",
            pygame.K_LEFT: "LEFT",
            pygame.K_RIGHT: "RIGHT",
        }
        if mapping.get(key) == self.sequence[self.index]:
            self.index += 1
            if self.index >= len(self.sequence):
                self.messenger.show("Access granted.")
                self.active = False
                return True
        else:
            self.messenger.show("Access denied.")
            self.active = False
        return False


class Terminal:
    """Activates a hacking puzzle when used."""
    def __init__(self, rect, level=1):
        self.rect = rect
        self.level = level
        self.puzzle = None
        self.solved = False

    def activate(self, messenger):
        if self.solved:
            messenger.show("Terminal already hacked.")
            return
        self.puzzle = HackingPuzzle(self.level, messenger)

    def update(self, events):
        if self.puzzle and self.puzzle.active:
            for e in events:
                if e.type == pygame.KEYDOWN:
                    solved = self.puzzle.handle_key(e.key)
                    if solved:
                        self.solved = True
                        self.level += 1
                        self.puzzle = None

    def draw(self, surface):
        if not self.solved:
            pygame.draw.rect(surface, (150, 0, 150), self.rect)


class ActionNode:
    """Simple contextual action area."""
    def __init__(self, rect, description):
        self.rect = rect
        self.description = description
        self.done = False

    def activate(self, messenger):
        if not self.done:
            self.done = True
            messenger.show(self.description)

    def draw(self, surface):
        if not self.done:
            pygame.draw.rect(surface, (150, 150, 0), self.rect)


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
    ai = AdaptiveAI(messenger)

    logs = [
        LogEntry(pygame.Rect(150, 150, 30, 30),
                 "Log 1: The captain feared HAL was hiding something."),
        LogEntry(pygame.Rect(600, 400, 30, 30),
                 "Log 2: Engineering report. Multiple crew missing."),
        LogEntry(pygame.Rect(350, 100, 30, 30),
                 "Log 3: Emergency protocol initiated without consent."),
    ]

    canisters = [
        OxygenCanister(pygame.Rect(200, 300, 20, 20)),
        OxygenCanister(pygame.Rect(500, 200, 20, 20)),
    ]

    terminals = [
        Terminal(pygame.Rect(100, 500, 30, 30)),
    ]

    actions = [
        ActionNode(pygame.Rect(700, 100, 30, 30), "System repaired."),
    ]

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    player.toggle_zero_g()
                if event.key == pygame.K_e:
                    for t in terminals:
                        if player.rect.colliderect(t.rect):
                            t.activate(messenger)
                    for a in actions:
                        if player.rect.colliderect(a.rect):
                            a.activate(messenger)

        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.update()

        for t in terminals:
            t.update(events)

        for canister in canisters:
            if (not canister.collected and canister.active and
                    player.rect.colliderect(canister.rect)):
                canister.collected = True
                player.oxygen = min(100, player.oxygen + canister.amount)
                messenger.show("HAL: Enjoy that extra oxygen while you can, Dave.")
                ai.register_canister_use()

        for log in logs:
            if not log.collected and player.rect.colliderect(log.rect):
                log.collected = True
                messenger.show(log.text)
                ai.register_log_pickup()

        ai.update(canisters, logs)

        messenger.update()

        screen.fill(BG_COLOR)
        for log in logs:
            log.draw(screen)
        for canister in canisters:
            canister.draw(screen)
        for t in terminals:
            t.draw(screen)
        for a in actions:
            a.draw(screen)
        player.draw(screen)
        messenger.draw(screen, font)
        draw_hud(screen, font, player)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
