import random

class AdaptiveAI:
    """Rule-based system that tweaks resources as the player adapts."""

    def __init__(self, messenger):
        self.messenger = messenger
        self.canister_uses = 0
        self.log_finds = 0
        self.difficulty = 1

    def register_canister_use(self):
        self.canister_uses += 1
        if self.canister_uses == 2:
            self.difficulty += 1
            self.messenger.show("HAL: I see you're relying on oxygen canisters, Dave.")

    def register_log_pickup(self):
        self.log_finds += 1
        if self.log_finds == 2:
            self.difficulty += 1
            self.messenger.show("HAL: You're becoming quite inquisitive, Dave.")

    def update(self, canisters, logs):
        """Modify resource availability based on the player's past actions."""
        if self.difficulty >= 2:
            # Chance to disable unused canisters
            for c in canisters:
                if not c.collected and c.active and random.random() < 0.3:
                    c.active = False
                    self.messenger.show("HAL: I've secured an oxygen canister, Dave.")

        if self.difficulty >= 3:
            # Randomize remaining log locations to keep things unpredictable
            for log in logs:
                if not log.collected and random.random() < 0.2:
                    log.rect.x = random.randint(50, 750)
                    log.rect.y = random.randint(50, 550)
                    self.messenger.show("HAL: I've moved some files for safekeeping, Dave.")

